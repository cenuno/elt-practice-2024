{% macro union_tables_by_pattern(schema, pattern) %}
    {%- set tables = dbt_utils.get_relations_by_pattern(schema, pattern) -%}
    {%- if tables | length == 0 -%}
        -- No tables found matching the pattern
        SELECT NULL AS id
    {%- else -%}
        {%- for table in tables %}
            SELECT 
                {{ get_client_acme_membership_processed_columns() }} 
            FROM {{ table }}
            {%- if not loop.last %} 
            UNION ALL
            {%- endif %}
        {%- endfor %}
    {%- endif %}
{% endmacro %}
