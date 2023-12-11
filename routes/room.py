from fastapi import Depends
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session

from dtos import *
from dtos.object_mapper import to_room_info
from models import get_db
from models.models import Room
from utils.utils import exception_to_string, error_response, success_response

room_router = APIRouter()


@room_router.get(path="/", response_model=ResponseEntity[List[RoomInfo]])
async def get_rooms(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        room = db.query(Room).offset(skip).limit(limit).all()
        return success_response(200, [to_room_info(b) for b in room])
    except Exception as ex:
        return error_response(500, exception_to_string(ex))


@room_router.get(path="/{room_id}", response_model=ResponseEntity[List[RoomInfo]])
async def get_room_by_id(room_id: int, db: Session = Depends(get_db)):
    try:
        room = db.query(Room).filter(Room.id == room_id).first()
        if room is None:
            return error_response(404, "Room Not Found")
        return success_response(200, to_room_info(room))

    except Exception as ex:
        return error_response(500, exception_to_string(ex))


@room_router.post(path="/", response_model=ResponseEntity[RoomInfo])
async def create_room(room: RoomCreate, db: Session = Depends(get_db)):
    try:
        new_room = Room(**room.model_dump())
        db.add(new_room)
        db.commit()
        db.refresh(new_room)
        return success_response(201, to_room_info(new_room))
    except Exception as ex:
        return error_response(500, exception_to_string(ex))


@room_router.put(path="/{room_id}", response_model=ResponseEntity[RoomInfo])
async def update_room(room_id: int, room: RoomUpdate, db: Session = Depends(get_db)):
    try:
        existing_room: Optional[Room] = db.query(Room).filter(Room.id == room_id).first()
        if existing_room is None:
            return error_response(404, "Room Not Found")

        existing_room.name = room.name if room.name is not None else existing_room.name
        existing_room.code = room.code if room.code is not None else existing_room.code

        db.commit()
        db.refresh(existing_room)
        return success_response(200, to_room_info(existing_room))

    except Exception as ex:
        return error_response(500, exception_to_string(ex))


@room_router.delete(path="/{room_id}", response_model=ResponseEntity[str])
async def delete_room(room_id: int, db: Session = Depends(get_db)):
    try:
        room = db.query(Room).filter(Room.id == room_id).first()
        if room is not None:
            db.delete(room)
            db.commit()
            return success_response(200, "Success")

        else:
            return error_response(404, msg="Room not found!")
    except Exception as ex:
        return error_response(500, exception_to_string(ex))
