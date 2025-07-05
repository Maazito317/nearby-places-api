from typing import Dict, Tuple
from shapely.geometry import Point
from shapely import wkt, wkb
from geoalchemy2.shape import to_shape, from_shape
from geoalchemy2.elements import WKTElement, WKBElement
import json


def point_to_geojson(point: Point) -> Dict:
    """Convert Shapely Point to GeoJSON format"""
    return {
        "type": "Point",
        "coordinates": [point.x, point.y]  # [longitude, latitude]
    }


def geojson_to_point(geojson: Dict) -> Point:
    """Convert GeoJSON Point to Shapely Point"""
    coords = geojson["coordinates"]
    return Point(coords[0], coords[1])  # longitude, latitude


def latlong_to_point(latitude: float, longitude: float) -> Point:
    """Convert lat/lng pair to Shapely Point"""
    return Point(longitude, latitude)  # Note: lng first!


def point_to_latlong(point: Point) -> Tuple[float, float]:
    """Convert Shapely Point to (latitude, longitude) tuple"""
    return (point.y, point.x)  # lat, lng


def point_to_wkt(point: Point) -> str:
    """Convert Shapely Point to Well-Known Text"""
    return point.wkt


def wkt_to_point(wkt_string: str) -> Point:
    """Convert WKT string to Shapely Point"""
    return wkt.loads(wkt_string)


def db_point_to_shapely(db_point) -> Point:
    """Convert database geometry to Shapely Point"""
    return to_shape(db_point)


def shapely_to_db_point(point: Point, srid: int = 4326) -> WKTElement:
    """Convert Shapely Point to database geometry"""
    return from_shape(point, srid=srid)


def validate_geojson_point(geojson: Dict) -> bool:
    """Validate GeoJSON Point structure"""
    try:
        return (
            geojson.get("type") == "Point" and
            "coordinates" in geojson and
            len(geojson["coordinates"]) == 2 and
            all(isinstance(coord, (int, float)) for coord in geojson["coordinates"])
        )
    except (TypeError, KeyError):
        return False
