from app.schemas.location_schemas import LocationCreate, LocationCreateGeoJSON, NearbySearchParams

# Test valid input
valid_location = LocationCreate(
    name="Test Location",
    description="A test location",
    latitude=40.7128,
    longitude=-74.0060
)
print(f"Valid location: {valid_location}")

# Test invalid coordinates
try:
    invalid_location = LocationCreate(
        name="Invalid",
        latitude=100,  # Invalid
        longitude=-74.0060
    )
except Exception as e:
    print(f"Validation error: {e}")

# Test GeoJSON input
geojson_location = LocationCreateGeoJSON(
    name="GeoJSON Location",
    point={"type": "Point", "coordinates": [-74.0060, 40.7128]}
)
print(f"GeoJSON location: {geojson_location}")

# Test search params
search = NearbySearchParams(
    latitude=40.7128,
    longitude=-74.0060,
    distance_meters=1000
)
print(f"Search params: {search}")
