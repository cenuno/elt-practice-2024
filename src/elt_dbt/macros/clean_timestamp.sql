{% macro clean_membership_end_date(date_column, invalid_dates) %}
    case
        when {{ date_column }} in ({{ invalid_dates | join(", ") }})
        -- NOTE: account for non-existent date stamps
        then null
        else to_timestamp({{ date_column }}, 'YYYY-MM-DD HH24:MI:SS')
    end
{% endmacro %}
