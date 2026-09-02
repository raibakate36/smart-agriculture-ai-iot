from sqlalchemy import Column, Integer, String, Float

from app.database.connection import Base


class CropConfiguration(Base):
    __tablename__ = "crop_configurations"

    id = Column(Integer, primary_key=True, index=True)

    crop_name = Column(String, unique=True, nullable=False)

    min_moisture = Column(Float, nullable=False)
    target_moisture = Column(Float, nullable=False)
    max_moisture = Column(Float, nullable=False)