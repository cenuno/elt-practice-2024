{{
    config(
        materialized="view",
        tags=["client_acme", "stg", "claims"]
    )
}}

-- NOTE: stack all the tables that share the same prefix via UNION ALL
-- AND select and clean particular columns
{{ union_acme_claim_by_tables_by_pattern("client_acme", "processed_acme_patient_claim_%") }}
