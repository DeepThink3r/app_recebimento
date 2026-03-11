from typing import Optional, List, Any, Dict
from datetime import datetime, timedelta, timezone

from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

import jwt

from models.conferente_model import ConferenteModel
from core.configs import settings
from core.security import verificar_senha


oauth2_schema = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/conferente/login"
)

async def autenticar(re: int, senha: str, db: AsyncSession) -> Optional[ConferenteModel]:
    query = select(ConferenteModel).where(ConferenteModel.re == re)
    result = await db.execute(query)
    usuario: ConferenteModel = result.scalars().unique().one_or_none()

    if not usuario:
        return None
    
    if not verificar_senha(senha, usuario.senha):
        return None
    
    return usuario
    
    
def _criar_token(sub: str, tempo_vida: timedelta, tipo_token: str = "access") -> str:
    """
    Cria um JWT seguindo a RFC 7519.
    
    Args:
        sub: Identificador único do usuário (Subject).
        tempo_vida: Duração da validade do token.
        tipo_token: 'access' ou 'refresh' (armazenado em claim privada).
    """
    agora = datetime.now(timezone.utc)
    expira = agora + tempo_vida
    
    payload: Dict[str, Any] = {
        "iat": agora,              
        "exp": expira,             
        "sub": str(sub),           
        "type": tipo_token
    }
    
    return jwt.encode(
        payload, 
        settings.SECRET_KEY, 
        algorithm=settings.ALGORITHM
    )


def criar_token_acesso(sub: str) -> str:
    return _criar_token(
        sub=sub,
        tempo_vida=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        tipo_token="access"
    )