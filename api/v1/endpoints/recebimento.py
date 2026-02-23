from typing import List

from fastapi import APIRouter, status, Depends, HTTPException, Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.recebimento_model import RecebimentoModel
from schemas.recebimento_schema import RecebimentoSchema
from core.deps import get_session


router = APIRouter()


#POST NFE
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=RecebimentoSchema)
async def post_recebimento(recebimento: RecebimentoSchema, db: AsyncSession = Depends(get_session)):
    novo_recebimento: RecebimentoModel = RecebimentoModel(
        nfe_num=recebimento.nfe_num,
        sku_id=recebimento.sku_id,
        qtd_contada=recebimento.qtd_contada,
        status_qualidade=recebimento.status_qualidade,
        id_conferente=recebimento.id_conferente
    )

    db.add(novo_recebimento)
    await db.commit()

    return novo_recebimento