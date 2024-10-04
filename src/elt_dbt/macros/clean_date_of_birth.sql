{% macro clean_date_of_birth(column) %}
    case
        -- NOTE: impossible to be born after the current year
        when
            split_part({{ column }}, ' ', 2) <> '00:00:00'
            and split_part({{ column }}, ', ', 2)::int > to_char(current_date, 'YYYY')::int
        then null
        when
            split_part({{ column }}, ' ', 2) <> '00:00:00'
            and split_part({{ column }}, ', ', 2)::int <= to_char(current_date, 'YYYY')::int
        then to_date({{ column }}, 'Month DD, YYYY')
        when split_part({{ column }}, ' ', 2) = '00:00:00'
        then to_date(substring({{ column }}, 1, 10), 'YYYY-MM-DD')
        else null
    end
{% endmacro %}
