from typing import List, Optional, Any

from fastapi import APIRouter, status, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

import sqlalchemy
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.conferente_model import ConferenteModel
from schemas.conferente_schema import ConferenteSchemaCreate, ConferenteSchemaRecebimento, ConferenteSchemaUpdate, ConferenteShemaBase
from core.deps import get_session, get_current_user
from core.security import gerar_hash_senha
from core.auth import autenticar, criar_token_acesso


router = APIRouter()


#GET Logado
@router.get('/logado', response_model=ConferenteShemaBase)
async def get_logado(conferente_logado: ConferenteModel = Depends(get_current_user)):
    return conferente_logado


#POST / Sign Up
@router.post('/signup', status_code=status.HTTP_201_CREATED, response_model=ConferenteShemaBase)
async def post_conferente(conferente: ConferenteSchemaCreate, db: AsyncSession = Depends(get_session)):
    novo_conferente: ConferenteModel = ConferenteModel(nome=conferente.nome, sobrenome=conferente.sobrenome, re=conferente.re, senha=gerar_hash_senha(conferente.senha), eh_admin=conferente.eh_admin)

    async with db as session:
        try:
            session.add(novo_conferente)
            await session.commit()

            return novo_conferente
        except sqlalchemy.exc.IntegrityError:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='Já existe um conferente com esse RE cadastrado')


#GET Conferentes
@router.get('/', response_model=List[ConferenteShemaBase])
async def get_conferentes(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ConferenteModel)
        result = await session.execute(query)
        conferentes: List[ConferenteModel] = result.scalars().unique().all()

        return conferentes


#GET Conferente
@router.get('/{conferente_id}', response_model=ConferenteSchemaRecebimento, status_code=status.HTTP_200_OK)
async def get_conferentes(conferente_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ConferenteModel).where(ConferenteModel.id == conferente_id)
        result = await session.execute(query)
        conferente: ConferenteModel = result.scalars().unique().one_or_none()

        if conferente:
            return conferente
        
        else:
            raise HTTPException(detail='Conferente não encontrado', status_code=status.HTTP_404_NOT_FOUND)
        

#PUT Conferente
@router.put('/{conferente_id}', response_model=ConferenteShemaBase, status_code=status.HTTP_200_OK)
async def put_conferente(conferente_id: int, conferente: ConferenteSchemaUpdate, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ConferenteModel).where(ConferenteModel.id == conferente_id)
        result = await session.execute(query)
        conferente_up: ConferenteModel = result.scalars().unique().one_or_none()

        if not conferente_up:
            raise HTTPException(detail='Conferente não encontrado', status_code=status.HTTP_404_NOT_FOUND)
        
        update_data = conferente.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            if key == 'senha':
                # Special handling for the password field
                setattr(conferente_up, key, gerar_hash_senha(value))
            else:
                # For all other fields, update directly
                setattr(conferente_up, key, value)
        
        try:
            await session.commit()
            await session.refresh(conferente_up)
            return conferente_up
        except sqlalchemy.exc.IntegrityError:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='Já existe um conferente com esse RE cadastrado')


#DELETE Conferente
@router.delete('/{conferente_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_conferente(conferente_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ConferenteModel).where(ConferenteModel.id == conferente_id)
        result = await session.execute(query)
        conferente_del: ConferenteModel = result.scalars().unique().one_or_none()

        if not conferente_del:
            raise HTTPException(detail='Conferente não encontrado', status_code=status.HTTP_404_NOT_FOUND)
        
        await session.delete(conferente_del)
        await session.commit()

        return Response(status_code=status.HTTP_204_NO_CONTENT)
    

#POST Login
@router.post('/login')
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_session)):
    usuario = await autenticar(int(form_data.username), form_data.password, db)

    if not usuario:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Dados de acesso incorretos')
    
    return JSONResponse(
        content={
            "access_token": criar_token_acesso(sub=usuario.re),
            "token_type": "bearer"
        },
        status_code=status.HTTP_200_OK
    )
