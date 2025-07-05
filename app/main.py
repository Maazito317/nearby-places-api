from fastapi import FastAPI
from app.routers import locations

app = FastAPI(title="Nearby Places API", version="1.0.0")

app.include_router(locations.router)


@app.get("/")
def root():
    return {"message": "Nearby Places API"}
