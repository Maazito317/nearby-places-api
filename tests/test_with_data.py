# test_with_data.py
from app.core.dependencies import get_db
from app.repositories.location_repository import LocationRepository
from app.schemas.query_schemas import LocationQuery, DistanceRangeQuery
from app.core.geometry import latlong_to_point

db_gen = get_db()
db = next(db_gen)
repo = LocationRepository(db)

# Create test locations first
starbucks = repo.create("Starbucks", "Coffee shop", latlong_to_point(40.7128, -74.0060))
dunkin = repo.create("Dunkin Coffee", "Another coffee shop", latlong_to_point(40.7130, -74.0062))
restaurant = repo.create("Joe's Pizza", "Pizza place", latlong_to_point(40.7125, -74.0058))

print(f"Created 3 locations")

# Now test search
query = LocationQuery(search="coffee", per_page=5)
locations, total = repo.get_all_with_filters(query)
print(f"Found {total} locations matching 'coffee'")

# Test distance range
distance_query = DistanceRangeQuery(
    latitude=40.7128,
    longitude=-74.0060,
    min_distance_meters=0,  # Changed to 0 to catch nearby locations
    max_distance_meters=1000
)
results, total = repo.find_within_distance_range(distance_query)
print(f"Found {total} locations between 0-1000m")

db.close()
