{% macro clean_phone_number(column) %}
    CASE
        WHEN LENGTH({{ column }}) = 10
                    THEN '1' || {{column}}
        WHEN LENGTH({{ column }}) = 11
                    THEN {{ column }}
        ELSE NULL
    END
{% endmacro %}
