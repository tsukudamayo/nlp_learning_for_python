FROM python:3
RUN apt-get -y update \
    && apt-get -y upgrade \
    && mkdir /code 
WORKDIR /code
ADD requirements.txt /code
RUN pip install -r requirements.txt
