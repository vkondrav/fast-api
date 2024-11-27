#!/bin/bash

IMAGE=serverless/api
ECR_REPOSITORY_NAME=serverless/api
FUNCTION=serverless-api
REGION=us-east-1
ECR_REPOSITORY_URI=064513325338.dkr.ecr.$REGION.amazonaws.com

#Chat Pages
npm run build --prefix chat-app

wrangler pages deploy chat-app/build --project-name=chat

#Chat Proxy Worker
wrangler deploy --config chat-worker/wrangler.toml

#Lambda Function
aws ecr get-login-password --region $REGION | docker login --username AWS --password-stdin $ECR_REPOSITORY_URI

docker buildx build --platform linux/amd64 ./app -t $IMAGE
docker tag $IMAGE:latest $ECR_REPOSITORY_URI/$ECR_REPOSITORY_NAME:latest
docker push $ECR_REPOSITORY_URI/$ECR_REPOSITORY_NAME:latest

docker images -f "dangling=true" -q | xargs docker rmi

output=$(aws lambda update-function-code \
    --function-name $FUNCTION \
    --image-uri $ECR_REPOSITORY_URI/$IMAGE:latest)

echo "$output"

for _ in {1..10}; do
    status=$(aws lambda get-function --function-name $FUNCTION)
    last_update_status=$(echo "$status" | jq -r '.Configuration.LastUpdateStatus')

    if [ "$last_update_status" == "Successful" ]; then
        echo "Lambda function update successful."
        break
    fi

    echo "Waiting for Lambda function update to complete..."
    sleep 3
done

if [ "$last_update_status" != "Successful" ]; then
    echo "Lambda function update did not complete successfully within the timeout period."
    exit 1
fi

if [ "$last_update_status" == "Successful" ]; then
    echo "Deleting dangling images in ECR..."
    images=$(aws ecr list-images --repository-name "$ECR_REPOSITORY_NAME" --filter "tagStatus=UNTAGGED" --query 'imageIds[*]' --output json)
    if [ "$images" != "[]" ]; then
        output=$(aws ecr batch-delete-image --repository-name "$ECR_REPOSITORY_NAME" --image-ids "$images")

        failures=$(echo "$output" | jq -r '.failures')

        if [ "$failures" == "[]" ]; then
            echo "Dangling images deleted successfully."
        else
            echo "Failed to delete some dangling images."
        fi

        echo "Dangling images deleted."
    else
        echo "No dangling images to delete."
    fi
fi
