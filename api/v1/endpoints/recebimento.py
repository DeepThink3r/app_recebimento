from typing import List

from fastapi import APIRouter, status, Depends, HTTPException, Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.recebimento_model import RecebimentoModel
from schemas.recebimento_schema import RecebimentoSchema, RecebimentoSchemaUpdate
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

#GET RECEBIMENTOS
@router.get('/', response_model=List[RecebimentoSchema])
async def get_recebimentos(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(RecebimentoModel)
        result = await session.execute(query)
        recebimentos: List[RecebimentoModel] = result.scalars().unique().all()

        return recebimentos


#GET RECEBIMENTO
@router.get('/{id_recebimento}', status_code=status.HTTP_200_OK, response_model=RecebimentoSchema)
async def get_recebimento(id_recebimento: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(RecebimentoModel).where(RecebimentoModel.id_recebimento == id_recebimento)
        result = await session.execute(query)
        recebimento: RecebimentoModel = result.scalars().unique().one_or_none()

        if recebimento:
            return recebimento
        else:
            raise HTTPException(detail='Recebimento não encontrado', status_code=status.HTTP_404_NOT_FOUND)
        
        
#PATCH RECEBIMENTO
@router.patch('/{id_recebimento}', status_code=status.HTTP_200_OK, response_model=RecebimentoSchema)
async def patch_recebimento(id_recebimento: int, recebimento: RecebimentoSchemaUpdate, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(RecebimentoModel).where(RecebimentoModel.id_recebimento == id_recebimento)
        result = await session.execute(query)
        recebimento_up: RecebimentoModel = result.scalars().unique().one_or_none()

        if not recebimento_up:
            raise HTTPException(detail='Recebimento não encontrado', status_code=status.HTTP_404_NOT_FOUND)
        
        update_recebimento = recebimento.model_dump(exclude_unset=True)
        for key, value in update_recebimento.items():
            setattr(recebimento_up, key, value)
        
        await session.commit()
        await session.refresh(recebimento_up)

        return recebimento_up
    

#DELETE RECEBIMENTO
@router.delete('/{id_recebimento}', status_code=status.HTTP_204_NO_CONTENT)
async def del_recebimento(id_recebimento: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(RecebimentoModel).where(RecebimentoModel.id_recebimento == id_recebimento)
        result = await session.execute(query)
        recebimento_del: RecebimentoModel = result.scalars().unique().one_or_none()

        if not recebimento_del:
            raise HTTPException(detail='Recebimento não encontrado', status_code=status.HTTP_404_NOT_FOUND)
        
        await session.delete(recebimento_del)
        await session.commit()

        return None
        
        