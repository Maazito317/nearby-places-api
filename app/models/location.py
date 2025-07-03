from geoalchemy2 import Geometry
from sqlalchemy import Column, Integer, String
from app.core.database import Base


class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    point = Column(
        Geometry(geometry_type='POINT', srid=4326),  # WGS84
        nullable=False
    )
