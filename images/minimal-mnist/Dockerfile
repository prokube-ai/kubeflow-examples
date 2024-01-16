# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the necessary files into the container directory
COPY training_script.py ./
COPY requirements.txt ./

# Install any required packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Define the command to run on container start
ENTRYPOINT ["python", "./training_script.py"]
