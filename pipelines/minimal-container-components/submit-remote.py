import sys
import pathlib

sys.path.append(str(pathlib.Path(__file__).parent.parent))

from utils.auth_session import get_istio_auth_session
import os
import datetime
from kfp.client import Client
from kfp import compiler
from pipeline import container_components_pipeline


auth_session = get_istio_auth_session(
    url=os.environ['KUBEFLOW_ENDPOINT'],
    username=os.environ['KUBEFLOW_USERNAME'],
    password=os.environ['KUBEFLOW_PASSWORD']
)


namespace = os.environ.get('KUBEFLOW_NAMESPACE', None) or \
            os.environ['KUBEFLOW_USERNAME'].split("@")[0].replace(".", "-")


if __name__ == "__main__":
    client = Client(host=f"{os.environ['KUBEFLOW_ENDPOINT']}/pipeline", namespace=namespace,
                    cookies=auth_session["session_cookie"], verify_ssl=False)

    compiler.Compiler().compile(container_components_pipeline, 'pipeline.yaml')

    run = client.create_run_from_pipeline_package(
        'pipeline.yaml',
        enable_caching=False,
        arguments={
            "input1": "Hello",
            "input2": "world!"
        },
        experiment_name='minimal-container-components-experiment',
        run_name=f'Simple pipeline {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
    )
