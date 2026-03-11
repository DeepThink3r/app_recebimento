from pydantic import BaseModel
from typing import Optional


class StatusSchemaBase(BaseModel):
    id: int
    status: str

    class Config:
        from_attributes = True

class StatusSchemaCreate(BaseModel):
    status: str

class StatusSchemaUpdate(BaseModel):
    status: Optional[str] = None