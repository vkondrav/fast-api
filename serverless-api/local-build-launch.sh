#!/bin/bash

IMAGE=serverless/api

npm run build --prefix chat-app

rm -rf app/static/*
mkdir -p app/static
mv chat-app/build/* app/static/

docker buildx build --platform linux/amd64 . -t $IMAGE
docker images -f "dangling=true" -q | xargs docker rmi

sam build
sam local start-api