from fastapi import Depends
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session

from dtos import *
from dtos.object_mapper import to_schedule_info
from models import get_db, Schedule, Lecturer
from utils.utils import error_response, exception_to_string, success_response

schedule_router = APIRouter()


@schedule_router.get(path="/", response_model=ResponseEntity[ScheduleInfo])
async def get_schedules(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        schedules = db.query(Schedule).offset(skip).limit(limit).all()
        return success_response(
            200,
            [to_schedule_info(data) for data in schedules]
        )
    except Exception as ex:
        return error_response(500, exception_to_string(ex))


@schedule_router.get(path="/{sche_id}", response_model=ResponseEntity[ScheduleInfo])
async def get_schedule_by_id(sche_id: int, db: Session = Depends(get_db)):
    try:
        schedule = db.query(Schedule).filter(Schedule.id == sche_id).first()
        if schedule is not None:
            return error_response(
                404,
                "Schedule is not found"
            )
        return success_response(
            200,
            to_schedule_info(schedule)
        )
    except Exception as ex:
        return error_response(500, exception_to_string(ex))


@schedule_router.post(path="/", response_model=ResponseEntity[ScheduleInfo])
async def create_schedule(schedule: ScheduleCreate, db: Session = Depends(get_db)):
    try:

        lecturer = db.query(Lecturer).filter(Lecturer.id == schedule.lecturer_id).first()
        if lecturer is None:
            return error_response(
                404,
                "Lecturer is not existed!"
            )

        schedule = Schedule(**schedule.model_dump())
        db.add(schedule)
        db.commit()
        db.refresh(schedule)
        return success_response(
            200,
            to_schedule_info(schedule)
        )
    except Exception as ex:
        return error_response(500, exception_to_string(ex))


@schedule_router.put(path="/{sche_id}", response_model=ResponseEntity[ScheduleInfo])
async def update_schedule(sche_id: int, schedule_update: ScheduleUpdate, db: Session = Depends(get_db)):
    try:
        sche: Optional[Schedule] = db.query(Schedule).filter(Schedule.id == sche_id).first()
        if sche is None:
            return error_response(
                404,
                "Schedule is not found!"
            )

        sche.start_block = schedule_update.start_block if schedule_update.start_block is not None else sche.start_block
        sche.end_block = schedule_update.end_block if schedule_update.end_block is not None else sche.end_block
        sche.lecturer_id = schedule_update.lecturer_id if schedule_update.lecturer_id is not None else sche.lecturer_id
        sche.course = schedule_update.course if schedule_update.course is not None else sche.course

        db.commit()
        db.refresh(sche)

        return success_response(
            200,
            to_schedule_info(sche)
        )
    except Exception as ex:
        return error_response(500, exception_to_string(ex))


@schedule_router.delete(path="/{sche_id}", response_model=ResponseEntity[str])
async def delete_schedule(sche_id: int, db: Session = Depends(get_db)):
    try:
        sche: Optional[Schedule] = db.query(Schedule).filter(Schedule.id == sche_id).first()
        if sche is not None:
            db.delete(sche)
            db.commit()
        return success_response(
            200,
            "Success!"
        )

    except Exception as ex:
        return error_response(500, exception_to_string(ex))
