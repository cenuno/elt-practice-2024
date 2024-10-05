{{
    config(
        materialized="view",
    )
}}

-- NOTE: stack all the tables that share the same prefix via UNION ALL
-- AND select and clean particular columns
{{ union_tables_by_pattern("client_acme", "processed_acme_patient_membership_%") }}
