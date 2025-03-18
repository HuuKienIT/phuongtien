from typing import TypeVar, Generic, Optional, Dict, Any
from pydantic import BaseModel

T = TypeVar("T")

class ApiResponse(BaseModel, Generic[T]):
    status: int
    message: str
    data: Optional[T] = None
    meta: Optional[Dict[str, Any]] = None

    class Config:
        arbitrary_types_allowed = True
