# Very Basic Example for a Training Image

This Docker image is a part of a simple demonstration project to showcase the 
capabilities of Katib for hyperparameter tuning in Kubernetes. The image 
encapsulates a basic machine learning training script using a Support Vector 
Machine (SVM) model on the MNIST dataset. The Katib example itself can be
found in the hparam-tuning directory of this reposity.

## Purpose of the Image

The primary purpose of this image is to serve as a minimal example for model 
training within the context of a Katib experiment. The image includes a Python 
training script (`training_script.py`) that accepts command-line arguments to adjust 
the SVM model's hyperparameters. These hyperparameters include `gamma`, `c`, 
`kernel`, `degree`, and `coef0`.

## Installation

Install Python dependencies:

```sh
pip install -r requirements.txt
```

## Usage

Run as a Python script:

```sh
python ./training_script.py --gamma 0.01 --c 1 --kernel rbf --degree 3 --coef0 0.0
```

Build using Docker:

```sh
docker build . -t katib-demo
```

Run as a Docker container:

```sh
docker run katib-demo --gamma 0.01 --c 1 --kernel rbf --degree 3 --coef0 0.0
```
