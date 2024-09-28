{{ 
    config(
        materialized='table',
    ) 
}}

WITH unioned_memberships AS (
    {{ union_tables_by_pattern('client_acme', 'processed_acme_patient_membership_%') }}
)

-- view results
SELECT 
    *
FROM
    unioned_memberships
