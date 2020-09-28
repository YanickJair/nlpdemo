FROM tiangolo/uwsgi-nginx-flask:python3.8

RUN apt install bash

COPY ./dataset /home/yanick/KRAKEN/PIP/NLP/demo/api

COPY ./requirements.txt /home/yanick/KRAKEN/PIP/NLP/demo/requirements.txt
RUN pip install -r /home/yanick/KRAKEN/PIP/NLP/demo/requirements.txt
