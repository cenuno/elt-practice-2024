{{
    config(
        materialized="incremental",
        unique_key=["claim_number"],
        on_schema_change="append_new_columns",
        tags=["client_acme", "int", "claims"],
    )
}}

-- For each member_id & claim_number, get the most recent date received
select sca_sc.*
from {{ ref("stg_client_acme__stacked_claims") }} as sca_sc
where
    sca_sc.claim_number is not null
    -- Handle incremental insert and update logic
    {% if is_incremental() %}
        -- Only insert or update records that are newer than the last loaded data
        and sca_sc.modified_on > (
            select max(this.modified_on)
            -- The current table being updated incrementally
            from {{ this }} as this
        )
    {% endif %}
