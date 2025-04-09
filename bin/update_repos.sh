#!/bin/bash

if [ ! -d "rag-api" ]; then
    git clone https://github.com/SantiagoFino/rag-api
else
    cd rag-api && git pull && cd ..
fi

if [ ! -d "cloud-solutions-api" ]; then
    git clone https://github.com/gamendez98/cloud-solutions-api
else
    cd cloud-solutions-api && git pull && cd ..
fi

if [ ! -d "misisCloudProject1-frotend" ]; then
    git clone https://github.com/helberthCO/misisCloudProject1-frotend
else
    cd misisCloudProject1-frotend && git pull && cd ..
fi