{{ config(materialized="view", tags=["client_hooli", "stg", "claims"]) }}

-- NOTE: stack all the tables that share the same prefix via UNION ALL
-- AND select and clean particular columns
{{ union_hooli_claim_by_tables_by_pattern("client_hooli", "processed_hooli_patient_claim_%") }}
