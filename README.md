# 🥫 OpenFood Analytics

This is a complete data engineering project designed to ingest, process, and analyze product data from the [Open Food Facts](https://world.openfoodfacts.org/) public API.

## 🎯 Objectives

- Practice key data engineering concepts with real-world data
- Build a modular, cloud-based pipeline with open-source tools
- Enable scalable ingestion, transformation, and analysis workflows

## 🛠️ Tech Stack

- **Python 3.10**
- **Pandas & PyArrow**
- **Apache Airflow**
- **AWS S3 (Free Tier)**
- **PySpark**
- **Poetry / venv + pip**
- **Git & GitHub**

## 📂 Project Structure

```
openfood-analytics/
├── data/                   # Local data (ignored by Git)
│   └── bronze/             # Raw Parquet files from API
├── dags/                   # Airflow DAGs
├── scripts/                # Python scripts (ingestion, transformation, etc.)
├── venv/                   # Virtual environment (ignored by Git)
├── .gitignore
├── README.md
└── requirements.txt
```

## 🚀 Pipeline Overview

1. **Ingestion**: Collect product data from the Open Food Facts API in pages
2. **Normalization**: Flatten nested JSON into tabular format
3. **Serialization**: Save data as Parquet in the local `data/bronze/` layer
4. **Cloud Upload**: Send data to an S3 bucket
5. **Transformation (next step)**: Use PySpark to clean and structure silver layer
6. **Orchestration (next step)**: Schedule all steps using Airflow DAGs

## 🧪 Running Locally

```bash
# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run ingestion script
python scripts/ingest_openfood_api.py

