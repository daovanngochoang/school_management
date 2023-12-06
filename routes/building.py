from fastapi import Depends
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session

from dtos import *
from dtos.object_mapper import to_building_info
from models import get_db
from models.models import Building
from utils import exception_to_string, error_response, success_response

building_router = APIRouter()


@building_router.get(path="/", response_model=ResponseEntity[List[BuildingInfo]])
async def get_buildings(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        building = db.query(Building).offset(skip).limit(limit).all()
        return success_response(200, [to_building_info(b) for b in building])

    except Exception as ex:
        return error_response(500, exception_to_string(ex))


@building_router.get(path="/{building_id}", response_model=ResponseEntity[List[BuildingInfo]])
async def get_building_by_id(building_id: int, db: Session = Depends(get_db)):
    try:
        building = db.query(Building).filter(Building.id == building_id).first()
        if building is None:
            return error_response(404, "Building Not Found")

        return success_response(200, to_building_info(building))

    except Exception as ex:
        return error_response(500, exception_to_string(ex))


@building_router.post(path="/", response_model=ResponseEntity[BuildingInfo])
async def create_building(building: BuildingCreate, db: Session = Depends(get_db)):
    try:
        new_building = Building(name=building.name, code=building.code)
        db.add(new_building)
        db.commit()
        db.refresh(new_building)
        return success_response(201, to_building_info(new_building))
    except Exception as ex:
        return error_response(500, exception_to_string(ex))


@building_router.put(path="/{building_id}", response_model=ResponseEntity[BuildingInfo])
async def update_building(building_id: int, building: BuildingUpdate, db: Session = Depends(get_db)):
    try:
        existing_building: Optional[Building] = db.query(Building).filter(Building.id == building_id).first()
        if existing_building is None:
            return error_response(404, "Building Not Found")

        existing_building.name = building.name if building.name is not None else existing_building.name
        existing_building.code = building.code if building.code is not None else existing_building.code

        db.commit()
        db.refresh(existing_building)
        return success_response(200, to_building_info(existing_building))

    except Exception as ex:
        return error_response(500, exception_to_string(ex))


@building_router.delete(path="/{building_id}", response_model=ResponseEntity[str])
async def delete_building(building_id: int, db: Session = Depends(get_db)):
    try:
        building = db.query(Building).filter(Building.id == building_id).first()
        if building is not None:
            db.delete(building)
            db.commit()
            return success_response(200, "Success")

        else:
            return error_response(404, msg="Building not found!")
    except Exception as ex:
        return error_response(500, exception_to_string(ex))
