import io
import re
from PIL import Image
from transformers import pipeline

print("🤖 Inicializando Inteligência Artificial local... Por favor, aguarde.")

# SERVIÇO 1: Visão Computacional para Documentos (Modelo Donut Oficial)
extrator_ia = pipeline(
    "document-question-answering", 
    model="naver-clova-ix/donut-base-finetuned-docvqa"
)

# SERVIÇO 2: Classificação de Texto (Zero-Shot)
categorizador_ia = pipeline(
    "zero-shot-classification", 
    model="facebook/bart-large-mnli"
)

print("✅ Modelos de IA carregados com sucesso e prontos para uso!")

def executar_extracao(imagem_bytes: bytes, pergunta: str) -> str:
    """Recebe uma imagem em bytes e extrai o dado correspondente à pergunta."""
    try:
        # 1. Converte os bytes recebidos em imagem Pillow
        imagem = Image.open(io.BytesIO(imagem_bytes))
        
        # 2. Garante o modo RGB (essencial para o Donut não quebrar com PNG/JPG)
        if imagem.mode != "RGB":
            imagem = imagem.convert("RGB")
            
        # 3. Redimensiona para evitar estouro de memória no terminal
        imagem.thumbnail((1200, 1200))
            
        # 4. Executa o modelo
        resultado = extrator_ia(image=imagem, question=pergunta)
        
        # 5. TRATAMENTO DO RETORNO
        if resultado and len(resultado) > 0:
            dados_resposta = resultado[0]
            
            # Se a resposta vier no formato padrão de dicionário
            if isinstance(dados_resposta, dict) and 'answer' in dados_resposta:
                return str(dados_resposta['answer'])
            
            # Se a resposta vier como uma string direta (comum no Python 3.13)
            elif isinstance(dados_resposta, str):
                return dados_resposta
                
            # Caso venha outra estrutura, converte para texto e limpa as tags <...>
            texto_puro = str(dados_resposta)
            texto_limpo = re.sub(r"<.*?>", "", texto_puro)
            return texto_limpo.strip()

        return "Não foi possível encontrar a informação no documento."

    except Exception as e:
        print(f"❌ Erro interno no motor do Donut: {str(e)}")
        raise e

def executar_categorizacao(descricao_produto: str) -> dict:
    """Classifica um produto em categorias pré-definidas."""
    categorias_possiveis = ["Eletrônicos e Informática", "Alimentos e Bebidas", "Vestuário e Acessórios", "Ferramentas e Casa"]
    resultado = categorizador_ia(descricao_produto, candidate_labels=categorias_possiveis)
    return {
        "categoria_detectada": resultado['labels'][0],
        "confianca": f"{round(resultado['scores'][0] * 100, 2)}%"
    }