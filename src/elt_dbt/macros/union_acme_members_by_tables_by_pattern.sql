{% macro union_acme_members_by_tables_by_pattern(schema, pattern) %}
    {# comment log("schema: " ~ schema ~ " pattern: " ~ pattern, info=True) #}
    -- NOTE: usage of dbt_utils.get_relations_by_pattern() resulted in breaking data lineage
    -- WARN: do not try to refactor as its more important that we retain data lineage
    -- TODO: find a way to dynamic fetch source tables without breaking data lineage
    {%- set relations = [
        "processed_acme_patient_membership_202307",
        "processed_acme_patient_membership_202308",
    ] -%}
    {# log("relations: " ~ relations, info=True) #}
    {%- for relation in relations %}
        select {{ get_client_acme_membership_processed_columns() }}, '{{ relation }}' as relation_name
        from {{ source(schema, relation) }}
        {%- if not loop.last %}
            union all
        {%- endif %}
    {%- endfor %}
{% endmacro %}
