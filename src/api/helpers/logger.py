# MyPy for Static Typing
from typing import List, Set, Dict, Tuple, Optional, Any, Iterable

# Custom Modules
from .config import config

# PyPi Modules
import logging
from logging.handlers import RotatingFileHandler

def getLogger() -> logging.Logger:        
    loggerLocation = config["logging"]["loggerLocation"]
    loggerLevel = config["logging"]["loggerLevel"]
    logging.basicConfig(
        filename=loggerLocation,
        level=loggerLevel, 
        format= '[%(asctime)s] [%(threadName)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    logger = logging.getLogger(__name__)    
    # loggers = logging.getLogger(__name__)
    # loggers.setLevel(loggerLevel)
    # if not len(loggers.handlers): #Checking if handlers for job does not exist
    #     fh = logging.FileHandler(loggerLocation)
    #     fh.setLevel(loggerLevel)
    #     formatter = logging.Formatter('[%(asctime)s] [%(threadName)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s', '%Y-%m-%d %H:%M:%S')
    #     fh.setFormatter(formatter)    
    #     loggers.addHandler(fh)

    #     ch = logging.StreamHandler()
    #     ch.setLevel(loggerLevel)
    #     ch.setFormatter(formatter)
    #     loggers.addHandler(ch) 
    return logger     

logger: logging.Logger = getLogger()