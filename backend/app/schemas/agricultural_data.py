from pydantic import BaseModel


class AgriculturalDataCreate(BaseModel):
    crop: str

    soil_ph: float | None = None
    nitrogen: float | None = None
    phosphorus: float | None = None
    potassium: float | None = None

    soil_moisture: float | None = None
    temperature: float | None = None
    humidity: float | None = None

    target: str | None = None