##################################################################
# File          : build/Dockerfile
# Description   : Build instructions for the header-hook 
#                 production environment
# Maintainer(s) : richardgarryparker@gmail.com
# Created       : 2025-03-16
# Last updated  : 2025-03-16
# Change Log :
#   2025-03-16  : First release
##################################################################

#################################
# Operating system
#################################
# Base image: Ubuntu 22.04
FROM ubuntu:22.04
# This helps avoid interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

#################################
# App structure
#################################
# Set the working directory
WORKDIR /workspaces
# Copy directories to image
COPY ./build /app/build
COPY ./data /app/data
COPY ./src /app/src
COPY ./tests /app/tests
COPY ./utils /app/utils
# Add GitHub pre-commit hook configuration file
COPY ./.pre-commit-config.yaml /app/.pre-commit-config.yaml
# Add main project configuration file
COPY ./pyproject.toml /app/pyproject.toml
COPY ./VERSION /app/VERSION


#################################
# Dependencies
#################################
# Update the package list and install basic utilities
RUN apt-get update && \
    apt-get install -y \
    build-essential \
    curl \
    git \
    wget \
    software-properties-common && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
# Install not-so-basic utilities
RUN apt-get update && \
    apt-get install -y \
    python3 \
    python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Configuration related to pre-commit hooks
RUN apt-get update && apt-get install -y git locales
# Generate the en_US.UTF-8 locale
RUN locale-gen en_US.UTF-8
ENV LANG=en_US.UTF-8
ENV LANGUAGE=en_US:en
ENV LC_ALL=en_US.UTF-8


# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"
# Disable Poetry virtual environment (not needed in Docker)
ENV POETRY_VIRTUALENVS_CREATE=false
# Install production requirements
RUN poetry install --directory /app --without dev,docs --no-interaction --no-ansi

#################################
# Run
#################################
# Default command to run when the container starts
CMD ["bash"]
