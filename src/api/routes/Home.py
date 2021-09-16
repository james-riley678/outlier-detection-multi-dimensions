# MyPy for Static Typing
from typing import List, Set, Dict, Tuple, Optional, Any, Union

# Customer Modules
from api.helpers.logger import logger
from api.services.DetectOutliers import DetectOutliers

# PyPi Modules
from flask_restful import Resource, abort
from app import FlaskApi
from flask import Flask, render_template, request, redirect, url_for, make_response, send_file

class Home(Resource):           
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('index.html'),200,headers)

    def post(self):
        try:
            uploadFile = request.files['file']
            if uploadFile.filename != '':
                uploadFile.save(f'files/{uploadFile.filename}')
                newFileLocation: str =  DetectOutliers().execute(uploadFile.filename)
                return send_file(newFileLocation, as_attachment=True) 
            else:
                return redirect(url_for('home'))
        except Exception as error:
            logger.error(error)
            abort(500, error_message = str(error))