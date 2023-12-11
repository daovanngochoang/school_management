import enum
from datetime import datetime, time
from typing import List

from sqlalchemy import String, Column, ForeignKey, Integer, DateTime, Date
from sqlalchemy.orm import Mapped, relationship, mapped_column

from . import Base, Gender, Faculty, TimeBlock


class Building(Base):
    __tablename__ = "buildings"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(name="name", type_=String(200))
    code: Mapped[str] = mapped_column(name="code", type_=String(30))
    rooms: Mapped[List["Room"]] = relationship(
        back_populates="building", cascade="all, delete-orphan"
    )

    created_at: Mapped[datetime] = mapped_column(
        name="created_at", default=datetime.utcnow, nullable=False, type_=DateTime
    )
    last_edited: Mapped[datetime] = Column(
        name="last_edited", default=datetime.utcnow, nullable=False, type_=DateTime, onupdate=datetime.utcnow
    )


class Room(Base):
    __tablename__ = "rooms"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(name="name", type_=String(200))
    code: Mapped[str] = mapped_column(name="code", type_=String(30))
    capacity: Mapped[int] = mapped_column(name="capacity", type_=Integer(), default=20)
    building_id: Mapped[int] = mapped_column(ForeignKey("buildings.id"))
    building: Mapped["Building"] = relationship(back_populates="rooms")
    reservations: Mapped[List["RoomReservation"]] = relationship(
        back_populates="room",
        cascade="all, delete-orphan",
    )

    created_at: Mapped[datetime] = mapped_column(
        name="created_at", default=datetime.utcnow, nullable=False, type_=DateTime
    )
    last_edited: Mapped[datetime] = Column(
        name="last_edited", default=datetime.utcnow, nullable=False, type_=DateTime, onupdate=datetime.utcnow
    )


class RoomReservation(Base):
    __tablename__ = "room_reservations"
    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    room: Mapped["Room"] = relationship("Room", back_populates="reservations")
    schedule_id: Mapped[int] = mapped_column(ForeignKey("schedules.id"))
    schedule: Mapped["Room"] = relationship("Schedule", back_populates="reservations")
    lecturer_id: Mapped[int] = mapped_column(ForeignKey("lecturers.id"))
    lecturer: Mapped["Lecturer"] = relationship("Lecturer", back_populates="reservations")
    date: Mapped[datetime] = mapped_column(name="date", type_=DateTime)
    start_block: Mapped[enum.Enum] = Column(name="start_block", default=TimeBlock.block1, type_=String)
    end_block: Mapped[enum.Enum] = Column(name="end_block", default=TimeBlock.block1, type_=String)
    created_at: Mapped[datetime] = mapped_column(
        name="created_at", default=datetime.utcnow, nullable=False, type_=DateTime
    )
    last_edited: Mapped[datetime] = Column(
        name="last_edited", default=datetime.utcnow, nullable=False, type_=DateTime, onupdate=datetime.utcnow
    )


class Schedule(Base):
    __tablename__ = "schedules"

    reservations: Mapped[List["RoomReservation"]] = relationship(
        back_populates="schedule",
        cascade="all, delete-orphan",
    )
    id: Mapped[int] = mapped_column(primary_key=True)
    lecturer_id: Mapped[int] = mapped_column(ForeignKey("lecturers.id"), name="lecturer_id")
    lecturer: Mapped["Lecturer"] = relationship("Lecturer", back_populates="schedules")
    course: Mapped[str] = mapped_column(name="course", type_=String(200))
    start_block: Mapped[enum.Enum] = Column(name="start_block", default=TimeBlock.block1, type_=String)
    end_block: Mapped[enum.Enum] = Column(name="end_block", default=TimeBlock.block1, type_=String)
    created_at: Mapped[datetime] = mapped_column(
        name="created_at", default=datetime.utcnow, nullable=False, type_=DateTime
    )
    last_edited: Mapped[datetime] = Column(
        name="last_edited", default=datetime.utcnow, nullable=False, type_=DateTime, onupdate=datetime.utcnow
    )


class Lecturer(Base):
    __tablename__ = "lecturers"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(name="username", type_=String(200), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(name="password", nullable=False)
    first_name: Mapped[str] = mapped_column(name="first_name", type_=String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(name="last_name", type_=String(100), nullable=False)
    email: Mapped[str] = mapped_column(name="email", type_=String(200), nullable=False, unique=True)
    dob: Mapped[Date] = mapped_column(name="dob", type_=DateTime(timezone=True))
    gender: Mapped[Gender] = mapped_column(name="gender", default=Gender.male)
    enabled: Mapped[bool] = mapped_column(name="enabled", default=False, nullable=False)
    active: Mapped[bool] = mapped_column(name="active", default=False, nullable=False)
    faculty: Mapped[Faculty] = mapped_column(name="faculty", default=Faculty.computer_science, nullable=False)
    schedules: Mapped[List["Schedule"]] = relationship(back_populates="lecturer")
    reservations: Mapped[List["RoomReservation"]] = relationship(back_populates="lecturer")

    created_at: Mapped[datetime] = mapped_column(
        name="created_at", default=datetime.utcnow, nullable=False, type_=DateTime
    )
    last_edited: Mapped[datetime] = Column(
        name="last_edited", default=datetime.utcnow, nullable=False, type_=DateTime, onupdate=datetime.utcnow
    )
