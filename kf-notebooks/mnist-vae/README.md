# Minimal Example Mnist Vae

## Clone this repo
From somewhere on your machine, run:
```sh
git clone git@imb-git.hsu-hh.de:imb/source-code/minimal-example-mnist-vae.git
```

## Installation
In this directory, run:
```sh
poetry install
```

## Run Training
Also, from the location where this README lives, run:

```sh
poetry run python run_training.py
```
Now sit back, relax, and wait.

## Install ipykernel
```sh
poetry run ipython kernel install --name "mnist-env" --user
```

## Run Visualization
Open a Jupyter notebook or JupyterLab, like so:
```sh
poetry run jupyter-notebook
```
Open the notebook `./visualizations.ipynb`.
Select the right kernel (`mnist-env`).
Execute all the cells and have fun.
