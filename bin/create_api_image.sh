#!/bin/bash

docker build -t us-docker.pkg.dev/proyecto-cs-455920/gcr-compat/cloud-solutions-api cloud-solutions-api
docker push us-docker.pkg.dev/proyecto-cs-455920/gcr-compat/cloud-solutions-api