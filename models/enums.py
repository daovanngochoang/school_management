import enum

from sqlalchemy import Enum


class Gender(enum.Enum):
    male: str = "MALE"
    female: str = "FEMALE"


class Faculty(enum.Enum):
    computer_science: str = "COMPUTER_SCIENCE"
    language: str = "LANGUAGE"
    economic: str = "FACULTY OF ECONOMIC"


class TimeBlock(enum.Enum):
    block1: str = "BLOCK_1"
    block2: str = "BLOCK_2"
    block3: str = "BLOCK_3"
    block4: str = "BLOCK_4"
    block5: str = "BLOCK_5"
    block6: str = "BLOCK_6"
    block7: str = "BLOCK_7"
    block8: str = "BLOCK_8"
    block9: str = "BLOCK_9"
    block10: str = "BLOCK_10"
