{{
    config(
        materialized="incremental",
        unique_key=["member_id"],
        on_schema_change="append_new_columns",
        tags=["client_hooli", "int", "contains_pii", "members"],
    )
}}

-- For each member_id, get the most recent membership_end_date
with
    cte_stacked_members as (
        select
            sch_sm.*,
            -- Ensure most recent record is marked with value of one
            row_number() over (
                partition by sch_sm.member_id, sch_sm.client_id order by sch_sm.eligibility_date desc
            ) as rn
        from {{ ref("stg_client_hooli__stacked_members") }} as sch_sm
    )

-- Handle incremental insert and update logic
select
    csm.member_id,
    csm.client_id,
    csm.eligibility_date,
    csm.member_fullname,
    csm.gender,
    csm.date_of_birth,
    csm.age_in_mths_no,
    csm.member_address_1,
    csm.member_address_2,
    csm.member_city,
    csm.member_state,
    csm.member_zip,
    csm.member_phone,
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
        and csm.modified_on >= (
            select max(this.modified_on)
            -- The current table being updated incrementally
            from {{ this }} as this
        )
    {% endif %}
