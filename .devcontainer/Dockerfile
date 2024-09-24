# Base Image
FROM python:3.12.6-bookworm


# If the steps of a `Dockerfile` use files that are different from the `context` file, COPY the
# file of each step separately; and RUN the file immediately after COPY
WORKDIR /app
COPY /.devcontainer/requirements.txt /app


# Installation
RUN apt update && apt -q -y upgrade && apt -y install sudo && sudo apt -y install graphviz && \
    pip install --upgrade pip && \
	pip install --requirement /app/requirements.txt --no-cache-dir


# Port
EXPOSE 8000


# ENTRYPOINT
ENTRYPOINT ["bash"]
