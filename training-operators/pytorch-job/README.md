# PyTorch Lightning MNIST Example on Kubeflow

## Overview

This directory contains a YAML configuration file for deploying a PyTorchJob
on Kubeflow using PyTorch Lightning and the MNIST dataset. How to create the 
corresponding code and how to build and push the container image is also 
described in this repository (`../../pytorch-lightning-mnist-image`).

## Usage

You have two options to deploy the PyTorchJob:

1. **Using `sed` commands**: Run the following command to replace placeholders 
   and apply the YAML configuration.
   
    ```sh
    sed 's/GITLABREGISTRY/<example.registry.com:4567>/' pytorch-lightning-mnist.yml | \
    sed 's/NAMESPACE/<your-namespace>/' | \
    sed 's/IMAGE_TAG/latest/' | \
    kubectl create -f -
    ```

2. **Manually Edit YAML**: Alternatively, you can manually replace 
   `GITLABREGISTRY`, `NAMESPACE`, and `IMAGE_TAG` directly in the YAML file, 
   then apply it with:
   
    ```sh
    kubectl create -f pytorch-lightning-mnist.yml
    ```

This will deploy the PyTorchJob with the specified configuration.

## Configuration

You can modify the job parameters like number of epochs, batch size, and
learning rate directly in the YAML file under `spec.pytorchReplicaSpecs`.

## Monitoring

Logs and checkpoints are uploaded to a MinIO bucket. Monitoring can be
done via TensorBoard.

## Cleanup

To remove the PyTorchJob, you can either:

1. **Using `sed` commands**:

    ```sh
    sed 's/NAMESPACE/<your-namespace>/' pytorch-lightning-mnist.yml | \
    kubectl delete -f -
    ```

2. **Manually Edit YAML and use `kubectl`**:

    ```sh
    kubectl delete -f pytorch-lightning-mnist.yml
    ```
