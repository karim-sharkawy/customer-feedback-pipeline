# Production ML Platform for NLP Feedback Intelligence

An end-to-end Machine Learning Engineering project that trains, deploys, and monitors transformer-based NLP models for customer feedback understanding at scale.

This repository demonstrates how modern ML teams build real-world NLP systems including experiment tracking, CI-ready deployment, and automated retraining workflows.

## Project Overview

Companies receive massive volumes of customer feedback every day. This project builds a full ML production pipeline that:
- Ingests raw customer feedback (batch + streaming simulation)
- Builds scalable preprocessing + feature pipelines using PySpark
- Trains transformer-based sentiment + topic classifiers (HuggingFace)
- Tracks experiments, metrics, and model versions with MLflow
- Deploys real-time inference through FastAPI
- Supports containerized ML deployment with Docker
- Lays the foundation for monitoring, drift detection, and continuous retraining

## Key Machine Learning Engineering Features
✅ Modular training + inference pipelines  
✅ Transformer fine-tuning with reproducible experiments  
✅ Model registry + version control (MLflow)  
✅ Real-time prediction API for production serving  
✅ CI/CD-ready deployment with Docker  
✅ Designed for monitoring + feedback-driven retraining  

## Tech Stack

| Layer                     | Tools |
|--------------------------|------|
| Distributed Feature Pipelines | PySpark (Databricks CE) |
| Storage + Data Lake       | MinIO |
| Metadata + Warehouse      | PostgreSQL |
| NLP Modeling              | HuggingFace Transformers, TensorFlow |
| Experiment Tracking       | MLflow (runs + registry) |
| Model Serving             | FastAPI |
| Deployment                | Docker |
| Optional UI Dashboard     | Streamlit |

---

## Repo Structure

```
feedback-ml-system/
│
├── data/                   # Sample datasets + labeling artifacts
│
├── src/
│   ├── ingestion/          # Feedback ingestion pipelines (batch/stream)
│   ├── preprocessing/      # Cleaning + feature engineering
│   ├── training/           # Transformer training + evaluation scripts
│   ├── inference/          # Batch + real-time prediction pipeline
│   ├── monitoring/         # Drift + performance monitoring (planned)
│   └── utils/              # Shared helpers
│
├── mlops/
│   ├── mlflow/             # Experiment + model registry configs
│   ├── ci_cd/              # GitHub Actions / pipeline automation
│   └── deployment/         # Deployment manifests
│
├── api/
│   └── main.py             # FastAPI model serving endpoint
│
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
│
├── notebooks/              # Exploration only (not production logic)
│
├── README.md
└── requirements.txt
```