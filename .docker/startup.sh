#!/bin/bash

ln -snf /usr/local/bin/python /usr/bin/python
cd /apps/$API_NAME && pipenv run build
pipenv run prod
