from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class SortOrder(str, Enum):
    asc = "asc"
    desc = "desc"


class LocationSortBy(str, Enum):
    name = "name"
    created_at = "created_at"
    distance = "distance"


class LocationQuery(BaseModel):
    page: int = Field(1, ge=1, description="Page number")
    per_page: int = Field(10, ge=1, le=100, description="Items per page")
    search: Optional[str] = Field(None, description="Search in name or description")
    sort_by: LocationSortBy = Field(LocationSortBy.created_at, description="Sort field")
    sort_order: SortOrder = Field(SortOrder.desc, description="Sort direction")


class DistanceRangeQuery(BaseModel):
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    min_distance_meters: int = Field(0, ge=0, description="Minimum distance")
    max_distance_meters: int = Field(..., gt=0, le=50000, description="Maximum distance")
    page: int = Field(1, ge=1)
    per_page: int = Field(10, ge=1, le=100)
    sort_by: LocationSortBy = Field(LocationSortBy.distance)
    sort_order: SortOrder = Field(SortOrder.asc)
