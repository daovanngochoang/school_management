from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import and_
from sqlalchemy.orm import Session

from dtos import ResponseEntity, EquipmentBorrowingInfo, EquipmentBorrowingCreate
from dtos.object_mapper import to_equipment_borrowing_info
from models import get_db, EquipmentBorrowing
from utils import success_response, error_response, exception_to_string

equipment_borrowing_router = APIRouter()


@equipment_borrowing_router.post(
    path="/",
    response_model=ResponseEntity[EquipmentBorrowingInfo]
)
async def request_equipment(e_req: EquipmentBorrowingCreate, db: Session = Depends(get_db)):
    try:
        new_request = EquipmentBorrowing(
            **e_req.model_dump()
        )
        db.add(new_request)
        db.commit()
        db.refresh(new_request)
        return success_response(201, to_equipment_borrowing_info(new_request))

    except Exception as ex:
        return error_response(500, exception_to_string(ex))


@equipment_borrowing_router.get(
    path="/",
    response_model=ResponseEntity[List[EquipmentBorrowingInfo]]
)
async def get_borrowed_equipments(db: Session = Depends(get_db)):
    try:
        bes = db.query(EquipmentBorrowing).all()
        return success_response(200, [to_equipment_borrowing_info(be) for be in bes])
    except Exception as ex:
        return error_response(500, exception_to_string(ex))


@equipment_borrowing_router.get(
    path="/lecturer/{lecturer_id}",
    response_model=ResponseEntity[List[EquipmentBorrowingInfo]]
)
async def get_borrowed_equipment_by_lecturer(lecturer_id: int, db: Session = Depends(get_db)):
    try:
        bes = db.query(EquipmentBorrowing).filter(EquipmentBorrowing.lecturer_id == lecturer_id)
        return success_response(200, [to_equipment_borrowing_info(be) for be in bes])
    except Exception as ex:
        return error_response(500, exception_to_string(ex))


@equipment_borrowing_router.get(
    path="/equipment/{equipment_id}}",
    response_model=ResponseEntity[List[EquipmentBorrowingInfo]]
)
async def get_borrowed_equipment_by_equipment(equipment_id: int, db: Session = Depends(get_db)):
    try:
        bes = db.query(EquipmentBorrowing).filter(EquipmentBorrowing.equipment_id == equipment_id)
        return success_response(200, [to_equipment_borrowing_info(be) for be in bes])
    except Exception as ex:
        return error_response(500, exception_to_string(ex))


@equipment_borrowing_router.get(
    path="/equipment/{equipment_id}/lecturer/{equipment_id}}",
    response_model=ResponseEntity[List[EquipmentBorrowingInfo]]
)
async def get_borrowed_equipment_by_lecturer_n_equipment(
        equipment_id: int,
        lecturer_id: int,
        db: Session = Depends(get_db),
):
    try:
        bes = db.query(EquipmentBorrowing).filter(
            and_(EquipmentBorrowing.equipment_id == equipment_id, EquipmentBorrowing.lecturer_id == lecturer_id))
        return success_response(200, [to_equipment_borrowing_info(be) for be in bes])
    except Exception as ex:
        return error_response(500, exception_to_string(ex))


@equipment_borrowing_router.put(
    path="/{borrowed_equipment_id}",
    response_model=ResponseEntity[EquipmentBorrowingInfo]
)
async def update_equipment(
        borrowed_equipment_id: int,
        db: Session = Depends(get_db),
):
    try:
        be = db.query(EquipmentBorrowing).filter(EquipmentBorrowing.id == borrowed_equipment_id)
        if be is None:
            return error_response(404, "Borrowed Equipment is Not Found")
        return success_response(200, to_equipment_borrowing_info(be))
    except Exception as ex:
        return error_response(500, exception_to_string(ex))


@equipment_borrowing_router.delete(
    path="/{borrowed_equipment_id}",
    response_model=ResponseEntity[str]
)
async def delete_equipment_request(
        borrowed_equipment_id: int,
        db: Session = Depends(get_db),
):
    try:
        be = db.query(EquipmentBorrowing).filter(EquipmentBorrowing.id == borrowed_equipment_id)
        db.delete(be)
        db.commit()
        return success_response(200, "Success!")

    except Exception as ex:
        return error_response(500, exception_to_string(ex))
