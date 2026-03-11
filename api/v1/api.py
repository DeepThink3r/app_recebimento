from fastapi import APIRouter

from api.v1.endpoints import recebimento, conferente, status


api_router = APIRouter()

api_router.include_router(recebimento.router, prefix='/recebimento', tags=['Recebimento'])
api_router.include_router(conferente.router, prefix='/conferente', tags=['Conferente'])
api_router.include_router(status.router, prefix='/status', tags=['Status Conferência'])
