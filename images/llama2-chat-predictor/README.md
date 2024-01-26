# Llama2 Deployment

For deploying the Llama2 model, we will create a custom predictor using KServe.
This directory holds all the code as well as the Dockerfile to create
the image for the llama2 deployment in kserve.
The steps for the actual deployment in kserve can also be found in this repository
(`/serving/llama2-chat`).

If you are new to creating custom predictors with KServe, you may read more about it in the [KServe documentation](https://kserve.github.io/website/0.8/modelserving/v1beta1/custom/custom_model/).

For a gentle introduction and detailed guide on working with Llama2, consider reading this blog post: [How to prompt Llama](https://replicate.com/blog/how-to-prompt-llama).

## Hugging Face Token

You'll need a Hugging Face token to utilize the transformers library for downloading
the model weights. Additionally, you'll need to ask Meta for permission to use the
Llama model itself. You can read more about that [here](https://huggingface.co/blog/llama2).

The code expects an environment variable named `HF_ACCESS_TOKEN` that holds the token as a string.

### Setting the Variable Locally

To set this variable for a local deployment, run:
```sh
export HF_ACCESS_TOKEN=<example-token>
```

## Run/develop Locally

To run it locally, you'll need to first install the Python dependencies. To
do so, run the following from this directory:
```
poetry install .
export HF_ACCESS_TOKEN=<example-token>
poetry run python main.py --name "llama2-chat" --device "cpu" --hf-model-string "meta-llama/Llama-2-13b-chat-hf"
```

### Run Query Against Local Deployment

Once the server is up and running, you might try something like:
```sh
curl localhost:8080/v1/models/llama2-chat:predict -d '{"top_k": 3, "max_length": 200, "instances": ["Why is MLOps so important?"]}'
```
We decided to allow the user to set the inference options for top_k (number of
samples with the best scores, from which we sample) and max_length in the API query, along with the prompt.

## Build and Push Image

### Using docker
To build the model using Docker, do:
```sh
docker build -t <your-image-registry-name>/llama2-chat:<TAG> .
```

To use this image in kserve, we'll also need to push it to an image registry.
First, log in:
```sh
docker login <example.registry.com>:4567 -u <token name> -p <token>
```

Note: This may require setting up a project access token in the GitLab UI first.
Navigate to: GitLab UI -> this Repository -> Settings -> Access Token -> Add a project access token.

Now, you can push the image using Docker:
```sh
docker push <image-repository-name>/llama2-chat:<TAG>
```

### Using GitLab Runner with Kaniko
Automated Build: Trigger an automatic build by committing a change to
any file in or under the directory where this README lives. This activates
a GitLab CI/CD pipeline using Kaniko. The built image will receive two tags:

latest: Always points to the most recent build.
commit-<SHORT_COMMIT_HASH>: Associates the image with a specific
Git commit.
