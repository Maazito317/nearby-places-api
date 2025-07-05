from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, asc, or_
from geoalchemy2 import functions
from app.models.location import Location
from app.core.geometry import shapely_to_db_point, db_point_to_shapely
from shapely.geometry import Point
from app.schemas.query_schemas import LocationQuery, DistanceRangeQuery, SortOrder, LocationSortBy

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
    
    def location_exists_at_point(self, point: Point, tolerance_meters: int = 10) -> bool:
        """Check if a location already exists within tolerance distance of this point"""
        query_point = shapely_to_db_point(point)
        
        existing = self.db.query(Location).filter(
            functions.ST_DWithin(
                Location.point,
                query_point,
                tolerance_meters
            )
        ).first()
        
        return existing is not None

    def create_if_not_exists(self, name: str, description: str, point: Point, tolerance_meters: int = 10) -> tuple[Location, bool]:
        """Create location only if one doesn't exist nearby. Returns (location, was_created)"""
        if self.location_exists_at_point(point, tolerance_meters):
            # Find and return existing location
            query_point = shapely_to_db_point(point)
            existing = self.db.query(Location).filter(
                functions.ST_DWithin(Location.point, query_point, tolerance_meters)
            ).first()
            return existing, False
        
        # Create new location
        new_location = self.create(name, description, point)
        return new_location, True

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

    def get_all_with_filters(self, query_params: LocationQuery) -> tuple[List[Location], int]:
        """Get locations with filtering, sorting, and pagination"""
        base_query = self.db.query(Location)

        # Apply search filter
        if query_params.search:
            search_term = f"%{query_params.search}%"
            base_query = base_query.filter(
                or_(
                    Location.name.ilike(search_term),
                    Location.description.ilike(search_term)
                )
            )

        # Get total count before pagination
        total_count = base_query.count()

        # Apply sorting
        if query_params.sort_by == LocationSortBy.name:
            sort_column = Location.name
        elif query_params.sort_by == LocationSortBy.created_at:
            sort_column = Location.created_at

        if query_params.sort_order == SortOrder.asc:
            base_query = base_query.order_by(asc(sort_column))
        else:
            base_query = base_query.order_by(desc(sort_column))

        # Apply pagination
        skip = (query_params.page - 1) * query_params.per_page
        locations = base_query.offset(skip).limit(query_params.per_page).all()

        return locations, total_count

    def find_within_distance_range(
        self,
        query_params: DistanceRangeQuery
    ) -> tuple[List[tuple[Location, float]], int]:
        """Find locations within a distance range (between min and max distance)"""
        center_point = shapely_to_db_point(
            Point(query_params.longitude, query_params.latitude)
        )

        # Separate count query - just count IDs
        count_query = self.db.query(Location.id).filter(
            functions.ST_DWithin(
                Location.point, 
                center_point, 
                query_params.max_distance_meters
            )
        )

        # Add minimum distance filter if specified
        if query_params.min_distance_meters > 0:
            count_query = count_query.filter(
                functions.ST_Distance(Location.point, center_point) >= query_params.min_distance_meters
            )

        total_count = count_query.count()

        # Main query with distance calculation
        main_query = self.db.query(
            Location,
            functions.ST_Distance(Location.point, center_point).label('distance')
        ).filter(
            functions.ST_DWithin(
                Location.point, 
                center_point, 
                query_params.max_distance_meters
            )
        )

        # Add minimum distance filter
        if query_params.min_distance_meters > 0:
            main_query = main_query.filter(
                functions.ST_Distance(Location.point, center_point) >= query_params.min_distance_meters
            )

        # Apply sorting and pagination
        if query_params.sort_order == SortOrder.asc:
            main_query = main_query.order_by(asc('distance'))
        else:
            main_query = main_query.order_by(desc('distance'))

        skip = (query_params.page - 1) * query_params.per_page
        results = main_query.offset(skip).limit(query_params.per_page).all()

        return [(location, float(distance)) for location, distance in results], total_count
