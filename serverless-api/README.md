
## Description

Simple API to run on AWS lambda for the purpose of transforming static seekr apis with business logic

## Setup

### Prerequisites

- [Docker](https://www.docker.com/get-started)
- [Visual Studio Code](https://code.visualstudio.com/)
- [Remote Containers Extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
- [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html)
- [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)
- [jq](https://stedolan.github.io/jq/download/) (for parsing function status)

### Using the Dev Container

This project includes a dev container configuration to provide a consistent development environment. Follow these steps to use the dev container:

1. **Open the project in Visual Studio Code.**

2. **Reopen in Container:**
   - Press `F1` to open the command palette.
   - Type `Remote-Containers: Reopen in Container` and select it.

3. **Wait for the container to build and start.**
   - The container will be built using the `Dockerfile` and the dependencies will be installed as specified in `requirements.txt`.

### Running the Function Locally

To run the function locally, follow these steps:

1. **Ensure Docker is running** on your machine

2. **Run the local build and launch script**:
    ```sh
    ./local-build-launch.sh
    ```

This script will:

- Build the Docker image for the project
- Build the AWS SAM application
- Start the API locally using SAM

You can now access the API locally at `http://localhost:3000/docs`.

### Pushing the Project to AWS

To push the project to AWS, follow these steps:

1. **Ensure Docker is running** on your machine.

2. **Configure the AWS CLI** with your credentials:
    ```sh
    aws configure
    ```

3. **Update AWS arguments**

The `cloud-build-launch.sh` script contains several variables that you may need to update to match your environment. These variables include:

- `IMAGE`: The name of the Docker image
- `ECR_REPOSITORY_NAME`: The name of the Amazon ECR repository
- `FUNCTION`: The name of the AWS Lambda function
- `REGION`: The AWS region where your resources are located
- `ECR_REPOSITORY_URI`: The URI of your Amazon ECR repository


4. **Run the cloud build and launch script**:
    ```sh
    ./cloud-build-launch.sh
    ```

This script will:

- Build the Docker image for the project
- Push the Docker image to Amazon ECR
- Update the AWS Lambda function with the new image
- Wait for successful Lambda function deploy
- Delete any dangling images from ECR