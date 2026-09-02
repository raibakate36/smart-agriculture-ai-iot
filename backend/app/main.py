from fastapi import FastAPI, Depends
from fastapi import UploadFile,File
from sqlalchemy.orm import Session
from app.database.connection import SessionLocal
from app.models.sensor import SensorReading

from app.schemas.sensor import SensorData
from app.database.connection import Base, engine, SessionLocal
from app.models.sensor import SensorReading
from app.services.irrigation import irrigation_decision
from app.models.crop import CropConfiguration
from app.schemas.crop import CropConfigurationCreate
from app.models.agricultural_data import AgriculturalData
from app.schemas.agricultural_data import AgriculturalDataCreate
from app.services.plant_analysis import analyze_plant_image
from app.services.crop_health import analyze_tomato_condition
from app.services.recommendation_engine import generate_recommendation

# Create database tables
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Smart Agriculture API",
    description="Backend for IoT-based Smart Agriculture System",
    version="1.0.0"
)


# Database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {
        "message": "Smart Agriculture API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


@app.post("/api/v1/sensor-data")
def receive_sensor_data(
    data: SensorData,
    db: Session = Depends(get_db)
):
    sensor_reading = SensorReading(
        device_id=data.device_id,
        crop=data.crop,
        soil_moisture=data.soil_moisture,
        temperature=data.temperature,
        humidity=data.humidity,
        soil_ph=data.soil_ph,
        nitrogen=data.nitrogen,
        phosphorus=data.phosphorus,
        potassium=data.potassium
    )

    db.add(sensor_reading)
    db.commit()
    db.refresh(sensor_reading)

    return {
        "message": "Sensor data saved successfully",
        "id": sensor_reading.id
    }

@app.get("/api/v1/sensor-data/latest")
def get_latest_sensor_data(db: Session = Depends(get_db)):
    latest_reading = (
        db.query(SensorReading)
        .order_by(SensorReading.timestamp.desc())
        .first()
    )

    if latest_reading is None:
        return {
            "message": "No sensor data available"
        }

    return {
        "id": latest_reading.id,
        "device_id": latest_reading.device_id,
        "crop": latest_reading.crop,
        "soil_moisture": latest_reading.soil_moisture,
        "temperature": latest_reading.temperature,
        "humidity": latest_reading.humidity,
        "soil_ph": latest_reading.soil_ph,
        "nitrogen": latest_reading.nitrogen,
        "phosphorus": latest_reading.phosphorus,
        "potassium": latest_reading.potassium,
        "timestamp": latest_reading.timestamp
    }

@app.get("/api/v1/irrigation/status")
def get_irrigation_status(db: Session = Depends(get_db)):
    latest_reading = (
        db.query(SensorReading)
        .order_by(SensorReading.timestamp.desc())
        .first()
    )

    if latest_reading is None:
        return {
            "message": "No sensor data available"
        }

    crop = (
        db.query(CropConfiguration)
        .filter(
            CropConfiguration.crop_name == latest_reading.crop
        )
        .first()
    )

    if crop is None:
        return {
            "message": "Crop configuration not found",
            "crop": latest_reading.crop
        }

    decision = irrigation_decision(
        soil_moisture=latest_reading.soil_moisture,
        temperature=latest_reading.temperature,
        humidity=latest_reading.humidity,
        min_moisture=crop.min_moisture,
        target_moisture=crop.target_moisture
    )

    return {
        "crop": latest_reading.crop,
        **decision
    }

@app.post("/api/v1/crops")
def create_crop(
    data: CropConfigurationCreate,
    db: Session = Depends(get_db)
):
    crop = CropConfiguration(
        crop_name=data.crop_name,
        min_moisture=data.min_moisture,
        target_moisture=data.target_moisture,
        max_moisture=data.max_moisture
    )

    db.add(crop)
    db.commit()
    db.refresh(crop)

    return {
        "message": "Crop configuration created successfully",
        "id": crop.id,
        "crop": crop.crop_name
    }

