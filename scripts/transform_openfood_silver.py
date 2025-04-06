from pyspark.sql import SparkSession
from pyspark.sql.functions import col, upper
from datetime import date
import boto3
import os

# Constants
INPUT_PATH = "data/bronze/openfood_2025-04-05.parquet"
OUTPUT_PATH = f"data/silver/openfood_transformed_{date.today()}.parquet"
BUCKET = "openfood-analytics-luiz"
S3_KEY = f"silver/{date.today()}/openfood_transformed.parquet"

# Start Spark session
spark = SparkSession.builder \
    .appName("TransformOpenFoodFacts") \
    .getOrCreate()

# Read raw data
df = spark.read.parquet(INPUT_PATH)

# Simple transformation: select and rename columns
df_transformed = df.select(
    col("product_name").alias("name"),
    col("brands").alias("brand"),
    col("countries_tags").alias("countries"),
    col("ingredients_text").alias("ingredients"),
    col("nutriscore_score").cast("float"),
    col("nova_group").cast("int")
).filter(col("product_name").isNotNull())

# Save locally as Parquet
df_transformed.write.mode("overwrite").parquet(OUTPUT_PATH)
print(f"Transformed data saved to: {OUTPUT_PATH}")

# Upload to S3
s3 = boto3.client("s3")
s3.upload_file(OUTPUT_PATH, BUCKET, S3_KEY)
print(f"Transformed file uploaded to S3: s3://{BUCKET}/{S3_KEY}")