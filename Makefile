.PHONY: help install install-dev test lint format clean run-api run-dashboard

help:
	@echo "Targets:"
	@echo "  install       Install core deps + project (editable)"
	@echo "  install-dev   Install core + dev deps"
	@echo "  test          Run pytest"
	@echo "  lint          Check lint + format (no changes)"
	@echo "  format        Auto-fix lint + format"
	@echo "  clean         Remove caches and build artifacts"
	@echo "  run-api       Start FastAPI server"
	@echo "  run-dashboard Start Streamlit dashboard"

install:
	python -m pip install --upgrade pip
	pip install -e .

install-dev:
	python -m pip install --upgrade pip
	pip install -e ".[dev]"

test:
	pytest -q

lint:
	ruff check src tests api
	ruff format --check src tests api

format:
	ruff check --fix src tests api
	ruff format src tests api

clean:
	rm -rf .pytest_cache .ruff_cache build dist *.egg-info
	rm -rf mlruns mlartifacts
	find . -type d -name "__pycache__" -exec rm -rf {} +

run-api:
	uvicorn api.main:app --reload --host 0.0.0.0 --port 8000

run-dashboard:
	streamlit run src/dashboard/app.py