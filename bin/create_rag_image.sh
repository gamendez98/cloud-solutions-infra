#!/bin/bash

docker build -f rag-api/document_indexing.dockerfile -t us-docker.pkg.dev/proyecto-cs-455920/gcr-compat/rag-api-indexing rag-api
docker push us-docker.pkg.dev/proyecto-cs-455920/gcr-compat/rag-api-indexing

docker build -f rag-api/ai_assistant.dockerfile -t us-docker.pkg.dev/proyecto-cs-455920/gcr-compat/rag-api-assistant rag-api
docker push us-docker.pkg.dev/proyecto-cs-455920/gcr-compat/rag-api-assistant