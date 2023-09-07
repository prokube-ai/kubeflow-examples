# chem-util
A simple python script that reads in a CSV with SMILES, calculates molecular fingerprints, trains a model and 
evaluates it. It is the basis for `pipelines/molecules` pipeline.

## Local run
Help
```shell
chem-util.py --help
```

All steps
```shell
mkdir /tmp/chem
chem-util.py preprocess -i ../../data/ames.csv.zip -o /tmp/chem/processed.csv.zip
chem-util.py split -i /tmp/chem/processed.csv.zip -o /tmp/chem/train.csv.zip -t /tmp/chem/test.csv.zip
chem-util.py train -i /tmp/chem/train.csv.zip -o /tmp/chem/model.joblib
chem-util.py evaluate -i /tmp/chem/test.csv.zip -m /chem/model.joblib
```

## Local build
```shell
docker build --platform linux/amd64 . -t chem-util
# Test run
docker run chem-util --help
# Jumping into the container with bound local folder
docker run --entrypoint /bin/bash -it -v <local-path>:<container-path> chem-util
```