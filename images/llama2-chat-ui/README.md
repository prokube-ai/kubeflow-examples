# Llama2-Chat UI Demo

A simple UI for our Llama2-Chat API, implemented with Dash, deployable as a Kubeflow notebook.

It's heavily inspired by [this dash example](https://github.com/plotly/dash-sample-apps/blob/main/apps/dash-gpt3-chatbot/app.py).
To use this, you'll need to deploy the model API first.
Detailed steps for the corresponding deployment in kserve can also be found in
this repository (`/serving/llama2-chat`).

## Running Locally

Make sure your local machine can communicate with the model API and follow these steps to run the application locally:

```sh
poetry install
poetry run python app.py
```

## Building and Pushing the Docker Image
### Using docker
#### Build

```sh
poetry export --without-hashes --format=requirements.txt > requirements.txt
docker build -t <your-image-registry>/llama2-chat-ui:<your-tag> .
```

#### Push

To utilize this image as a notebook image, it needs to be pushed to an image registry.

First, log in:
```sh
docker login <example.registry.com>:4567 -u <token name> -p <token>
```

Note: This might require setting up a project access token in the GitLab UI first. Navigate to: GitLab UI -> this Repository -> Settings -> Access Tokens -> Add a project access token.

Now, you can push the image using Docker:
```sh
docker push <image-repository-name>/llama2-chat-ui:<TAG>
```

### Using GitLab Runner with Kaniko
Automated Build: Trigger an automatic build by committing a change to
any file in or under the directory where this README lives. This activates
a GitLab CI/CD pipeline using Kaniko. The built image will receive two tags:

latest: Always points to the most recent build.
commit-<SHORT_COMMIT_HASH>: Associates the image with a specific
Git commit.

## Usage in Kubeflow

To use this image in Kubeflow, please follow these steps:

1. Click the launch notebook button.
2. Provide a name.
3. Select the "JupyterLab" option.
4. Tick the custom image checkbox.
5. Copy the path to the image from GitLab and paste it into the respective field.
6. The default options should be fine; configure the other options as desired and click launch.
