from fastapi import Depends
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session

from dtos import *
from dtos.object_mapper import to_lecturer_info
from models import get_db, Lecturer
from utils.utils import success_response, error_response, exception_to_string

lecturer_router = APIRouter()


@lecturer_router.get(path="/", response_model=ResponseEntity[LecturerInfo])
async def get_lecturers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        lecturers = db.query(Lecturer).offset(skip).limit(limit).all()
        return success_response(
            200,
            [to_lecturer_info(lecturer) for lecturer in lecturers]
        )
    except Exception as ex:
        return error_response(500, exception_to_string(ex))


@lecturer_router.get(path="/{lid}", response_model=ResponseEntity[LecturerInfo])
async def get_lecturer_by_id(lid: int, db: Session = Depends(get_db)):
    try:
        lecturer = db.query(Lecturer).filter(Lecturer.id == lid).first()
        return success_response(
            200,
            to_lecturer_info(lecturer)
        )
    except Exception as ex:
        return error_response(500, exception_to_string(ex))


@lecturer_router.put(path="/{lid}", response_model=ResponseEntity[LecturerInfo])
async def update_lecturer(lid: int, lecturerInfo: LectureUpdate, db: Session = Depends(get_db)):
    try:
        lecturer = db.query(Lecturer).filter(Lecturer.id == lid).first()
        if lecturer is None:
            return error_response(404, "Lecturer not found!")

        lecturer.dob = lecturerInfo.dob if lecturerInfo.dob is not None else lecturer.dob
        lecturer.first_name = lecturerInfo.first_name if lecturerInfo.first_name is not None else lecturer.first_name
        lecturer.last_name = lecturerInfo.last_name if lecturerInfo.last_name is not None else lecturer.last_name
        lecturer.username = lecturerInfo.username if lecturerInfo.username is not None else lecturer.username
        lecturer.password = lecturerInfo.password if lecturerInfo.password is not None else lecturer.password
        lecturer.email = lecturerInfo.email if lecturerInfo.email is not None else lecturer.email
        lecturer.faculty = lecturerInfo.faculty if lecturerInfo.faculty is not None else lecturer.faculty
        lecturer.gender = lecturerInfo.gender if lecturerInfo.gender is not None else lecturer.gender

        db.commit()
        db.refresh(lecturer)

        return success_response(
            200,
            to_lecturer_info(lecturer)
        )
    except Exception as ex:
        return error_response(500, exception_to_string(ex))


@lecturer_router.delete(path="/{lid}", response_model=ResponseEntity[str])
async def delete_lecturer(lid: int, db: Session = Depends(get_db)):
    try:
        lec = db.query(Lecturer).filter(Lecturer.id == lid).first()
        db.delete(lec)
        db.commit()
        return success_response(200, "Success!")
    except Exception as ex:
        return error_response(500, exception_to_string(ex))
