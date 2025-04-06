{{ config(
    materialized = "table"
) }}

with trim_brand as (
    select distinct
        trim(brand) as brand_name
    from {{ ref('fact_product_nutrient') }}
    where product_name is not null
)

select
    row_number() over () as brand_id
    , brand_name
from trim_brand