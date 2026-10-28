import logging
import sys
from pathlib import Path

def setup_logger(name: str = "StickEmpiresDailyCoinCollectionLoop") -> logging.Logger:
    logger = logging.getLogger(name)
    
    if logger.hasHandlers():
        return logger

    logger.setLevel(logging.INFO)

    log_format = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] (%(filename)s:%(lineno)d) -> %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    log_file_path = Path("app.log")
    file_handler = logging.FileHandler(log_file_path, encoding="utf-8")
    file_handler.setFormatter(log_format)
    file_handler.setLevel(logging.INFO)
    logger.addHandler(file_handler)

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(log_format)
    stream_handler.setLevel(logging.INFO)
    logger.addHandler(stream_handler)

    return logger

logger = setup_logger()
