from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


from core.configs import settings


class RecebimentoModel(settings.DBBaseModel):
    __tablename__ = 'recebimento'

    id_recebimento = Column(Integer, primary_key=True, autoincrement=True)
    nfe_num = Column(String(100), nullable=False)
    sku_id = Column(String(100), nullable=False)
    qtd_contada = Column(Integer, nullable=False)
    status_qualidade = Column(String(50), nullable=False)
    id_conferente = Column(Integer, ForeignKey('conferente.id'))
    data_registro = Column(
        DateTime(timezone=True), 
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        server_default=func.now()
    )
    
    