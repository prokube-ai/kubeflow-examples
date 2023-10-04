FROM mambaorg/micromamba:1.4.9
WORKDIR /app

COPY --chown=$MAMBA_USER:$MAMBA_USER env.yaml /tmp/env.yaml
RUN micromamba install -y -n base -f /tmp/env.yaml && \
    micromamba clean --all --yes

ARG MAMBA_DOCKERFILE_ACTIVATE=1

COPY . .

USER root
RUN export PATH="$PATH:/opt/conda/bin/"
ENTRYPOINT ["/opt/conda/bin/python", "/app/chem-util.py"]
