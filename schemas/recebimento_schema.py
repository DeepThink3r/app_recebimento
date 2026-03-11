from datetime import datetime, timezone

from typing import Optional
from pydantic import BaseModel, Field


class RecebimentoSchema(BaseModel):
    id_recebimento: Optional[int] = None
    nfe_num: str
    sku_id: str
    qtd_contada: int
    status_qualidade: int
    id_conferente: int
    data_registro: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        from_attributes = True


class RecebimentoSchemaCreate(BaseModel):
    nfe_num: str
    sku_id: str
    qtd_contada: int
    status_qualidade: int


class RecebimentoSchemaUpdate(BaseModel):
    sku_id: Optional[str] = None
    qtd_contada: Optional[int] = None
    status_qualidade: Optional[int] = None