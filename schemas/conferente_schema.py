from pydantic import BaseModel
from typing import Optional, List

from schemas.recebimento_schema import RecebimentoSchema



class ConferenteSchemaBase(BaseModel):
    id: int
    re: int
    nome: str
    sobrenome: str
    eh_admin: bool


    class Config:
        from_attributes = True

class ConferenteSchemaCreate(BaseModel):
    re: int
    nome: str
    sobrenome: str
    senha: str
    eh_admin: bool = False

class ConferenteSchemaRecebimento(ConferenteSchemaBase):
    recebimentos: Optional[List[RecebimentoSchema]]


class ConferenteSchemaUpdate(BaseModel):
    re: Optional[int] = None
    nome: Optional[str] = None
    sobrenome: Optional[str] = None
    senha: Optional[str] = None
    eh_admin: Optional[bool] = None
