{{
    config(
        materialized="incremental",
        unique_key=["member_id", "claim_number"],
        on_schema_change="append_new_columns",
        tags=["client_acme", "int", "contains_pii", "member", "claims"],
    )
}}

-- NOTE: for each member, find their claim information
select
    ica_m.member_id,
    ica_m.membership_end_date,
    ica_m.phone_number,
    ica_m.state,
    ica_m.zip,
    ica_m.client_id,
    ica_m.client_name,
    ica_m.relation_name as member_relation_name,
    ica_m.modified_on as member_modified_on,
    ica_c.claim_number,
    ica_c.member_id is not null as has_claim,
    ica_c.date_received,
    extract(year from ica_c.date_received) as year_date_received,
    extract(quarter from ica_c.date_received) as quarter_date_received,
    extract(month from ica_c.date_received) as month_date_received,
    extract(week from ica_c.date_received) as week_date_received,
    extract(dow from ica_c.date_received) as dow_date_received,
    ica_c.claim_category,
    ica_c.vendor,
    ica_c.hospital_service,
    ica_c.coding_system,
    ica_c.code,
    ica_c.primary_diagnosis,
    ica_c.total_billed,
    ica_c.processing_status,
    ica_c.relation_name as claim_relation_name,
    ica_c.modified_on as claim_modified_on
from {{ ref("int_client_acme__member") }} as ica_m
left join {{ ref("int_client_acme__claim") }} as ica_c on ica_m.member_id = ica_c.member_id
-- Handle incremental insert and update logic
{% if is_incremental() %}
    where
        -- Only insert or update records that are newer than the last loaded data
        (
            (
                ica_m.modified_on > (
                    select max(this.member_modified_on)
                    -- The current table being updated incrementally
                    from {{ this }} as this
                )
            )
            or (
                ica_c.modified_on > (
                    select max(this.claim_modified_on)
                    -- The current table being updated incrementally
                    from {{ this }} as this
                )
            )
        )
{% endif %}
order by ica_m.member_id, ica_c.date_received
