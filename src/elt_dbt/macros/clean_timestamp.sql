{% macro clean_membership_end_date(date_column, invalid_dates) %}
    CASE
        WHEN {{ date_column }} IN ({{ invalid_dates | join(', ') }})
            -- NOTE: account for non-existent date stamps
            THEN NULL
        ELSE TO_TIMESTAMP({{ date_column }}, 'YYYY-MM-DD HH24:MI:SS')
    END
{% endmacro %}
