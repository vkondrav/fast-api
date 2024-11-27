#!/bin/bash

cleanup() {
    echo "Killing all background processes..."
    kill $worker_pid $app_pid $sam_pid
}

trap cleanup EXIT

docker buildx build --platform linux/amd64 ./app -t serverless/api
docker images -f "dangling=true" -q | xargs docker rmi

(cd chat-worker && wrangler dev) &
worker_pid=$!
(cd chat-app && npm run dev) &
app_pid=$!
(cd app && sam build && sam local start-api --warm-containers EAGER --debug)
sam_pid=$!

wait