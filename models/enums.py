import enum

from sqlalchemy import Enum


class Gender(enum.Enum):
    male: str = "MALE"
    female: str = "FEMALE"


class Faculty(enum.Enum):
    computer_science: str = "COMPUTER_SCIENCE"
    language: str = "LANGUAGE"
    economic: str = "FACULTY OF ECONOMIC"


class BorrowingStatus(enum.Enum):
    received: str = "RECEIVED"
    in_review: str = "IN_REVIEW"
    success: str = "SUCCESS"
    failure: str = "FAILURE"
    returned: str = "RETURNED"
