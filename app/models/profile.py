from datetime import datetime
from sqlalchemy import Column, Integer, String, Numeric, DateTime, CheckConstraint, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base

class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    auth_id = Column(String, ForeignKey("authentications.id"), nullable=False)
    # profile fields
    preference = Column(String(10), nullable=True)         # 'CARDIO' | 'WEIGHT'
    weight_unit = Column(String(3), nullable=True)         # 'KG' | 'LBS'
    height_unit = Column(String(4), nullable=True)         # 'CM' | 'INCH'
    weight = Column(Numeric(6, 2), nullable=True)          # 10..1000
    height = Column(Numeric(6, 2), nullable=True)          # 3..250
    name = Column(String(60), nullable=True)
    image_uri = Column(String(1024), nullable=True)

    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    __table_args__ = (
        CheckConstraint("(weight IS NULL) OR (weight >= 10 AND weight <= 1000)", name="chk_weight_range"),
        CheckConstraint("(height IS NULL) OR (height >= 3 AND height <= 250)", name="chk_height_range"),
    )
