from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime

from app.database.connection import Base


class DiseaseAnalysis(Base):
    __tablename__ = "disease_analyses"

    id = Column(Integer, primary_key=True, index=True)

    filename = Column(String, nullable=False)

    disease = Column(String, nullable=False)

    confidence = Column(Float, nullable=False)

    device_id = Column(String, nullable=True)

    crop = Column(String, nullable=True)

    timestamp = Column(
        DateTime,
        default=datetime.utcnow
    )