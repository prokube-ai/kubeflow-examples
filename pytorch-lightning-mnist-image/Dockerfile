# Use an official PyTorch runtime as a parent image with CUDA support
FROM pytorch/pytorch:2.0.0-cuda11.7-cudnn8-devel

# Set the working directory in the container
WORKDIR /app

# Install poetry
RUN pip install poetry

# Copy only the files necessary for installing dependencies
COPY pyproject.toml poetry.lock ./

# Install project dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev

# Copy the rest of the code
COPY . /app

# Run train.py when the container launches
CMD ["python", "run_training.py"]

