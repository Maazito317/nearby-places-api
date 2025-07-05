from app.core.dependencies import get_db
from app.repositories.location_repository import LocationRepository
from app.core.geometry import latlong_to_point

# Test repository operations
db_gen = get_db()
db = next(db_gen)
repo = LocationRepository(db)

# Test create
nyc_point = latlong_to_point(40.7128, -74.0060)
location = repo.create("NYC", "New York City", nyc_point)
print(f"Created location: {location.id} - {location.name}")

# Test get_by_id
found = repo.get_by_id(location.id)
print(f"Found location: {found.name if found else 'Not found'}")

# Test count
total = repo.count_total()
print(f"Total locations: {total}")

db.close()
