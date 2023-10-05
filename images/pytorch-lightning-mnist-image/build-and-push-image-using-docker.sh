#!/bin/bash

# Exit script on error
set -e

# Default Variables
IMAGE_REPOSITORY="/kiss/kubeflow-examples"

# Validate arguments
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <registry> <tag>"
    exit 1
fi

# Variables
IMAGE_NAME="pytorch-lightning-mnist-training"
TAG=$2
REGISTRY=$1

# Build the Docker image
echo "Building Docker image..."
docker build -t ${IMAGE_NAME}:${TAG} .

# Tag the Docker image
echo "Tagging Docker image..."
docker tag ${IMAGE_NAME}:${TAG} ${REGISTRY}${IMAGE_REPOSITORY}/${IMAGE_NAME}:${TAG}

# Push the Docker image to the registry
echo "Pushing Docker image to registry..."
docker push ${REGISTRY}${IMAGE_REPOSITORY}/${IMAGE_NAME}:${TAG}

echo "Docker image has been pushed: ${REGISTRY}${IMAGE_REPOSITORY}/${IMAGE_NAME}:${TAG}"
