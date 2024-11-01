{{ config(materialized="view", tags=["client_acme", "stg", "contains_pii", "members"]) }}

-- NOTE: stack all the tables that share the same prefix via UNION ALL
-- AND select and clean particular columns
{{ union_acme_members_by_tables_by_pattern("client_acme", "processed_acme_patient_membership_%") }}
