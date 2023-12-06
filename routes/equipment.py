from typing import List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from dtos import EquipmentInfo, ResponseEntity, EquipmentCreate, EquipmentUpdate
from dtos.object_mapper import to_equipment_info
from models import get_db, Equipment
from utils import exception_to_string, error_response, success_response

equipment_router = APIRouter()


@equipment_router.get(path="/", response_model=ResponseEntity[List[EquipmentInfo]])
async def get_equipment(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        equipments = db.query(Equipment).offset(skip).limit(limit).all()
        return success_response(
            200,
            [to_equipment_info(e) for e in equipments])

    except Exception as ex:
        return error_response(500, exception_to_string(ex))


@equipment_router.post(path="/")
async def create_equipment(equipment: EquipmentCreate, db: Session = Depends(get_db())):
    try:
        new_equipment = Equipment(**equipment.model_dump())
        db.add(new_equipment)
        db.commit()
        db.refresh(new_equipment)
        return success_response(200, to_equipment_info(new_equipment))

    except Exception as ex:
        return error_response(500, exception_to_string(ex))


@equipment_router.put(path="/{equipment_id}")
async def update_equipment(equipment_id: str, equipment: EquipmentUpdate, db: Session = Depends(get_db())):
    try:
        updated_equipment: Optional[Equipment] = db.query(Equipment).filter(Equipment.id == equipment_id).first()
        if updated_equipment is None:
            return error_response(404, "Equipment Not Found")

        updated_equipment.name = equipment.name if equipment.name is not None else updated_equipment.name
        updated_equipment.code = equipment.code if equipment.code is not None else updated_equipment.code
        updated_equipment.total_quantity = equipment.total_quantity if equipment.total_quantity is not None else updated_equipment.total_quantity
        updated_equipment.broken_quantity = equipment.broken_quantity if equipment.broken_quantity is not None else updated_equipment.broken_quantity

        db.commit()
        db.refresh(updated_equipment)

        return success_response(200, to_equipment_info(updated_equipment))
    except Exception as ex:
        return error_response(500, exception_to_string(ex))


@equipment_router.delete(path="/{equipment_id}")
async def delete_equipment(equipment_id: str, db: Session = Depends(get_db())):
    try:
        db.delete(db.query(Equipment).filter(Equipment.id == equipment_id).first())
        return success_response(200, "Success!")

    except Exception as ex:
        return error_response(500, exception_to_string(ex))
