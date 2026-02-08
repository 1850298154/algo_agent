import logging
import sys
from src.retrieval.arXiv.config import LOG_FILE

def setup_logger(name="ArxivDownloader"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    if not logger.handlers:
        formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
        
        # 文件处理器
        file_handler = logging.FileHandler(LOG_FILE, encoding='utf-8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        # 控制台处理器
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)
        
    return logger

# 创建全局单例logger
logger = setup_logger()