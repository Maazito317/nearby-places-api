from sqlalchemy.orm import Session
from sqlalchemy import func
from geoalchemy2 import functions
from app.models.location import Location
from shapely.geometry import Point
from geoalchemy2.shape import from_shape


def find_locations_within_distance(
    db: Session,
    latitude: float,
    longitude: float,
    distance_meters: int
) -> list[Location]:
    """
    Find all locations within specified distance of a point using ST_DWithin.
    Uses spatial index for fast querying.
    """
    query_point = from_shape(Point(longitude, latitude), srid=4326)

    return db.query(Location).filter(
        functions.ST_DWithin(
            Location.point,
            query_point,
            distance_meters
        )
    ).all()


def calculate_distance(db: Session,
                       location_id: int,
                       latitude: float,
                       longitude: float) -> float:
    """
    Calculate exact distance between a location and a point using ST_Distance.
    Returns distance in meters.
    """
    query_point = from_shape(Point(longitude, latitude), srid=4326)

    result = db.query(
        functions.ST_Distance(Location.point, query_point)
    ).filter(Location.id == location_id).scalar()

    return float(result) if result else None


def validate_coordinates(latitude: float, longitude: float) -> bool:
    """Validate lat/lng are within valid bounds"""
    return -90 <= latitude <= 90 and -180 <= longitude <= 180
