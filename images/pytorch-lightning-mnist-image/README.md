# PyTorch Training Image for Kubeflow

## Overview

This repository contains resources for building a containerized PyTorch 
(and PyTorch Lightning) training environment. It's compatible with 
Kubeflow's training operators and Katib's hyperparameter tuning. The focus 
is on containerizing and deploying code for Kubeflow, not on the model or 
data science aspects. The example uses PyTorch Lightning and the MNIST dataset.

## Features

- **Run Anywhere**: Execute locally, inside Docker, in a Kubeflow notebook, as a PyTorchJob, or through Katib.
- **TensorBoard**: Integrated for monitoring training metrics. Can be used both locally and with Kubeflow's TensorBoard when MinIO syncing is enabled.
- **Custom Callbacks**: 
    - MinIO Syncing: Custom callback for syncing logs and checkpoints with MinIO.
    - Katib Logging: Custom callback to write training and validation loss metrics to standard output for Katib optimization.
- **Framework**: Utilizes PyTorch Lightning.
- **Dependencies**: Managed via Poetry.
- **Flexible setup**: Suitable for single and multi-node training as well as CPU and GPU environments.

## Installation

To install the required Python packages locally, you'll need [Poetry](https://
python-poetry.org/). Navigate to this directory and run:

```sh
poetry install
```

This will read the `pyproject.toml` and `poetry.lock` files and install the dependencies accordingly.

## Usage

### Local Development

The Python script `run_training.py` has several command-line options that can be set to customize the behavior of the model training:

  - `--batch_size`: The batch size for training. Default is 64.
  - `--learning_rate`: The learning rate for the optimizer. Default is 0.001.
  - `--epochs`: The number of epochs for the training loop. Default is 10.
  - `--run_as_pytorchjob`: Flag to indicate whether the script should run in the context of a Kubeflow PyTorchJob. Default is False.
  - `--logs_bucket`: Name of the MinIO bucket where logs will be stored. Default is "kubeflow-examples".
  - `--logs_folder`: Name of the folder within the MinIO bucket where logs will be stored. Default is "mnist-logs".
  - `--sync_minio`: Flag to indicate whether logs and checkpoints should be synced to Minio. Default is False.
  - `--num_nodes`: Number of machines for training. Default is 1.
  - `--num_data_loader_workers`: Number of PyTorch DataLoader workers. Default is 0.
  - `--use_std_out_logger`: Flag to indicate whether to log loss to standard output. Default is False.

An example of how to use these options can be found in the file `./run_locally.sh`, which is executable.
To run the training script on your local machine or within a notebook pod, run:
```bash
./run_locally.sh
```

### What Happens When the Code is Run?

In addition to the standard PyTorch Lightning procedure, the following things happen in the script:
1. **MinIO Bucket**: A bucket named "kubeflow-examples" is created in MinIO if 
   it doesn't already exist. Within this bucket, a folder called "mnist-logs" 
   is also created, unless specified otherwise via CLI arguments.

2. **Logs and Checkpoints**: At the end of each training epoch, both the 
   training logs and model checkpoints are uploaded to this MinIO bucket. This 
   allows you to monitor training progress through TensorBoard in real-time.

3. **Best Model**: For the checkpoints, the model with the best performance on
   the validation set is used.

For further details and customization options, refer to the code and the 
comments contained within it.

## Building and Pushing the Image

### Using Docker

1. **Prepare for the Script**: Before running the script, make sure you're 
   authenticated with the Docker registry. If needed, log in as follows:

    ```bash
    docker login <example.registry.com>:4567 -u <token name> -p <token>
    ```

    Note: This may require setting up a project access token in the Gitlab
    UI first. Navigate to: Gitlab UI -> this Repository -> Settings -> Access 
    Token -> Add a project access token.

2. **Run the Script**: Use `build-and-push-image-using-docker.sh <registry>
   <tag>` to build and push the image.

    Example:

    ```bash
    ./build-and-push-image-using-docker.sh <example.registry.com>:4567 my-tag
    ```

    This builds an image named `pytorch-lightning-mnist-training` with the tag 
    `my-tag` and pushes it to the Gitlab registry of this repository.

### Using GitLab Runner with Kaniko

1. **Automated Build**: Trigger an automatic build by committing a change to
   any file in or under the directory where this README resides. This activates
   a GitLab CI/CD pipeline using Kaniko. The built image will receive two tags:
    - `latest`: Always points to the most recent build.
    - `commit-<SHORT_COMMIT_HASH>`: Associates the image with a specific 
       Git commit.

