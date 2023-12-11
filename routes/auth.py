from fastapi import APIRouter
from fastapi.security import OAuth2PasswordRequestForm

from dtos import LecturerCreate, ResponseEntity, AuthToken, LecturerInfo
from dtos.object_mapper import to_lecturer_info
from utils.crypto import get_password_hash, verify_password
from utils.jwt_token import *
from utils.utils import error_response, exception_to_string, success_response

auth_router = APIRouter()


@auth_router.post(path="/token", response_model=dict)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # try:
        lecturer: Optional[Lecturer] = db.query(Lecturer).filter(Lecturer.username == form_data.username).first()
        if lecturer is None:
            return error_response(
                400,
                msg="Incorrect email or password"
            )

        hashed_pass = lecturer.password
        if not verify_password(form_data.password, hashed_pass):
            return error_response(
                400,
                msg="Incorrect email or password"
            )

        return {
            "token_type": "bearer",
            "lecturer": to_lecturer_info(lecturer=lecturer, include_reservation=False),
            "access_token": create_access_token(
                data={"sub": lecturer.username},
                expires_delta=timedelta(minutes=setting.settings.ACCESS_TOKEN_EXPIRE_MINUTES),
            )
        }

    # except Exception as ex:
    #     return error_response(500, exception_to_string(ex))


@auth_router.post("/register", response_model=ResponseEntity[LecturerInfo])
async def register(lecturer_info: LecturerCreate, db: Session = Depends(get_db)):
    try:

        lecturer = db.query(Lecturer).filter(Lecturer.username == lecturer_info.username).first()
        if lecturer is not None:
            return error_response(
                409,
                "User with this username is existed!"
            )

        hashed_password = get_password_hash(lecturer_info.password)
        lecturer_info.password = hashed_password
        new_lecturer = Lecturer(**lecturer_info.model_dump())
        db.add(new_lecturer)
        db.commit()
        db.refresh(new_lecturer)

        return success_response(
            201,
            to_lecturer_info(new_lecturer)
        )
    except Exception as ex:
        return error_response(500, exception_to_string(ex))
