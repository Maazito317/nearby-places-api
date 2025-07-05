from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, asc
from geoalchemy2 import functions
from app.models.location import Location
from app.core.geometry import shapely_to_db_point, db_point_to_shapely
from shapely.geometry import Point


class LocationRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, name: str, description: str, point: Point) -> Location:
        """Create a new location"""
        db_location = Location(
            name=name,
            description=description,
            point=shapely_to_db_point(point)
        )
        self.db.add(db_location)
        self.db.commit()
        self.db.refresh(db_location)
        return db_location

    def get_by_id(self, location_id: int) -> Optional[Location]:
        """Get location by ID"""
        return self.db.query(Location).filter(Location.id == location_id).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Location]:
        """Get all locations with pagination"""
        return self.db.query(Location).offset(skip).limit(limit).all()

    def find_within_distance(
        self,
        center_point: Point,
        distance_meters: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[Location]:
        """Find locations within distance, with pagination"""
        query_point = shapely_to_db_point(center_point)

        return self.db.query(Location).filter(
            functions.ST_DWithin(
                Location.point,
                query_point,
                distance_meters
            )
        ).offset(skip).limit(limit).all()

    def find_within_distance_with_distances(
        self,
        center_point: Point,
        distance_meters: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[tuple[Location, float]]:
        """Find locations within distance and return with calculated distances"""
        query_point = shapely_to_db_point(center_point)

        results = self.db.query(
            Location,
            functions.ST_Distance(Location.point, query_point).label('distance')
        ).filter(
            functions.ST_DWithin(Location.point, query_point, distance_meters)
        ).order_by(asc('distance')).offset(skip).limit(limit).all()

        return [(location, float(distance)) for location, distance in results]

    def delete(self, location_id: int) -> bool:
        """Delete location by ID"""
        location = self.get_by_id(location_id)
        if location:
            self.db.delete(location)
            self.db.commit()
            return True
        return False

    def count_total(self) -> int:
        """Get total count of locations"""
        return self.db.query(Location).count()

    def count_within_distance(self, center_point: Point, distance_meters: int) -> int:
        """Count locations within distance"""
        query_point = shapely_to_db_point(center_point)
        return self.db.query(Location).filter(
            functions.ST_DWithin(Location.point, query_point, distance_meters)
        ).count()
