from __future__ import annotations

from typing import Generic, TypeVar, Optional

from pydantic import BaseModel

T = TypeVar("T")


class ResponseEntity(BaseModel, Generic[T]):
    status: bool
    error_message: Optional[str]
    data: T
