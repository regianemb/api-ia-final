from fastapi import FastAPI, UploadFile, File, Form, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, Field
from app.services import executar_extracao, executar_categorizacao
from app.security import verificar_token_jwt, criar_token_jwt, USUARIO_CORRETO, SENHA_CORRETA
from app.logs import logger

app = FastAPI(
    title="Nexus AI - API com Autenticação JWT",
    description="API Corporativa contendo serviços de IA protegidos por autenticação via tokens JWT.",
    version="1.1.0"
)

class ProdutoSchema(BaseModel):
    descricao: str = Field(..., min_length=5, description="Descrição bruta do item a ser classificado.")

# --- ROTA DE LOGIN (Para gerar o Token) ---
@app.post("/api/v1/auth/login", tags=["Autenticação"])
def login(dados_formulario: OAuth2PasswordRequestForm = Depends()):
    if dados_formulario.username == USUARIO_CORRETO and dados_formulario.password == SENHA_CORRETA:
        token = criar_token_jwt({"sub": dados_formulario.username})
        logger.info(f"Usuário '{dados_formulario.username}' logado com sucesso. Token gerado.")
        return {"access_token": token, "token_type": "bearer"}
    
    logger.warning(f"Tentativa de login inválida com usuário: {dados_formulario.username}")
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário ou senha incorretos.")

# --- ROTAS DOS SERVIÇOS DE IA PROTEGIDOS POR JWT ---
@app.post("/api/v1/extracao-documento", tags=["Serviços de IA"])
async def api_extracao_documento(
    pergunta: str = Form(..., description="O dado que você quer extrair (Ex: 'What is the total amount?')"),
    arquivo: UploadFile = File(...),
    token_valido: dict = Depends(verificar_token_jwt)
):
    logger.info(f"Usuário autenticado '{token_valido['sub']}' solicitou extração de documento.")
    
    if not arquivo.content_type.startswith("image/"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Erro de Validação: O arquivo precisa ser uma imagem.")
        
    try:
        conteudo_imagem = await arquivo.read()
        resposta_ia = executar_extracao(conteudo_imagem, pergunta)
        return {"status": "sucesso", "resposta_da_ia": resposta_ia}
    except Exception as e:
        logger.error(f"Erro na extração: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro interno no processamento da IA.")

@app.post("/api/v1/categorizar-produto", tags=["Serviços de IA"])
def api_categorizar_produto(
    dados: ProdutoSchema,
    token_valido: dict = Depends(verificar_token_jwt)
):
    logger.info(f"Usuário autenticado '{token_valido['sub']}' solicitou categorização.")
    
    try:
        resultado_ia = executar_categorizacao(dados.descricao)
        return {"status": "sucesso", "resultado": resultado_ia}
    except Exception as e:
        logger.error(f"Erro na categorização: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro interno na categorização.")