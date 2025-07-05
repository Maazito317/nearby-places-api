from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.dependencies import get_db
from app.repositories.location_repository import LocationRepository
from app.schemas.location_schemas import (
    LocationCreate, LocationResponse, LocationWithDistance,
    NearbySearchParams, LocationListResponse
)
from app.core.geometry import latlong_to_point, db_point_to_shapely, point_to_latlong

router = APIRouter(prefix="/locations", tags=["locations"])


@router.post("/", response_model=LocationResponse, status_code=status.HTTP_201_CREATED)
def create_location(
    location: LocationCreate,
    db: Session = Depends(get_db)
):
    """Create a new location"""
    repo = LocationRepository(db)
    point = latlong_to_point(location.latitude, location.longitude)

    db_location = repo.create_if_not_exists(
        name=location.name,
        description=location.description,
        point=point
    )

    # Convert back to response format
    shapely_point = db_point_to_shapely(db_location.point)
    lat, lng = point_to_latlong(shapely_point)

    return LocationResponse(
        id=db_location.id,
        name=db_location.name,
        description=db_location.description,
        latitude=lat,
        longitude=lng,
        created_at=db_location.created_at,
        updated_at=db_location.updated_at
    )


@router.get("/{location_id}", response_model=LocationResponse)
def get_location(
    location_id: int,
    db: Session = Depends(get_db)
):
    """Get a single location by ID"""
    repo = LocationRepository(db)
    location = repo.get_by_id(location_id)

    if not location:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Location not found"
        )

    shapely_point = db_point_to_shapely(location.point)
    lat, lng = point_to_latlong(shapely_point)

    return LocationResponse(
        id=location.id,
        name=location.name,
        description=location.description,
        latitude=lat,
        longitude=lng,
        created_at=location.created_at,
        updated_at=location.updated_at
    )


@router.delete("/{location_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_location(
    location_id: int,
    db: Session = Depends(get_db)
):
    """Delete a location"""
    repo = LocationRepository(db)
    if not repo.delete(location_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Location not found"
        )


@router.get("/nearby/search", response_model=List[LocationWithDistance])
def find_nearby_locations(
    params: NearbySearchParams = Depends(),
    db: Session = Depends(get_db)
):
    """Find locations within specified distance"""
    repo = LocationRepository(db)
    center_point = latlong_to_point(params.latitude, params.longitude)

    # Calculate pagination
    skip = (params.page - 1) * params.per_page

    results = repo.find_within_distance_with_distances(
        center_point=center_point,
        distance_meters=params.distance_meters,
        skip=skip,
        limit=params.per_page
    )

    response = []
    for location, distance in results:
        shapely_point = db_point_to_shapely(location.point)
        lat, lng = point_to_latlong(shapely_point)

        response.append(LocationWithDistance(
            id=location.id,
            name=location.name,
            description=location.description,
            latitude=lat,
            longitude=lng,
            created_at=location.created_at,
            updated_at=location.updated_at,
            distance_meters=distance
        ))

    return response
