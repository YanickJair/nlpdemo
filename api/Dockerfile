FROM tiangolo/uwsgi-nginx-flask:python3.8

MAINTAINER Yanick Andrade

RUN apt-get install bash

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

COPY ./requirements.txt /home/yanick/KRAKEN/PIP/NLP/demo/api/requirements.txt
RUN pip install -r /home/yanick/KRAKEN/PIP/NLP/demo/api/requirements.txt
