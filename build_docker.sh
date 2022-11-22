#!/bin/sh
app="docker.test"
docker build -t ${app} .
docker run -d ${app} -p 56733:8000 \
  --name=${app} \
  -v $PWD:/app
