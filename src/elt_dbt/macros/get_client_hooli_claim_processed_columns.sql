{% macro get_client_hooli_claim_processed_columns() %}
    "claim_category",
    cast("member_id" as integer) as "member_id",
    "claim_number",
    cast({{ clean_invalid_values("date_received", ["'2023-11-31'"]) }} as date) as "date_received",
    "hospital_service",
    "code_system",
    "code",
    "diagnosis_type",
    cast("cost_total" as decimal(20, 10)) as "cost_total",
    "status",
    "client_name",
    "client_id",
    "internal_filename",
    "external_filename",
    "created_on",
    "modified_on"
{% endmacro %}
