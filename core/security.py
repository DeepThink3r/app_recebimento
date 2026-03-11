from datetime import datetime, timedelta, timezone
from typing import Any, Union
import jwt
from core.configs import settings
from pwdlib import PasswordHash


password_hash = PasswordHash.recommended()

DUMMY_HASH = password_hash.hash("dummypassword")


def verificar_senha(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)


def gerar_hash_senha(password):
    return password_hash.hash(password)

