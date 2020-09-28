#!/bin/bash
app="nlpdemo.api"

docker build -t ${app} .
docker run -d -p 56733:80 \
  --name=${app} \
  -v /home/yanick/KRAKEN/PIP/NLP/demo/dataset/dataset:/app ${app} \

