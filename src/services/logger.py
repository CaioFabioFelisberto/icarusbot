import logging
import os
import sys

def setup_logger():
    """Configura o sistema de logging estruturado do IcarusBot."""

    # 1. Garante que a pasta logs/ exista na raiz
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_file_path = os.path.join(log_dir, "icarusbot.log")
    
    # Formato do log: [Data Hora] [Nível] [Módulo]: Mensagem
    log_format = logging.Formatter(
        fmt='[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    # 2. Handler para exibir no Terminal (Console)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(log_format)
    console_handler.setLevel(logging.INFO)

    # 3. Handler para salvar em Arquivo (icarusbot.log)
    file_handler = logging.FileHandler(log_file_path, encoding='utf-8')
    file_handler.setFormatter(log_format)
    file_handler.setLevel(logging.INFO)

    # Limpa handlers antigos e adiciona os novos
    if root_logger.hasHandlers():
        root_logger.handlers.clear()
        
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)

    # Evita que logs muito poluídos de bibliotecas externas (httpx, urllib3) fiquem enchendo o terminal
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("asyncio").setLevel(logging.WARNING)

    logging.info("Sistema de Logging e Observabilidade inicializado com sucesso!")