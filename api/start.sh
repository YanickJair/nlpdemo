#!/bin/bash
app="nlpapi"

docker build -t ${app} .
docker run -d -p 5000:80 \
  --name=${app} \
  -v ${pwd}:/nlpapi ${app} \

