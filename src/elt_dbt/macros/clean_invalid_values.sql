{% macro clean_invalid_values(column, invalid_values) %}
    CASE
        WHEN {{ column }} IN ({{ invalid_values | join(', ') }})
            THEN NULL
        ELSE {{ column }}
    END
{% endmacro %}
