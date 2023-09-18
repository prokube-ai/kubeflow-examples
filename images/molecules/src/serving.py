import joblib
from kserve import Model, constants
from kserve.errors import InferenceError, ModelMissingError
from typing import Dict
import logging
from rdkit import Chem
from .features import get_cfps
import pathlib
import os
#import s3fs

#S3_ENDPOINT = 'http://minio.minio'
#AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', None) or 'minio'
#AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', None)

logging.basicConfig(level=constants.KSERVE_LOGLEVEL)


class MolTransformer(Model):
    def __init__(self, name: str, predictor_host: str, n_bits: int = 1024, headers: Dict[str, str] = None):
        super().__init__(name)
        self.predictor_host = predictor_host
        self.n_bits = n_bits
        self.ready = True

    def preprocess(self, inputs: Dict, headers: Dict[str, str] = None) -> Dict:
        return {'instances': [[x.item() for x in get_cfps(Chem.MolFromSmiles(instance), nBits=self.n_bits)] for
                              instance in inputs['instances']]}

    def postprocess(self, inputs: Dict, headers: Dict[str, str] = None) -> Dict:
        return inputs


class MolPredictor(Model):
    def __init__(self, name: str):
        super().__init__(name)
        self.name = name
        self.ready = False
        self.load()

    def load(self):
        self.model = joblib.load(f'/mnt/models/{os.environ["MODEL_FILENAME"]}')
        self.ready = True
        print(f"Loaded {self.model.__str__()}")
        return self.ready

    def predict(self, payload: Dict, headers: Dict[str, str] = None) -> Dict:
        instances = payload["instances"]
        try:
            result = self.model.predict(instances).tolist()
            return {"predictions": result}
        except Exception as e:
            raise InferenceError(str(e))


if __name__ == "__main__":
    mt = MolTransformer("n", 'localhost')
    model = MolPredictor('m')
    mt