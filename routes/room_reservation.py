from fastapi import Depends
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session
from sqlalchemy.sql.operators import or_, and_

from dtos import *
from dtos.object_mapper import to_room_reservation, string_to_datetime
from models import get_db
from models.models import Room, RoomReservation, Schedule, Lecturer
from utils.jwt_token import get_current_user
from utils.utils import exception_to_string, error_response, success_response

room_reservation_router = APIRouter()


@room_reservation_router.get(path="/", response_model=ResponseEntity[List[RoomReservationInfo]])
async def get_reservations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        reservations = db.query(RoomReservation).offset(skip).limit(limit).all()
        return success_response(
            200,
            [to_room_reservation(reservation) for reservation in reservations]
        )

    except Exception as ex:
        return error_response(500, exception_to_string(ex))


@room_reservation_router.post(path="/", response_model=ResponseEntity[List[RoomReservationInfo]])
async def create_reservations(
        reservation_info: RoomReservationCreate,
        lecturer: Lecturer = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    try:
        schedule = None
        room = None

        if reservation_info.schedule_id is not None:
            schedule = db.query(Schedule).filter(Schedule.id == reservation_info.schedule_id).first()
            if schedule is None:
                return error_response(
                    404,
                    "Schedule is not found!"
                )
        if reservation_info.lecturer_id is not None:
            lecturer = db.query(Lecturer).filter(Lecturer.id == reservation_info.lecturer_id).first()
            if lecturer is None:
                return error_response(
                    404,
                    "Lecturer is not found!"
                )
        if reservation_info.room_id is not None:
            room = db.query(Room).filter(Room.id == reservation_info.room_id).first()
            if room is None:
                return error_response(
                    404,
                    "Room is not found!"
                )

        reservations = db.query(RoomReservation).filter(
            RoomReservation.date == string_to_datetime(reservation_info.date),
        ).filter(
            or_(
                RoomReservation.start_block == schedule.start_block,
                RoomReservation.end_block == schedule.end_block,
            )
        ).all()

        if len(reservations) > 0:
            return error_response(
                409,
                "Room is already reserved!"
            )
        reservation_info.lecturer_id = lecturer.id
        reservation_info.start_block = schedule.start_block
        reservation_info.end_block = schedule.end_block

        print(reservation_info.model_dump())

        new_reservation = RoomReservation(**reservation_info.model_dump())

        db.add(new_reservation)
        db.commit()
        return success_response(
            201,
            to_room_reservation(new_reservation)
        )


    except Exception as ex:
        return error_response(500, exception_to_string(ex))


@room_reservation_router.put(path="/{rid}", response_model=ResponseEntity[List[RoomReservationInfo]])
async def update_reservations(
        rid: int, reservation_info: RoomReservationUpdate,
        lecturer: Lecturer = Depends(get_current_user),
        db: Session = Depends(get_db),
):
    try:
        reservation: Optional[RoomReservation] = db.query(RoomReservation).filter(RoomReservation.id == rid).first()
        if reservation is None:
            return error_response(
                404,
                "Reservation is not found!"
            )

        reservation.lecturer_id = reservation_info.lecturer_id if reservation_info.lecturer_id is not None else reservation.lecturer_id
        reservation.schedule_id = reservation_info.schedule_id if reservation_info.schedule_id is not None else reservation.schedule_id
        reservation.room_id = reservation_info.room_id if reservation_info.room_id is not None else reservation.room_id
        reservation.date = reservation_info.date if reservation_info.date is not None else reservation.date
        reservation.start_block = reservation_info.start_block if reservation_info.start_block is not None else reservation.start_block
        reservation.end_block = reservation_info.end_block if reservation_info.end_block is not None else reservation.end_block

        db.commit()
        db.refresh(reservation)
        return success_response(
            200,
            to_room_reservation(reservation)
        )
    except Exception as ex:
        return error_response(500, exception_to_string(ex))


@room_reservation_router.delete(path="/{rid}", response_model=ResponseEntity[List[RoomReservationInfo]])
async def delete_reservations(rid: int, db: Session = Depends(get_db)):
    try:
        reservation = db.query(RoomReservation).filter(RoomReservation.id == rid).first()
        if reservation is not None:
            db.delete(reservation)
            db.commit()

    except Exception as ex:
        return error_response(500, exception_to_string(ex))
