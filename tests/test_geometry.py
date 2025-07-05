from app.core.geometry import *

# Test coordinate conversions
point = latlong_to_point(40.7128, -74.0060)  # NYC
print(f"Point: {point}")
print(f"Back to lat/lng: {point_to_latlong(point)}")

# Test GeoJSON
geojson = point_to_geojson(point)
print(f"GeoJSON: {geojson}")
back_to_point = geojson_to_point(geojson)
print(f"Back to point: {back_to_point}")

# Test WKT
wkt_str = point_to_wkt(point)
print(f"WKT: {wkt_str}")

# Test validation
print(f"Valid GeoJSON: {validate_geojson_point(geojson)}")
print(f"Invalid GeoJSON: {validate_geojson_point({'type': 'LineString'})}")
