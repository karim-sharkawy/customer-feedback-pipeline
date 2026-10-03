# ─────────────────────────────────────────────────────────────
# customer-feedback-pipeline
#
# Usage:
#   make setup     first time only — creates venv + installs deps
#   make ingest    downloads dataset into data/
#   make explore   opens Jupyter Lab
#   make test      runs pytest
#   make clean     nukes venv and downloaded data
# ─────────────────────────────────────────────────────────────

VENV := venv
PY   := $(VENV)/bin/python

# Windows uses Scripts/ instead of bin/
ifeq ($(OS),Windows_NT)
    PY := $(VENV)/Scripts/python.exe
endif

# .PHONY tells make these aren't real files — always run them,
# even if a file named "setup" happens to exist.
.PHONY: setup ingest explore test clean

# Create the venv (if missing) and install the project + dev deps.
# Safe to re-run: it always re-installs so deps stay in sync
# with pyproject.toml.
setup:
	python -m venv $(VENV)
	$(PY) -m pip install --upgrade pip
	$(PY) -m pip install -e ".[dev]"

# Download the Amazon reviews + products CSVs into data/.
# Change the filename if your ingestion script is named differently.
ingest:
	$(PY) ingestion.py

# Launch Jupyter Lab for exploring the data.
explore:
	$(PY) -m jupyter lab

# Run the test suite.
test:
	$(PY) -m pytest

# Delete the venv and any downloaded data.
# Warning: this is destructive — everything in data/ goes.
clean:
	rm -rf $(VENV)
	rm -f data/*.csv data/*.parquet