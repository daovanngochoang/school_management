from datetime import datetime, time
from typing import List

from sqlalchemy import String, Column, ForeignKey, Integer, DateTime, Date
from sqlalchemy.orm import Mapped, relationship, mapped_column

from . import Base, Gender, Faculty, BorrowingStatus


class Building(Base):
    __tablename__ = "buildings"
    id: Mapped[int] = mapped_column(primary_key=True, )
    name: Mapped[str] = mapped_column(name="name", type_=String(200))
    code: Mapped[str] = mapped_column(name="code", type_=String(30))
    rooms: Mapped[List["Room"]] = relationship(
        back_populates="building", cascade="all, delete-orphan"
    )

    created_at: Mapped[datetime] = mapped_column(
        name="create_at", default=datetime.utcnow, nullable=False, type_=DateTime
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

    schedules: Mapped[List["Schedule"]] = relationship(
        back_populates="room",
        cascade="all, delete-orphan",
    )

    created_at: Mapped[datetime] = mapped_column(
        name="create_at", default=datetime.utcnow, nullable=False
    )
    last_edited: Mapped[datetime] = Column(
        name="last_edited", default=datetime.utcnow, nullable=False, type_=DateTime
    )


class Schedule(Base):
    __tablename__ = "schedules"

    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    room: Mapped["Room"] = relationship("Room", back_populates="schedules")
    lecturer_id: Mapped[int] = mapped_column(ForeignKey("lecturers.id"), name="lecturer_id")
    lecturer: Mapped["Lecturer"] = relationship("Lecturer", back_populates="schedules")
    course: Mapped[str] = mapped_column(name="course", type_=String(200))
    start: Mapped[datetime] = mapped_column(default=datetime.utcnow, nullable=False)
    end: Mapped[datetime] = mapped_column(default=datetime.utcnow, nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, nullable=False)
    last_edited: Mapped[datetime] = Column(default=datetime.utcnow, nullable=False, type_=DateTime)


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
    borrowed_equipments: Mapped[List["EquipmentBorrowing"]] = relationship(
        back_populates="lecturer",
        cascade="all, delete-orphan"
    )

    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, nullable=False)
    last_edited: Mapped[datetime] = Column(default=datetime.utcnow, nullable=False, type_=DateTime)


class Equipment(Base):
    __tablename__ = "equipments"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String())
    total_quantity: Mapped[int] = mapped_column(name="total_quantity", type_=Integer(), default=1)
    broken_quantity: Mapped[int] = mapped_column(name="broken_quantity", type_=Integer(), default=0)
    code: Mapped[str] = mapped_column(name="code", type_=String(30))
    borrowed_equipments: Mapped[List["EquipmentBorrowing"]] = relationship(
        back_populates="equipment",
        cascade="all, delete-orphan",
        uselist=True
    )
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, nullable=False)
    last_edited: Mapped[datetime] = Column(default=datetime.utcnow, nullable=False, type_=DateTime)


class EquipmentBorrowing(Base):
    __tablename__ = "equipment_borrowing"
    id: Mapped[int] = mapped_column(primary_key=True)
    lecturer_id: Mapped[int] = mapped_column(ForeignKey("lecturers.id"))
    lecturer: Mapped["Lecturer"] = relationship("Lecturer", back_populates="borrowed_equipments")
    equipment: Mapped["Equipment"] = relationship(back_populates="borrowed_equipments")
    equipment_id: Mapped[int] = mapped_column(ForeignKey("equipments.id"), name="equipment_id", type_=Integer(),
                                              nullable=False)
    start: Mapped[datetime] = mapped_column(default=datetime.utcnow, nullable=False)
    end: Mapped[datetime] = mapped_column(default=datetime.utcnow, nullable=False)
    status: Mapped[BorrowingStatus] = mapped_column(default=BorrowingStatus.received, nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, nullable=False)
    last_edited: Mapped[datetime] = Column(default=datetime.utcnow, nullable=False, type_=DateTime)
