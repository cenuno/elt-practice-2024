{% macro clean_invalid_values(column, invalid_values) %}
    case when {{ column }} in ({{ invalid_values | join(", ") }}) then null else {{ column }} end
{% endmacro %}
