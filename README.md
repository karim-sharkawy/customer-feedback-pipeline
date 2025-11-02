# Scalable NLP Pipeline for Customer Feedback Analysis

A production-style, end-to-end NLP system that ingests, processes, analyzes, and serves customer feedback data using a modern data + AI engineering stack.

## 🚀 Project Overview

This project simulates what real companies use to monitor and understand user sentiment at scale.
* Ingest raw customer feedback (simulated API / batch input)
* Clean and transform data using PySpark on Databricks
* Store data in a MinIO (S3-compatible) data lake and PostgreSQL warehouse
* Perform sentiment + topic classification using TensorFlow + HuggingFace
* Track experiments and models with MLflow
* Serve predictions via FastAPI (real-time API)
* Containerized using Docker (CI/CD-ready)

## 🛠️ Tech Stack (Free/Open Source)

| Layer                  | Tool                    |
| ---------------------- | ----------------------- |
| Distributed Processing | PySpark (Databricks CE) |
| Data Lake              | MinIO (S3-compatible)   |
| Database / Warehouse   | PostgreSQL              |
| AI / NLP Modeling      | TensorFlow, HuggingFace |
| Experiment Tracking    | MLflow                  |
| Model Serving          | FastAPI                 |
| Containerization       | Docker                  |
| Optional Dashboard     | Streamlit               |

## 📂 Project Structure (planned)

```
project_root/
├── data_ingestion/
├── spark_jobs/
├── models/
├── api/
├── mlops/
├── docker/
└── README.md
```

More sections coming soon: Setup, Architecture Diagram, Execution Flow.