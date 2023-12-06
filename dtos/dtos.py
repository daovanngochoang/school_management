from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel

from models import BorrowingStatus, Faculty, Gender


class BuildingUpdate(BaseModel):
    name: Optional[str]
    code: Optional[str]


class BuildingCreate(BaseModel):
    id: int
    name: str
    code: str


class BuildingInfo(BaseModel):
    id: int
    name: str
    code: str
    rooms: List["RoomInfo"]
    create_at: str
    last_edited: str


class RoomCreate(BaseModel):
    name: str
    code: str
    status: BorrowingStatus
    building_id: int
    capacity: int


class RoomUpdate(BaseModel):
    name: Optional[str]
    code: Optional[str]
    status: Optional[BorrowingStatus]
    building_id: Optional[int]
    capacity: Optional[int]


class RoomInfo(BaseModel):
    id: int
    name: str
    code: str
    status: BorrowingStatus
    buildings: List["BuildingInfo"]
    capacity: int
    schedules: List["ScheduleInfo"]


class EquipmentUpdate(BaseModel):
    name: Optional[str]
    total_quantity: Optional[int]
    broken_quantity: Optional[int]
    code: Optional[str]


class EquipmentInfo(BaseModel):
    name: Optional[str]
    total_quantity: Optional[int]
    broken_quantity: Optional[int]
    code: Optional[str]
    created_at: str
    last_edited: str
    borrowed_equipments: List


class EquipmentCreate(BaseModel):
    name: str
    total_quantity: int
    broken_quantity: int
    code: str


class EquipmentBorrowingCreate(BaseModel):
    lecturer_id: int
    equipment_id: int
    start: datetime
    end: datetime


class EquipmentBorrowingUpdate(BaseModel):
    lecturer_id: Optional[int]
    equipment_id: Optional[int]
    start: Optional[datetime]
    end: Optional[datetime]


class EquipmentBorrowingInfo(BaseModel):
    id: int
    lecturer: "LecturerInfo"
    equipment: EquipmentInfo
    start: datetime
    end: datetime
    created_at: str
    last_edited: str


class LecturerInfo(BaseModel):
    id: int
    username: str
    first_name: str
    last_name: str
    email: str
    dob: datetime
    gender: Gender
    enabled: bool
    active: bool
    faculty: Faculty
    schedules: List["ScheduleInfo"]
    created_at: datetime
    last_edited: datetime


class LecturerAuth(BaseModel):
    username: str
    password: str


class LectureUpdate(BaseModel):
    username: Optional[str]
    password: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[str]
    dob: Optional[datetime]
    faculty: Optional[Faculty]
    gender: Optional[Gender]


class ScheduleInfo(BaseModel):
    id: int
    room: List["RoomInfo"]
    lecturer: List["LecturerInfo"]
    course: str
    start: datetime
    end: datetime
    create_at: datetime
    last_edited: datetime


class ScheduleCreate(BaseModel):
    id: int
    room_id: int
    lecturer_id: int
    course: str
    start: datetime
    end: datetime


class ScheduleUpdate(BaseModel):
    room_id: Optional[int]
    lecturer_id: Optional[int]
    course: Optional[str]
    start: Optional[datetime]
    end: Optional[datetime]
