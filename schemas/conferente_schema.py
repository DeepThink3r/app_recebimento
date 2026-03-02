from pydantic import BaseModel


class ConferenteSchema(BaseModel):
    id: int
    nome: str
    sobrenome: str
    senha: str
    eh_admin: bool


    class Config:
        from_attributes = True
