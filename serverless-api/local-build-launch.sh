#!/bin/bash

IMAGE=serverless/api

docker buildx build --platform linux/amd64 . -t $IMAGE
docker images -f "dangling=true" -q | xargs docker rmi
sam build
sam local start-api