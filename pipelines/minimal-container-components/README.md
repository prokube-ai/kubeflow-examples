# Minimal container components
This example shows a minimal example of how to use 
[container components](https://www.kubeflow.org/docs/components/pipelines/v2/components/container-components/)
in pipelines.  

The pipeline itself is in `pipeline.py` and you can use `submit-cluster.py` or `submit-remote.py` to submit from
the cluster (e.g. form a KF-Notebook) or remotely, respectively.

For remote submission, you'll need to follow the preparation steps outlined below.

## Preparing for Remote KFP Connection
### Deployments that expose pipelines endpoint
To submit a pipeline remotely you need a deployment that uses dex as an identity provider and exposes the 
pipelines endopint.

```sh
export KUBEFLOW_ENDPOINT="http://my-endpoint"
export KUBEFLOW_USERNAME="example@user.com"
export KUBEFLOW_PASSWORD="12341234"
 ```

### Deployments that don't expose the endpoint
In this case we have to resort to port-forwarding
1. **Port Forwarding**: Set up port forwarding to the cluster by executing the following command:
   ```sh
   kubectl port-forward --namespace istio-system svc/istio-ingressgateway 8080:80
   ```
   Make sure it remains running in a separate terminal.
2. **Setting environment variables**: Define these environment variables in your shell. Make sure to replace the username and password with your own credentials:
    ```sh
    export KUBEFLOW_ENDPOINT="http://localhost:8080"
    export KUBEFLOW_USERNAME="example@user.com"
    export KUBEFLOW_PASSWORD="12341234"
    ```
