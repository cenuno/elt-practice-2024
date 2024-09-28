{% macro clean_date_of_birth(column) %}
    CASE
        -- NOTE: impossible to be born after the current year
        WHEN SPLIT_PART({{ column }}, ' ', 2) <> '00:00:00' AND SPLIT_PART({{ column }}, ', ', 2)::INT > TO_CHAR(CURRENT_DATE, 'YYYY')::INT 
            THEN NULL
        WHEN SPLIT_PART({{ column }}, ' ', 2) <> '00:00:00' AND SPLIT_PART({{ column }}, ', ', 2)::INT <= TO_CHAR(CURRENT_DATE, 'YYYY')::INT 
            THEN TO_DATE({{ column }}, 'Month DD, YYYY') 
        WHEN SPLIT_PART({{ column }}, ' ', 2) = '00:00:00'
            THEN TO_DATE(SUBSTRING({{ column }}, 1, 10), 'YYYY-MM-DD')
        ELSE NULL
    END
{% endmacro %}