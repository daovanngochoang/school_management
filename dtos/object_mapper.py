from datetime import datetime

from dtos import BuildingInfo, LecturerInfo, RoomInfo, ScheduleInfo, RoomReservationInfo
from models import Building, Lecturer, Room, Schedule, RoomReservation


def datetime_to_string(date_time: datetime) -> str:
    return date_time.strftime("%Y-%m-%dT%H:%M:%SZ")


def string_to_datetime(date_time: str) -> datetime:
    return datetime.strptime(date_time, "%Y-%m-%dT%H:%M:%SZ")


def to_building_info(building: Building, include_room: bool = True) -> BuildingInfo:
    rooms = None
    if include_room:
        rooms = [to_room_info(room) for room in building.rooms]

    return BuildingInfo(
        id=building.id,
        name=building.name,
        code=building.code,
        rooms=rooms,
        created_at=datetime_to_string(building.created_at),
        last_edited=datetime_to_string(building.last_edited)
    )


def to_lecturer_info(
        lecturer: Lecturer,
        include_schedules: bool = True,
        include_reservation: bool = True
) -> LecturerInfo:
    schedule = None
    if include_schedules:
        schedule = [to_schedule_info(sch) for sch in lecturer.schedules]

    reservations = None
    if include_reservation:
        reservations = [to_room_reservation(re, include_lecturer=False, include_room=False) for
                        re in lecturer.reservations]

    return LecturerInfo(
        id=lecturer.id,
        username=lecturer.username,
        first_name=lecturer.first_name,
        last_name=lecturer.last_name,
        email=lecturer.email,
        dob=datetime_to_string(lecturer.dob),
        gender=lecturer.gender,
        enabled=lecturer.enabled,
        active=lecturer.active,
        faculty=lecturer.faculty,
        schedules=schedule,
        created_at=datetime_to_string(lecturer.created_at),
        last_edited=datetime_to_string(lecturer.last_edited),
        reservations=reservations
    )


def to_room_info(
        room: Room,
        include_reservation: bool = True,
        include_building: bool = True
) -> RoomInfo:
    room_building = None
    if include_building:
        room_building = to_building_info(room.building, include_room=False)

    reservation = None
    if include_reservation:
        reservation = [to_room_reservation(res, include_room=False) for res in room.reservations]

    return RoomInfo(
        id=room.id,
        name=room.name,
        code=room.code,
        building=room_building,
        capacity=room.capacity,
        reservations=reservation,
    )


def to_schedule_info(
        sch: Schedule,
        include_lecturer: bool = True,
        include_reservations: bool = True,
) -> ScheduleInfo:
    lecturer = None
    reservations = None
    if include_lecturer:
        lecturer = to_lecturer_info(sch.lecturer, include_schedules=False)
    if reservations:
        reservations = [to_room_reservation(res) for res in sch.reservations]

    return ScheduleInfo(
        id=sch.id,
        lecturer=lecturer,
        course=sch.course,
        start_block=sch.start_block,
        end_block=sch.end_block,
        created_at=datetime_to_string(sch.created_at),
        last_edited=datetime_to_string(sch.last_edited),
        reservations=reservations
    )


def to_room_reservation(
        reservation: RoomReservation,
        include_room: bool = True,
        include_lecturer: bool = True,
        include_schedule: bool = True,
) -> RoomReservationInfo:
    room = None
    lecturer = None
    schedule = None

    if include_room:
        room = to_room_info(reservation.room, include_reservation=False)
    if include_lecturer:
        lecturer = to_lecturer_info(reservation.lecturer, include_reservation=False, include_schedules=False)
    if include_schedule:
        schedule = to_schedule_info(reservation.schedule, include_lecturer=False, include_reservations=False)
    return RoomReservationInfo(
        id=reservation.id,
        schedule=schedule,
        room=room,
        lecturer=lecturer,
        date=datetime_to_string(date_time=reservation.date),
        start_block=reservation.start_block,
        end_block=reservation.end_block,
        created_at=datetime_to_string(reservation.created_at),
        last_edited=datetime_to_string(reservation.last_edited),
    )
