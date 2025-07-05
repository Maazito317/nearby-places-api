from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime


class LocationBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Location name")
    description: Optional[str] = Field(None, description="Location description")


class LocationCreate(LocationBase):
    latitude: float = Field(..., ge=-90, le=90, description="Latitude (-90 to 90)")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude (-180 to 180)")


class LocationCreateGeoJSON(LocationBase):
    point: dict = Field(..., description="GeoJSON Point geometry")

    @validator('point')
    def validate_geojson_point(cls, v):
        if not isinstance(v, dict):
            raise ValueError('Point must be a dict')
        if v.get('type') != 'Point':
            raise ValueError('Geometry type must be Point')
        coords = v.get('coordinates')
        if not coords or len(coords) != 2:
            raise ValueError('Point must have exactly 2 coordinates')
        lng, lat = coords
        if not (-180 <= lng <= 180) or not (-90 <= lat <= 90):
            raise ValueError('Invalid coordinates')
        return v


class LocationResponse(LocationBase):
    id: int
    latitude: float
    longitude: float
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Allows conversion from SQLAlchemy models


class LocationGeoJSON(LocationBase):
    id: int
    geometry: dict
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class LocationWithDistance(LocationResponse):
    distance_meters: float = Field(..., description="Distance from query point in meters")


class LocationListResponse(BaseModel):
    locations: List[LocationResponse]
    total: int
    page: int
    per_page: int
    has_next: bool


class NearbySearchParams(BaseModel):
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    distance_meters: int = Field(..., gt=0, le=50000, description="Search radius in meters (max 50km)")
    page: int = Field(1, ge=1, description="Page number")
    per_page: int = Field(10, ge=1, le=100, description="Items per page")
