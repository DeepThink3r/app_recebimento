from fastapi import APIRouter

from api.v1.endpoints import recebimento, conferente


api_router = APIRouter()

api_router.include_router(recebimento.router, prefix='/recebimento', tags=['Recebimento'])
api_router.include_router(conferente.router, prefix='/conferente', tags=['Conferente'])
