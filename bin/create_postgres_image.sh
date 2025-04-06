#!/bin/zsh

docker build -t us-docker.pkg.dev/proyecto-cs-455920/gcr-compat/postgresql-custom postgresql-custom
docker push us-docker.pkg.dev/proyecto-cs-455920/gcr-compat/postgresql-custom
