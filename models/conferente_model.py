from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from core.configs import settings


class ConferenteModel(settings.DBBaseModel):
    __tablename__ = 'conferente'

    id = Column(Integer, primary_key=True)
    nome = Column(String(50), nullable=False)
    sobrenome = Column(String(100), nullable=False)
    eh_admin = Column(Boolean, default=False)