from app.core.dependencies import get_db
from app.repositories.location_repository import LocationRepository
from app.schemas.query_schemas import LocationQuery, DistanceRangeQuery
from app.core.geometry import latlong_to_point

# Create some test data first
db_gen = get_db()
db = next(db_gen)
repo = LocationRepository(db)

# Test search functionality
query = LocationQuery(search="coffee", per_page=5)
locations, total = repo.get_all_with_filters(query)
print(f"Found {total} locations matching 'coffee'")

# Test distance range
distance_query = DistanceRangeQuery(
    latitude=40.7128,
    longitude=-74.0060,
    min_distance_meters=100,
    max_distance_meters=1000
)
results, total = repo.find_within_distance_range(distance_query)
print(f"Found {total} locations between 100-1000m")

db.close()
