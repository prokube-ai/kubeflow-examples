# Llama2 Deployment

For deploying the Llama2 model, we will create a custom predictor using KServe.
KServe provides a way to implement a custom model server, enabling you to bring
your own models and pre- and post-processing code.
In the `images` directory of this repo, you'll find a directory holding all the
code and the Dockerfiles needed to create the image for this deployment.
Here, we'll assume the image is in a registry that KServe has access to and
focus on the Kserve specific steps of the deployment.
If you are interested, also feel free to check out our simple UI, which is
designed to use this deployment (`images/llama2-chat-ui`).

## Hugging Face Token

You'll need a Hugging Face token to utilize the transformers library for downloading
the model weights. Additionally, you'll need to ask Meta for permission to use the
Llama model itself. You can read more about that [here](https://huggingface.co/blog/llama2).

The code expects an environment variable named `HF_ACCESS_TOKEN` that holds the token as a string.

### Creating a Kubernetes Secret

We've created a file called hf-token-secret.yaml in this directory to create a 
Kubernetes secret that holds the access token (which we'll need for the kserve 
deployment later on). First, encode the token to base64 by running:
```sh
echo -n <example-token> | base64
```

Now, the output of the above command can be used to create the Kubernetes secret:
```sh
sed 's/HF_ACCESS_TOKEN/<example-token-base64>/' hf-token-secret.yaml | kubectl apply -n <your-namespace> -f -
```

## Deploy on KServe

Ensure there is a secret called hf-token-secret in your namespace and run this
to create the KServe inference service:
```
sed 's/IMAGE_REGISTRY/<your-image-registry>/;s/TAG/<your-tag>/' predictor.yaml | kubectl create -n <your-namespace> -f -
```
Note that you might need to change the command in the `prediction.yaml` to match your hardware.

### Run Query Against the KServe Deployment

First, wait for the API to be ready; you can observe the progress and logs, etc.,
in the Kubeflow UI under models. Note that this may take several minutes.
Once it's ready, you can copy the internal URL from
the Kubeflow UI and try:
```sh
curl <internal-inference-url> -d '{"top_k": 3, "max_length": 100, "instances": ["Why is MLOps so important?"]}'
```


