{% macro get_client_acme_claim_processed_columns() %}
    cast("member_id" as integer) as member_id,
    "client_id",
    "claim_number",
    cast({{ clean_invalid_values("date_received", ["'2023-11-31'"]) }} as date) as "date_received",
    "claim_category",
    "vendor",
    "hospital_service",
    "coding_system",
    "code",
    "primary_diagnosis",
    cast("total_billed" as decimal(20, 10)) AS total_billed,
    "processing_status",
    "client_name",
    "internal_filename",
    "external_filename",
    "created_on",
    "modified_on"
{% endmacro %}
