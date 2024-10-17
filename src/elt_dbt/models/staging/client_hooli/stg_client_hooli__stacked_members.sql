{{ config(materialized="view", tags=["client_hooli", "stg", "contains_pii", "members"]) }}

-- NOTE: stack all the tables that share the same prefix via UNION ALL
-- AND select and clean particular columns
{{ union_hooli_members_by_tables_by_pattern("client_hooli", "processed_hooli_patient_membership_%") }}
