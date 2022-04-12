# MyPy for Static Typing
from typing import List, Set, Dict, Tuple, Optional, Any, Union

# Custom Modules
from api.helpers.config import config
from api.helpers.logger import logger

# PyPi Modules
from flask import Flask
from flask import request
from flask_restful import Resource, Api
from flask_cors import CORS, cross_origin
import logging
import os
import datetime
from waitress import serve


class FlaskApi:
    def __init__(self):
        self.debug: bool = False
        if config['logging']['loggerLevel'] != 'INFO': self.debug = True

        # Initialisation Methods   
        logger.info('Initialisng methods')
        self.__initialiseFlaskLogging()
        self.__initialiseEnvVariables()                 
        self.__initialiseFlaskApi()  
        logger.info('Methods Initialised')
        
        if config['logging']['loggerLevel'] == 'INFO':
            # Prod
            logger.info('Starting Server in Production Mode...')
            serve(self.app, host='0.0.0.0', port=self.port)    
        else:
            # Dev
            logger.info('Starting Server in Development Mode...')            
            self.app.run(host='0.0.0.0', port=self.port, debug=True)        

    def __initialiseFlaskLogging(self) -> None:
        loggerLevel: str = config["logging"]["loggerLevel"]
        console = logging.StreamHandler()
        console.setLevel(loggerLevel)
        formatter = logging.Formatter('[%(threadName)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s')
        console.setFormatter(formatter)        
        logging.getLogger('').addHandler(console)  

    def __initialiseFlaskApi(self) -> None:        
        self.app = Flask('APP')
        CORS(self.app)
        self.api = Api(app=self.app)

        self.__initialiseRoutes()        
        self.port = config['app']['port']

    def __initialiseRoutes(self) -> None:
        import api.routes as routes
        self.api.add_resource(routes.Home.Home, '/')
        # self.api.add_resource(routes.RunReport.RunReport, '/') 

    def __initialiseEnvVariables(self) -> None:
        envVariables: dict = config['app']['env']        
        for env in envVariables.keys():            
            os.environ[env] = envVariables[env]

if __name__ == '__main__':    
    FlaskApi()