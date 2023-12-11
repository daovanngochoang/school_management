import uvicorn
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from models import Building, Room, Schedule, Lecturer
from models.base import Base, engine, get_db, SessionLocal
from routes.auth import auth_router
from routes.building import building_router
from routes.lecturer import lecturer_router
from routes.room import room_router
from routes.room_reservation import room_reservation_router
from routes.schedule import schedule_router
from setting import settings
from utils.crypto import get_password_hash

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.on_event("startup")
async def init_database():
    db = SessionLocal()
    print(f"\n\nusername: lecturer\npassword: 123456\n\n")
    try:
        db.add(Lecturer(
            **{"username": "lecturer",
               "password": get_password_hash("123456"),
               "first_name": "lecturer",
               "last_name": "1",
               "email": "lecturer1@gmail.com",
               "dob": "2023-12-11T14:25:16Z",
               "gender": "MALE",
               "enabled": True,
               "active": True,
               "faculty": "COMPUTER_SCIENCE",
               }
        ))

        db.bulk_save_objects(
            objects=[
                Building(
                    id=0,
                    name="Nha K",
                    code="K"
                ),
                Building(
                    id=1,
                    name="Nha A",
                    code="A"
                ), Building(
                    id=2,
                    name="Nha B",
                    code="B"
                ), Building(
                    id=3,
                    name="Nha C",
                    code="C"
                ),
            ]
        )
        db.commit()

        db.bulk_save_objects(
            objects=[
                Schedule(
                    lecturer_id=2,
                    course="Networking",
                    start_block="BLOCK_1",
                    end_block="BLOCK_2",

                ),
                Schedule(
                    lecturer_id=2,
                    course="Distributed Systems",
                    start_block="BLOCK_1",
                    end_block="BLOCK_2",

                ),
                Schedule(
                    lecturer_id=2,
                    course="Computer Organization in C Programming language perspective.",
                    start_block="BLOCK_1",
                    end_block="BLOCK_2",
                )
            ]
        )
        db.commit()

        db.bulk_save_objects(
            objects=[
                Room(
                    name="Phong 1",
                    code="P1",
                    building_id=0,
                ),
                Room(
                    name="Phong 2",
                    code="P2",
                    building_id=0,

                ),
                Room(
                    name="Phong 3",
                    code="P3",
                    building_id=1,
                ),

                Room(
                    name="Phong 4",
                    code="P4",
                    building_id=2,
                ),
                Room(
                    name="Phong 5",
                    code="P5",
                    building_id=3
                ),
            ]
        )
        db.commit()
    except:
        pass
    db.close()

app.include_router(router=auth_router, prefix="/auth", tags=["Auth Apis"])
app.include_router(router=building_router, prefix="/building", tags=["Building Apis"])
app.include_router(router=lecturer_router, prefix="/lecturer", tags=["Lecturer Apis"])
app.include_router(router=schedule_router, prefix="/schedule", tags=["Schedule Apis"])
app.include_router(router=room_router, prefix="/room", tags=["Room Apis"])
app.include_router(router=room_reservation_router, prefix="/reservation", tags=["Reservation Apis"])

if __name__ == '__main__':
    uvicorn.run("main:app", host=settings.SERVER_HOST, port=int(settings.SERVER_PORT), reload=True)
