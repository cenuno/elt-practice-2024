{{
    config(
        materialized="incremental",
        unique_key=["member_id"],
        on_schema_change="append_new_columns",
    )
}}

with cte_members as ({{ union_tables_by_pattern("client_acme", "processed_acme_patient_membership_%") }})

-- Handle incremental insert and update logic
select
    cm.member_id,
    cm.client_id,
    cm.membership_end_date,
    cm.member_first_name,
    cm.member_middle_name,
    cm.member_last_name,
    cm.gender,
    cm.date_of_birth,
    cm.address,
    cm.city,
    cm.state,
    cm.zip,
    cm.phone_number,
    cm.ethnicity,
    cm.client_name,
    cm.internal_filename,
    cm.external_filename,
    cm.created_on,
    cm.modified_on,
    cm.relation_name
from
    (
        -- For each member_id, get the most recent membership_end_date
        select
            cte_members.*,
            -- Ensure most recent record is marked with value of one
            row_number() over (
                partition by cte_members.member_id, cte_members.client_id order by cte_members.membership_end_date desc
            ) as rn
        from cte_members
    ) as cm
where
    cm.rn = 1

    {% if is_incremental() %}

        -- Only insert or update records that are newer than the last loaded data
        and cm.modified_on > (
            select max(modified_on)
            -- The current table being updated incrementally
            from {{ this }}
        )

    {% endif %}
