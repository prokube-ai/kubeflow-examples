# Utils
## auth_session.py

It is possible to connect to KF Pipelines from the outside of the cluster by getting a session cookie. More info
in the official [documentation](https://www.kubeflow.org/docs/components/pipelines/v1/sdk/connect-api/#full-kubeflow-subfrom-outside-clustersub).  

You can use `auth_session.py` to get the session cookie if your deployment is using dex.  
Example pipeline:
```python
from .auth_session import get_istio_auth_session
from kfp.client import Client
from kfp import dsl, compiler
import os


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

    compiler.Compiler().compile(my_pipeline, 'pipeline.yaml')

    run = client.create_run_from_pipeline_package(
        'pipeline.yaml',
        arguments={},
        run_name='My run'
    )
```
