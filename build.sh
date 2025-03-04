#!/bin/bash

if [ ! -d "rag-api" ]; then
    git clone https://github.com/SantiagoFino/rag-api
fi

if [ ! -d "cloud-solutions-api" ]; then
    git clone https://github.com/gamendez98/cloud-solutions-api
fi

if [ ! -d "misisCloudProject1-frotend" ]; then
    git clone https://github.com/helberthCO/misisCloudProject1-frotend
fi

docker-compose up --build