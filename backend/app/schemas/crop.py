from pydantic import BaseModel


class CropConfigurationCreate(BaseModel):
    crop_name: str
    min_moisture: float
    target_moisture: float
    max_moisture: float