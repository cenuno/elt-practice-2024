{{
    config(
        materialized="incremental",
        unique_key=["member_id"],
        on_schema_change="append_new_columns",
    )
}}

-- For each member_id, get the most recent membership_end_date
with
    cte_stacked_members as (
        select
            sca_sm.*,
            -- Ensure most recent record is marked with value of one
            row_number() over (
                partition by sca_sm.member_id, sca_sm.client_id order by sca_sm.membership_end_date desc
            ) as rn
        from {{ ref("stg_client_acme__stacked_members") }} as sca_sm
    )

-- Handle incremental insert and update logic
select
    csm.member_id,
    csm.client_id,
    csm.membership_end_date,
    csm.member_first_name,
    csm.member_middle_name,
    csm.member_last_name,
    csm.gender,
    csm.date_of_birth,
    csm.address,
    csm.city,
    csm.state,
    csm.zip,
    csm.phone_number,
    csm.ethnicity,
    csm.client_name,
    csm.internal_filename,
    csm.external_filename,
    csm.created_on,
    csm.modified_on,
    csm.relation_name
from cte_stacked_members as csm
where
    csm.rn = 1
    {% if is_incremental() %}
        -- Only insert or update records that are newer than the last loaded data
        and csm.modified_on > (
            select max(this.modified_on)
            -- The current table being updated incrementally
            from {{ this }} as this
        )
    {% endif %}
