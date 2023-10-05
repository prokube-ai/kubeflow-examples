# Katib Experiment with PyTorch Lightning and MNIST

## Overview

This directory contains a YAML configuration file 
(`katib-pytorchjob-mnist-experiment.yaml`) for deploying a Katib Experiment 
using PyTorch Lightning and the MNIST dataset. The procedure for creating the 
corresponding code and building and pushing the container image is described in 
another section of this repository (`../../pytorch-lightning-mnist-image`).

## Usage

You have two options to deploy the Katib Experiment:

1. **Using `sed` commands**: Run the following command to replace placeholders 
   and apply the YAML configuration.

    ```sh
    sed 's/GITLABREGISTRY/<example.registry.com:4567>/' katib-pytorchjob-mnist-experiment.yaml | \
    sed 's/NAMESPACE/<your-namespace>/' | \
    sed 's/IMAGE_TAG/latest/' | \
    kubectl create -f -
    ```

2. **Manually Edit YAML**: Alternatively, you can manually replace 
   `GITLABREGISTRY`, `NAMESPACE`, and `IMAGE_TAG` directly in the YAML file, 
   then apply it with:

    ```sh
    kubectl create -f katib-pytorchjob-mnist-experiment.yaml
    ```

## Configuration

Modify the experiment parameters like `learning_rate` and `batch_size` directly
in the YAML file under `spec.parameters`.

## Monitoring

You can monitor the progress of the experiment in the Katib UI under 
"Experiments" in the "AutoML" tab.

## Cleanup

To remove the Katib Experiment, you can either:

1. **Using `sed` commands**:

    ```sh
    sed 's/NAMESPACE/<your-namespace>/' katib-pytorchjob-mnist-experiment.yaml | \
    kubectl delete -f -
    ```

2. **Manually Edit YAML and use `kubectl`**:

    ```sh
    kubectl delete -f katib-pytorchjob-mnist-experiment.yaml
    ```
