from datetime import datetime

from dtos import BuildingInfo, EquipmentInfo, EquipmentBorrowingInfo
from models import Building, Equipment, EquipmentBorrowing


def datetime_to_string(date_time: datetime) -> str:
    return date_time.strftime("%m/%d/%Y, %H:%M:%S")


def to_building_info(building: Building) -> BuildingInfo:
    return BuildingInfo(
        id=building.id,
        name=building.name,
        code=building.code,
        rooms=building.rooms,
        create_at=datetime_to_string(building.created_at),
        last_edited=datetime_to_string(building.last_edited),
    )


def to_equipment_info(equipment: Equipment) -> EquipmentInfo:
    return EquipmentInfo(
        id=equipment.id,
        name=equipment.name,
        total_quantity=equipment.total_quantity,
        broken_quantity=equipment.broken_quantity,
        code=equipment.code,
        borrowed_equipments=[to_equipment_borrowing_info(eq) for eq in equipment.borrowed_equipments],
        create_at=datetime_to_string(equipment.created_at),
        last_edited=datetime_to_string(equipment.last_edited)
    )


def to_equipment_borrowing_info(eb: EquipmentBorrowing) -> EquipmentBorrowingInfo:
    return EquipmentBorrowingInfo(
        id=eb.id,
        lecturer=eb.lecturer,
        equipment=[to_equipment_borrowing_info(eq) for eq in eb.equipment],
        start=datetime_to_string(eb.start),
        end=datetime_to_string(eb.end),
        create_at=datetime_to_string(eb.created_at),
        last_edited=datetime_to_string(eb.last_edited)
    )
