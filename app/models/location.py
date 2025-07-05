from geoalchemy2 import Geometry
from sqlalchemy import Column, Integer, String, Text, DateTime, Index
from sqlalchemy.sql import func
from app.core.database import Base


class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    description = Column(Text, nullable=True)
    point = Column(
        Geometry(geometry_type='POINT', srid=4326),  # WGS84
        nullable=False
    )
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Spatial index for point column - critical for spatial query performance
    __table_args__ = (
        Index('idx_locations_point', 'point', postgresql_using='gist'),
        Index('idx_locations_created_at', 'created_at'),  # For time-based queries
    )
