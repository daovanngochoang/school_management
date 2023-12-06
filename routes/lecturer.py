from fastapi import Depends
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session

from dtos import *
from models import get_db, Building

route = APIRouter()


@route.get(path="/", response_model=ResponseEntity[LecturerInfo])
async def get_lecturers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Building).offset(skip).limit(limit)


@route.post(path="/{lid}", response_model=ResponseEntity[LecturerInfo])
async def create_lecturer(lid: int, db: Session = Depends(get_db)):
    pass


@route.post(path="/", response_model=ResponseEntity[LecturerInfo])
async def create_lecturer(lecturer: LecturerAuth, db: Session = Depends(get_db)):
    pass


@route.put(path="/{lid}", response_model=ResponseEntity[LecturerInfo])
async def update_lecturer(lid: int, lecturer: LectureUpdate, db: Session = Depends(get_db)):
    pass


@route.delete(path="/{lid}", response_model=ResponseEntity[str])
async def delete_lecturer(lid: int, db: Session = Depends(get_db)):
    pass
