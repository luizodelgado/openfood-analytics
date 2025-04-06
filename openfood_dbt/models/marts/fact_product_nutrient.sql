-- models/marts/fact_product_nutrient.sql

{{ config(
    materialized = "table"
) }}

select
    name as product_name
    , brand
    , countries
    , ingredients
    , nutriscore_score
    , nova_group
    , current_date as ingestion_date
from read_parquet('../data/silver/**/*.parquet')
where name is not null