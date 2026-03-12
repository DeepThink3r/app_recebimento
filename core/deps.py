from typing import AsyncGenerator
from fastapi import Depends, HTTPException, status
import jwt

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel

from core.database import Session
from core.auth import oauth2_schema
from core.configs import settings
from models.conferente_model import ConferenteModel



class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


async def get_session() -> AsyncGenerator:
    session: AsyncSession = Session()

    try:
        yield session
    finally:
        await session.close()


async def get_current_user(
    token: str = Depends(oauth2_schema),
    db: AsyncSession = Depends(get_session)
) -> ConferenteModel:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except jwt.PyJWTError:
        raise credentials_exception
    
    query = select(ConferenteModel).where(ConferenteModel.re == int(token_data.username))
    result = await db.execute(query)
    usuario: ConferenteModel = result.scalars().first()
    
    if usuario is None:
        raise credentials_exception
            
    return usuario