@app.post("/api/v1/agricultural-data")
def create_agricultural_data(
    data: AgriculturalDataCreate,
    db: Session = Depends(get_db)
):
    record = AgriculturalData(
        crop=data.crop,
        soil_ph=data.soil_ph,
        nitrogen=data.nitrogen,
        phosphorus=data.phosphorus,
        potassium=data.potassium,
        soil_moisture=data.soil_moisture,
        temperature=data.temperature,
        humidity=data.humidity,
        target=data.target
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    return {
        "message": "Agricultural data saved successfully",
        "id": record.id
    }

@app.get("/api/v1/agricultural-data")
def get_agricultural_data(db: Session = Depends(get_db)):
    records = (
        db.query(AgriculturalData)
        .order_by(AgriculturalData.id.desc())
        .all()
    )

    return records

@app.post("/api/v1/plant-image/analyze")
async def analyze_plant_image_endpoint(
    image: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    result = analyze_plant_image(
        filename=image.filename,
        file=image.file
    )

    latest_sensor = (
        db.query(SensorReading)
        .order_by(SensorReading.timestamp.desc())
        .first()
    )

    if latest_sensor is not None:

        recommendation = generate_recommendation(
            disease=result["prediction"]["disease"],
            confidence=result["prediction"]["confidence"],
            soil_moisture=latest_sensor.soil_moisture,
            temperature=latest_sensor.temperature,
            humidity=latest_sensor.humidity,
            soil_ph=latest_sensor.soil_ph,
            nitrogen=latest_sensor.nitrogen,
            phosphorus=latest_sensor.phosphorus,
            potassium=latest_sensor.potassium,
        )

        result["recommendation"] = recommendation

        result["sensor_data"] = {
            "device_id": latest_sensor.device_id,
            "crop": latest_sensor.crop,
            "soil_moisture": latest_sensor.soil_moisture,
            "temperature": latest_sensor.temperature,
            "humidity": latest_sensor.humidity,
            "soil_ph": latest_sensor.soil_ph,
            "nitrogen": latest_sensor.nitrogen,
            "phosphorus": latest_sensor.phosphorus,
            "potassium": latest_sensor.potassium,
            "timestamp": latest_sensor.timestamp,
        }

    else:

        result["recommendation"] = generate_recommendation(
            disease=result["prediction"]["disease"],
            confidence=result["prediction"]["confidence"]
        )

        result["sensor_data"] = None

    return result

@app.post("/api/v1/crop-health/analyze")
def crop_health_analysis(
    soil_moisture: float,
    temperature: float,
    humidity: float,
    soil_ph: float | None = None,
    nitrogen: float | None = None,
    phosphorus: float | None = None,
    potassium: float | None = None,
    image_condition: str | None = None,
):
    result = analyze_tomato_condition(
        soil_moisture=soil_moisture,
        temperature=temperature,
        humidity=humidity,
        soil_ph=soil_ph,
        nitrogen=nitrogen,
        phosphorus=phosphorus,
        potassium=potassium,
        image_condition=image_condition,
    )

    return result

@app.get("/api/v1/crop-health/live")
def live_crop_health(db: Session = Depends(get_db)):

    latest_sensor = (
        db.query(SensorReading)
        .order_by(SensorReading.timestamp.desc())
        .first()
    )

    if latest_sensor is None:
        return {
            "message": "No sensor data available"
        }

    result = analyze_tomato_condition(
        soil_moisture=latest_sensor.soil_moisture,
        temperature=latest_sensor.temperature,
        humidity=latest_sensor.humidity,
        soil_ph=latest_sensor.soil_ph,
        nitrogen=latest_sensor.nitrogen,
        phosphorus=latest_sensor.phosphorus,
        potassium=latest_sensor.potassium,
    )

    return {
        "device_id": latest_sensor.device_id,
        "crop": latest_sensor.crop,
        "sensor_timestamp": latest_sensor.timestamp,
        "sensor_data": {
            "soil_moisture": latest_sensor.soil_moisture,
            "temperature": latest_sensor.temperature,
            "humidity": latest_sensor.humidity,
            "soil_ph": latest_sensor.soil_ph,
            "nitrogen": latest_sensor.nitrogen,
            "phosphorus": latest_sensor.phosphorus,
            "potassium": latest_sensor.potassium,
        },
        "crop_health": result
    }

@app.get("/api/v1/field-analysis")
def field_analysis(db: Session = Depends(get_db)):

    # --------------------------------------------------------
    # Get latest sensor reading
    # --------------------------------------------------------

    latest_sensor = (
        db.query(SensorReading)
        .order_by(SensorReading.timestamp.desc())
        .first()
    )

    if latest_sensor is None:
        return {
            "status": "no_sensor_data",
            "message": "No sensor readings are available."
        }

    # --------------------------------------------------------
    # Run crop health analysis
    # --------------------------------------------------------

    crop_health = analyze_tomato_condition(
        soil_moisture=latest_sensor.soil_moisture,
        temperature=latest_sensor.temperature,
        humidity=latest_sensor.humidity,
        soil_ph=latest_sensor.soil_ph,
        nitrogen=latest_sensor.nitrogen,
        phosphorus=latest_sensor.phosphorus,
        potassium=latest_sensor.potassium,
    )

    # --------------------------------------------------------
    # Irrigation decision
    # --------------------------------------------------------

    crop = (
        db.query(CropConfiguration)
        .filter(
            CropConfiguration.crop_name == latest_sensor.crop
        )
        .first()
    )

    irrigation = None

    if crop is not None:

        irrigation = irrigation_decision(
            soil_moisture=latest_sensor.soil_moisture,
            temperature=latest_sensor.temperature,
            humidity=latest_sensor.humidity,
            min_moisture=crop.min_moisture,
            target_moisture=crop.target_moisture
        )

    # --------------------------------------------------------
    # Return complete field status
    # --------------------------------------------------------

    return {
        "status": "analysis_complete",

        "field": {
            "device_id": latest_sensor.device_id,
            "crop": latest_sensor.crop,
            "timestamp": latest_sensor.timestamp,
        },

        "sensor_data": {
            "soil_moisture": latest_sensor.soil_moisture,
            "temperature": latest_sensor.temperature,
            "humidity": latest_sensor.humidity,
            "soil_ph": latest_sensor.soil_ph,
            "nitrogen": latest_sensor.nitrogen,
            "phosphorus": latest_sensor.phosphorus,
            "potassium": latest_sensor.potassium,
        },

        "irrigation": irrigation,

        "crop_health": crop_health,

        "note": (
            "Disease diagnosis requires a plant image. "
            "Use /api/v1/plant-image/analyze for image-based disease detection."
        )
    }