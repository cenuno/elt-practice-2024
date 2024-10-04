{% macro union_tables_by_pattern(schema, pattern) %}
    {%- set tables = dbt_utils.get_relations_by_pattern(schema, pattern) -%}
    {%- if tables | length == 0 -%}
        -- No tables found matching the pattern
        select null as id
    {%- else -%}
        {%- for table in tables %}
            select {{ get_client_acme_membership_processed_columns() }}, '{{ table }}' as relation_name
            from {{ table }}
            {%- if not loop.last %}
                union all
            {%- endif %}
        {%- endfor %}
    {%- endif %}
{% endmacro %}
