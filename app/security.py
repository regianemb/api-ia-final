from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime, timedelta, timezone
import jwt

# Configurações do JWT
SECRET_KEY = "sua_chave_secreta_super_segura_mpgo" # Chave para criptografar o token
ALGORITHM = "HS256" # Algoritmo de segurança
TEMPO_EXPIRACAO_MINUTOS = 30

# Simulação de usuário cadastrado no sistema para o teste
USUARIO_CORRETO = "admin"
SENHA_CORRETA = "pos2026"

# O FastAPI usa o HTTPBearer para gerenciar o cadeado do JWT no Swagger automaticamente
security_bearer = HTTPBearer()

def criar_token_jwt(dados: dict):
    """Gera o token criptografado com data de expiração."""
    copia_dados = dados.copy()
    # Define que o token vai expirar em 30 minutos
    tempo_expiracao = datetime.now(timezone.utc) + timedelta(minutes=TEMPO_EXPIRACAO_MINUTOS)
    copia_dados.update({"exp": tempo_expiracao})
    
    # Encripta os dados usando nossa chave secreta
    token_criptografado = jwt.encode(copia_dados, SECRET_KEY, algorithm=ALGORITHM)
    return token_criptografado

def verificar_token_jwt(credentials: HTTPAuthorizationCredentials = Depends(security_bearer)):
    """Verifica se o token enviado é válido e não expirou."""
    token = credentials.credentials
    try:
        # Descriptografa o token recebido
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload # Retorna os dados do usuário contidos no token se estiver tudo OK
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="O Token enviado já expirou. Faça login novamente."
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou corrompido."
        )