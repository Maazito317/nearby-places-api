from app.core.dependencies import get_db
from app.core.spatial import validate_coordinates, find_locations_within_distance

# Test coordinate validation
print("Valid coords:", validate_coordinates(40.7128, -74.0060))  # NYC
print("Invalid coords:", validate_coordinates(100, -200))

# Test spatial query (will be empty until we have data)
db_gen = get_db()
db = next(db_gen)
results = find_locations_within_distance(db, 40.7128, -74.0060, 1000)
print(f"Found {len(results)} locations")
db.close()
