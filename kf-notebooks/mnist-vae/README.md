# Minimal Example: MNIST VAE with Kubeflow

This example demonstrates a) how Kubeflow notebooks can be used as a full-featured Python IDE, and b) how Kubeflow's TensorBoard feature can be utilized for tracking PyTorch training sessions. This repository contains a minimal example of a Variational Autoencoder (VAE) designed to generate MNIST images as a generative model.

## Installation

In this directory, run:

```sh
poetry install
```

## Run Training

Also, from the location where this README is located, run:

```sh
poetry run python run_training.py --hidden_dim=400 --latent_dim=2
```

Now sit back, relax, and wait for the training to complete.

## Install ipykernel

To use the training environment within a Jupyter notebook, install the kernel:

```sh
poetry run ipython kernel install --name "mnist-env" --user
```

## Run Visualization

To visualize the training results:

1. Open a Jupyter notebook or JupyterLab. If you're using a code-server Kubeflow notebook, this step is not necessary.
2. Run:

```sh
poetry run jupyter-notebook
```

3. Open the notebook ./visualizations.ipynb.
4. Select the right kernel (mnist-env).
5. Execute all the cells to explore the visualizations.

## Use Tensorboard

To visualize the training progress with Kubeflow's TensorBoard feature:

1. In Kubeflow, navigate to the TensorBoard section and click New TensorBoard.
2. Give the TensorBoard instance a name, select PVC (Persistent Volume Claim), and choose the volume that is mounted to the notebook used for training.
3. Use TensorBoard to monitor and visualize various aspects of the training session.
