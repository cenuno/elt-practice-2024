{% macro clean_phone_number(column) %}
    case
        when length({{ column }}) = 10
        then '1' || {{ column }}
        when length({{ column }}) = 11
        then {{ column }}
        else null
    end
{% endmacro %}
