from datetime import datetime
from typing import Optional, List, Union

from pydantic import BaseModel

from models import Faculty, Gender


class BuildingUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None


class BuildingCreate(BaseModel):
    name: str
    code: str


class BuildingInfo(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    code: Optional[str] = None
    rooms: Optional[List["RoomInfo"]] = None
    created_at: Optional[str] = None
    last_edited: Optional[str] = None


class RoomCreate(BaseModel):
    name: str
    code: str
    building_id: int
    capacity: int


class RoomUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    building_id: Optional[int] = None
    capacity: Optional[int] = None


class RoomInfo(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    code: Optional[str] = None
    building: Optional["BuildingInfo"] = None
    capacity: Optional[int] = None
    reservations: Optional[List["RoomReservationInfo"]] = None


class RoomReservationCreate(BaseModel):
    room_id: Optional[int] = None
    schedule_id: Optional[int] = None
    lecturer_id: Optional[int] = None
    date: Optional[str] = None
    start_block: Optional[str] = None
    end_block: Optional[str] = None


class RoomReservationUpdate(BaseModel):
    room_id: Optional[int] = None
    schedule_id: Optional[int] = None
    lecturer_id: Optional[int] = None
    date: Optional[str] = None
    start_block: Optional[str] = None
    end_block: Optional[str] = None


class RoomReservationInfo(BaseModel):
    id: Optional[int] = None
    schedule: Optional['ScheduleInfo'] = None
    room: Optional["RoomInfo"] = None
    lecturer: Optional["LecturerInfo"] = None
    date: Optional[str] = None
    start_block: Optional[str] = None
    end_block: Optional[str] = None
    created_at: Optional[str] = None
    last_edited: Optional[str] = None


class LecturerInfo(BaseModel):
    id: Optional[int] = None
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    dob: Optional[str] = None
    gender: Optional[str] = None
    enabled: Optional[bool] = None
    active: Optional[bool] = None
    faculty: Optional[str] = None
    schedules: Optional[List["ScheduleInfo"]] = None
    reservations: Optional[List["RoomReservationInfo"]] = None
    created_at: Optional[str] = None
    last_edited: Optional[str] = None


class LecturerAuth(BaseModel):
    username: str
    password: str


class TokenData(BaseModel):
    username: Union[str, None] = None


class AuthToken(BaseModel):
    lecturer: LecturerInfo
    access_token: str


class LecturerCreate(BaseModel):
    username: str
    password: str
    first_name: str
    last_name: str
    email: str
    dob: str
    faculty: Faculty
    gender: Gender


class LectureUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    dob: Optional[datetime] = None
    faculty: Optional[Faculty] = None
    gender: Optional[Gender] = None


class ScheduleInfo(BaseModel):
    id: Optional[int] = None
    reservations: Optional[List["RoomReservationInfo"]] = None
    lecturer: Optional["LecturerInfo"] = None
    course: Optional[str] = None
    start_block: Optional[str] = None
    end_block: Optional[str] = None
    created_at: Optional[str] = None
    last_edited: Optional[str] = None


class ScheduleCreate(BaseModel):
    lecturer_id: int
    course: str
    start_block: str
    end_block: str


class ScheduleUpdate(BaseModel):
    lecturer_id: Optional[int] = None
    course: Optional[str] = None
    start_block: Optional[str] = None
    end_block: Optional[str] = None
