from fastapi import Depends
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session

from dtos import *
from models import get_db, Building

route = APIRouter()


@route.get(path="/", response_model=ResponseEntity[LecturerInfo])
async def get_schedules(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Building).offset(skip).limit(limit)


@route.post(path="/{sche_id}", response_model=ResponseEntity[LecturerInfo])
async def create_schedule(sche_id: int, db: Session = Depends(get_db)):
    pass


@route.post(path="/", response_model=ResponseEntity[LecturerInfo])
async def create_schedule(schedule: ScheduleCreate, db: Session = Depends(get_db)):
    pass


@route.put(path="/{sche_id}", response_model=ResponseEntity[LecturerInfo])
async def update_schedule(sche_id: int, schedule: ScheduleUpdate, db: Session = Depends(get_db)):
    pass


@route.delete(path="/{sche_id}", response_model=ResponseEntity[str])
async def delete_schedule(sche_id: int, db: Session = Depends(get_db)):
    pass
