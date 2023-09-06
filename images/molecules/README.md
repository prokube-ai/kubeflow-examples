# chem-util
A simple python script that reads in a CSV with SMILES, calculates molecular fingerprints, trains a model and 
evaluates it.

## Local build
```shell
docker build --platform linux/amd64 . -t chem-util
# Test run
docker run chem-util --help
# Jumping into the container with bound local folder
docker run --entrypoint /bin/bash -it -v <local-path>:<container-path> chem-util
```