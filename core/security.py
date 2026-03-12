from pwdlib import PasswordHash


password_hash = PasswordHash.recommended()

def verificar_senha(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)


def gerar_hash_senha(password):
    return password_hash.hash(password)

