from kserve import Model, constants
from typing import Dict
import logging
from rdkit import Chem
from .features import get_cfps


logging.basicConfig(level=constants.KSERVE_LOGLEVEL)


class MolTransformer(Model):
    def __init__(self, name: str, predictor_host: str, headers: Dict[str, str] = None):
        super().__init__(name)
        self.predictor_host = predictor_host
        self.ready = True

    def preprocess(self, inputs: Dict, headers: Dict[str, str] = None) -> Dict:
        return {'instances': [list(get_cfps(Chem.MolFromSmiles(instance))) for instance in inputs['instances']]}

    def postprocess(self, inputs: Dict, headers: Dict[str, str] = None) -> Dict:
        return inputs


if __name__ == "__main__":
    mt = MolTransformer("n", 'localhost')
    mt