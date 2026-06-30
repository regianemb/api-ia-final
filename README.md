# 🤖 Nexus AI - API de Serviços de Inteligência Artificial

Trabalho final desenvolvido para a disciplina de **Construção de APIs para Inteligência Artificial** 

Esta API corporativa disponibiliza dois serviços distintos de Inteligência Artificial utilizando modelos reais e pré-treinados da Hugging Face, estruturada sob o framework **FastAPI** (Python 3.13).

**ALUNOS:**
- EDUARDO DE AGUIAR REZENDE 
- REGIANE MENDES BARBOSA

**TURMA:** T3 - MPGO 2026

---

## 📁 Estrutura do Projeto

* `app/main.py`: Ponto de entrada da API, gerenciamento de rotas e tratamento de exceções.
* `app/services.py`: Camada de serviços responsável pela inicialização e execução dos modelos de IA.
* `app/security.py`: Segurança e autenticação baseada em tokens de acesso **JWT**.
* `app/logs.py`: Centralização de registros e auditoria do sistema (`api_funcionamento.log`).

---

## 🛠️ Requisitos Básicos Atendidos

* **a. Validação de dados:** Implementada via `Pydantic` no endpoint de categorização e na checagem de tipo mime (`image/*`) no endpoint de extração.
* **b. Tratamento de erros:** Tratamento de exceções via blocos `try/except` convertendo falhas internas e retornos em respostas HTTP limpas e sem traces para o cliente (`400`, `401` e `500`).
* **c. Logs:** Gravação em segundo plano do arquivo `api_funcionamento.log` descrevendo data/hora, rotas acessadas, status e erros.
* **d. Segurança:** Bloqueio de endpoints usando Autenticação via **Token JWT** (`Bearer Token` com expiração de 30 minutos).
* **e. Versionamento:** URLs controladas utilizando o padrão de rotas versionadas `/api/v1/`.

---

## 🧠 Modelos de IA Utilizados

1. **Visão Computacional para Documentos:**
   - **Modelo:** `naver-clova-ix/donut-base-finetuned-docvqa`
   - **Descrição:** Modelo da família Donut (*OCR-free Transformer*). Oferece extração de informações de documentos em formato de imagem sem requerer o utilitário Tesseract OCR na máquina host, tornando a aplicação portátil para produção.
2. **Classificação de Texto (Zero-Shot):**
   - **Modelo:** `facebook/bart-large-mnli`
   - **Descrição:** Classifica textos e descrições de produtos de forma dinâmica em português dentro de categorias customizáveis sem necessitar de treinamento adicional.

---

## 🚀 Como Executar este Projeto

### 1. Clonar ou Baixar o Repositório
Navegue até a pasta pelo terminal:
```bash
cd api-ia-final
```

### 2. Criar e Ativar o Ambiente Virtual (venv)
*No Windows (PowerShell/CMD):*
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

*No Linux / macOS:*
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar as Dependências
Utilize o `requirements.txt` modificado (que inclui `timm` para execução do Donut):
```bash
pip install -r requirements.txt
```

### 4. Executar Servidor FastAPI
Execute o servidor de desenvolvimento via Uvicorn:
```bash
uvicorn app.main:app --reload
```
A API estará acessível localmente em: **http://127.0.0.1:8000**

---

## 🔒 Instruções de Teste e Autenticação (JWT)

A API utiliza o padrão de segurança **JWT (JSON Web Tokens)**. Os serviços de IA só processarão requisições se um token válido for fornecido.

### Passo a Passo para Testar no Navegador:

1. Acesse a documentação interativa em: **http://127.0.0.1:8000/docs**
2. Localize a rota vermelha **`POST /api/v1/auth/login`**.
3. Clique em **Try it out** e preencha as credenciais de teste:
   * **username:** `admin`
   * **password:** `pos2026`
4. Clique em **Execute**. A API retornará um JSON contendo o seu token no campo `"access_token"`. Copie aquele código extenso.
5. Suba até o topo da página do Swagger e clique no botão **Authorize** (ícone do cadeado).
6. Cole o token copiado no campo de texto e clique em **Authorize**, depois em **Close**.
7. **Pronto!** O cadeado estará fechado e você poderá testar as rotas de Extração de Documentos e Categorização de Produtos normalmente. O token expira automaticamente após 30 minutos.
