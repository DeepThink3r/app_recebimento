from typing import List

from fastapi import APIRouter, status, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError

from models.status_model import StatusModel
from models.conferente_model import ConferenteModel
from schemas.status_schema import StatusSchemaBase, StatusSchemaCreate, StatusSchemaUpdate
from core.deps import get_session, get_current_user

router = APIRouter()

# GET Status Todos
@router.get('/', response_model=List[StatusSchemaBase])
async def get_todos_status(db: AsyncSession = Depends(get_session)):
    query = select(StatusModel)
    result = await db.execute(query)
    status_lista: List[StatusModel] = result.scalars().unique().all()
    return status_lista

# GET Status Um
@router.get('/{status_id}', response_model=StatusSchemaBase)
async def get_status(status_id: int, db: AsyncSession = Depends(get_session)):
    query = select(StatusModel).where(StatusModel.id == status_id)
    result = await db.execute(query)
    status_obj: StatusModel = result.scalars().unique().one_or_none()

    if not status_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Status não encontrado')
    return status_obj

# POST Status
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=StatusSchemaBase)
async def post_status(status_in: StatusSchemaCreate, usuario_logado: ConferenteModel = Depends(get_current_user), db: AsyncSession = Depends(get_session)):
    novo_status: StatusModel = StatusModel(status=status_in.status)
    
    try:
        db.add(novo_status)
        await db.commit()
        await db.refresh(novo_status)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='Status já existente')
    
    return novo_status

# PUT Status
@router.put('/{status_id}', response_model=StatusSchemaBase)
async def put_status(status_id: int, status_up: StatusSchemaUpdate, usuario_logado: ConferenteModel = Depends(get_current_user), db: AsyncSession = Depends(get_session)):
    query = select(StatusModel).where(StatusModel.id == status_id)
    result = await db.execute(query)
    status_existente: StatusModel = result.scalars().unique().one_or_none()

    if not status_existente:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Status não encontrado')
    
    if status_up.status:
        status_existente.status = status_up.status
        
    try:
        await db.commit()
        await db.refresh(status_existente)
        return status_existente
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='Status já existente')

# DELETE Status
@router.delete('/{status_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_status(status_id: int, usuario_logado: ConferenteModel = Depends(get_current_user), db: AsyncSession = Depends(get_session)):
    query = select(StatusModel).where(StatusModel.id == status_id)
    result = await db.execute(query)
    status_del: StatusModel = result.scalars().unique().one_or_none()

    if not status_del:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Status não encontrado')
    
    await db.delete(status_del)
    await db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)