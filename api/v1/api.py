from fastapi import APIRouter

from api.v1.endpoints import recebimento


api_router = APIRouter()

api_router.include_router(recebimento.router, prefix='/recebimento', tags=['Recebimento'])