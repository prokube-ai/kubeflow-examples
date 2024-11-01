FROM pytorch/pytorch:latest
RUN apt-get update && apt-get install -y libglib2.0-0
RUN mkdir /app
WORKDIR /app
COPY pyproject.toml /app/
COPY llama2_chat /app/llama2_chat
RUN python -m pip install .
ADD main.py ./main.py
ENV PORT=8080
EXPOSE 8080
