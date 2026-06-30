import logging

# Configura o diário de bordo (Log) da nossa API
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(message)s",
    handlers=[
        logging.FileHandler("api_funcionamento.log", encoding="utf-8"), # Salva no arquivo
        logging.StreamHandler() # Mostra no terminal em tempo real
    ]
)

logger = logging.getLogger("nexus_ai")