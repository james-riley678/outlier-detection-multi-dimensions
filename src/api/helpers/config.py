# MyPy for Static Typing
from typing import List, Set, Dict, Tuple, Optional, Any, Iterable

# PyPi Modules
import json
import os

class Config:
    def __init__(self) -> None:
        self.config: dict = self.__getConfig()

    def get(self) -> Any:
        return self.config

    def __getConfig(self) -> dict:
        envVariables: os._Environ = os.environ
        if "PYTHON_ENV" in envVariables and "PYTHON_CONFIG_DIR" in envVariables:
            pythonEnv = os.getenv("PYTHON_ENV")
            
            pythonConfigDir: str = str(os.getenv("PYTHON_CONFIG_DIR"))
            pythonConfigDir = pythonConfigDir.rstrip('/')
            with open(f'{pythonConfigDir}/{pythonEnv}.json') as configData:
                config: dict = json.load(configData)
                return config
        else:
            raise ConfigError("PYTHON_ENV or/and PYTHON_CONFIG_DIR environment variables not declared for configuration file") 

class ConfigError(Exception):
    pass

config = Config().get() 