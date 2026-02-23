from datetime import datetime, timezone

from typing import Optional
from pydantic import BaseModel, Field


class RecebimentoSchema(BaseModel):
    id_recebimento: Optional[int] = None
    nfe_num: str
    sku_id: str
    qtd_contada: int
    status_qualidade: str
    id_conferente: int
    data_registro: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class Config:
    from_attributes = True



    nfe_num: str