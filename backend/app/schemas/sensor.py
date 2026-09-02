from pydantic import BaseModel


class SensorData(BaseModel):
    device_id: str
    crop: str
    soil_moisture: float
    temperature: float
    humidity: float
    soil_ph: float
    nitrogen: float
    phosphorus: float
    potassium: float