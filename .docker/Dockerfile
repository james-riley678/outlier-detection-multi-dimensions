FROM 		python:3.7-slim-stretch
MAINTAINER 	James Riley

ARG API_NAME
ARG PROXY

ENV TZ=Europe/London \
    # API Env Variables
    API_NAME=$API_NAME \
    PYTHON_ENV=config \
    PYTHON_CONFIG_DIR=/apps/regression-engine/config \
    # PROXY Env Variable
    http_proxy=$PROXY \
    https_proxy=$PROXY
RUN env


RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone && \
    apt-get -y update && \
    apt-get -y install zip unzip libaio1 iputils-ping --fix-missing && \
    echo "alias ls='ls --color'" >> ~/.bashrc
    
WORKDIR /apps/
RUN mkdir -p /apps/$API_NAME
COPY $API_NAME.tgz /apps/$API_NAME
RUN cd $API_NAME && tar zxf $API_NAME.tgz && rm $API_NAME.tgz

COPY startup.sh /startup.sh
COPY Dockerfile /apps/$API_NAME/Dockerfile

RUN mkdir /var/log/EV && \
    chmod +x /startup.sh && \
    python -m pip install --upgrade pip && \
    python -m pip install pipenv && \    
    cd /apps/$API_NAME && pipenv install 

# CMD tail -f /dev/null

ENTRYPOINT ["/startup.sh"]
