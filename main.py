from fastapi import FastAPI

from models.base import Base, engine
from routes.building import building_router

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(router=building_router, prefix="/building")
