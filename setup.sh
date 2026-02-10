#!/bin/bash
set -e

PYTHON_VERSION=python3.12.1
ENV_NAME=cfp_venv #customer feedback pipeline

$PYTHON_VERSION -m venv $ENV_NAME
echo "Created virtual environment using $PYTHON_VERSION"

echo "Virtual environment created."
echo "To activate it, run:"
echo "source $ENV_NAME/bin/activate"
# run 'deactivate' to exit venv