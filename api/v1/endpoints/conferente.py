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


#GET USUARIO
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
        
        