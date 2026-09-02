from sqlalchemy import Column, Integer, String, Float

from app.database.connection import Base


class AgriculturalData(Base):
    __tablename__ = "agricultural_data"

    id = Column(Integer, primary_key=True, index=True)

    crop = Column(String, nullable=False)

    soil_ph = Column(Float, nullable=True)
    nitrogen = Column(Float, nullable=True)
    phosphorus = Column(Float, nullable=True)
    potassium = Column(Float, nullable=True)

    soil_moisture = Column(Float, nullable=True)
    temperature = Column(Float, nullable=True)
    humidity = Column(Float, nullable=True)

    target = Column(String, nullable=True)