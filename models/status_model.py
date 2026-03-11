from sqlalchemy import Column, Integer, String

from core.configs import settings


class StatusModel(settings.DBBaseModel):
    __tablename__ = 'status_conferencia'

    id = Column(Integer, primary_key=True, autoincrement=True)
    status = Column(String(50), nullable=False, unique=True)