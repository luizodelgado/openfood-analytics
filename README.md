# 🥫 OpenFood Analytics

This is a complete data engineering project designed to ingest, process, and analyze product data from the [Open Food Facts](https://world.openfoodfacts.org/) public API.

## 🎯 Objectives

- Practice key data engineering concepts with real-world data  
- Build a modular, cloud-based pipeline with open-source tools  
- Enable scalable ingestion, transformation, and analysis workflows  

## 🛠️ Tech Stack

- **Python 3.10**
- **PySpark**
- **Pandas & PyArrow**
- **DuckDB**
- **dbt + DuckDB adapter**
- **Apache Airflow**
- **AWS S3 (Free Tier)**
- **Poetry / venv + pip**
- **Git & GitHub**

## 📂 Project Structure

```
.
└── openfood-analytics/
    ├── dags/        # Airflow DAGs
    ├── data/        # Local data (ignored by Git)/
    │   ├── bronze/      # Raw Parquet files from API
    │   ├── silver/      # Cleaned data (PySpark)
    │   └── gold/        # Final analytical tables (dbt + DuckDB)
    ├── dbt/         # dbt structure
    ├── notebooks/   # Exploration and analysis
    ├── scripts/     # Python scripts (ingestion, transformation, etc)
    ├── venv/        # Virtual environment (ignored by Git)
    ├── .gitignore
    ├── RREADME.md
    └── requirements.txt 
```

## 🚀 Pipeline Overview

1. **Ingestion**: Collect product data from the Open Food Facts API in pages  
2. **Normalization**: Flatten nested JSON into tabular format  
3. **Serialization**: Save data as Parquet in the local `data/bronze/` layer  
4. **Cloud Upload**: Send data to an S3 bucket  
5. **Transformation (Silver)**: Use PySpark to clean and structure the silver layer  
6. **Modeling (Gold)**: Use dbt with DuckDB to create analytical models from the silver data  
7. **Exploration**: Query the DuckDB file locally using DBeaver or SQL engines  
8. **Orchestration (next step)**: Schedule all steps using Airflow DAGs

## 🟡 Gold Modeling with dbt

The project uses [dbt](https://www.getdbt.com/) with the [DuckDB adapter](https://docs.getdbt.com/docs/build/projects/using-duckdb) to model the gold layer locally and without costs.

- The gold layer is built on top of the silver `.parquet` files using SQL models
- A local `openfood.duckdb` file is generated at `data/gold/openfood.duckdb`
- Tables include:
  - `fact_product_nutrient`: flattened product data with nutrition score and region
  - `dim_marca`: brand dimension table with unique brand names
- This DuckDB file can be explored in tools like **DBeaver**, **Metabase**, or even **Python notebooks**

Example query:

```sql
SELECT brand_name, COUNT(*) 
FROM fact_product_nutrient 
GROUP BY brand_name 
ORDER BY COUNT(*) DESC;
```

## 🧪 Running Locally

```bash
# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run ingestion script
python scripts/ingest_openfood_api.py

# Run silver transformation
python scripts/transform_openfood_silver.py

# Run gold modeling (from inside openfood_dbt)
cd openfood_dbt
dbt run
```

