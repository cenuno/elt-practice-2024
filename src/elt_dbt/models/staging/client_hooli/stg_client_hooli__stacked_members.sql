{{ config(materialized="view", tags=["client_hooli", "stg", "contains_pii", "members"]) }}

-- NOTE: in this case, nothing to stack
select {{ get_client_hooli_membership_processed_columns() }}, '{{ relation }}' as relation_name
from {{ source("client_hooli", "processed_hooli_patient_membership_202307") }}
