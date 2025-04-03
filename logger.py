import logging

def setup_logger(log_file='bot_log.txt', log_level=logging.DEBUG):
    logger = logging.getLogger('GomokuBot')
    logger.setLevel(log_level)
    
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(log_level)
    
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger
