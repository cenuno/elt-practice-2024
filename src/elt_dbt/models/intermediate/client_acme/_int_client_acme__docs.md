{% docs table_int_client_acme__member %}

This table contains one row per member id where we only keep the latest record based on `membership_end_date` across all `_membership_YYYYMM` tables for client acme.

{% enddocs %}

{% docs table_int_client_acme__claim %}

This table contains one row per member id per claim number across all `_claim_YYYYMM` tables for client acme.

{% enddocs %}

{% docs table_int_client_acme__member_claim %}

This table contains one row per member id per claim number across all `_membership_YYYYMM` and `_claim_YYYYMM` tables for client acme.

{% enddocs %}

{% docs column_has_claim %}

Boolean indicating if a member has a claim or not

{% enddocs %}

{% docs column_year_date_received %}

The year the claim was received

{% enddocs %}

{% docs column_quarter_date_received %}

The quarter the claim was received

{% enddocs %}

{% docs column_month_date_received %}

The month the claim was received

{% enddocs %}

{% docs column_week_date_received %}

The week the claim was received

{% enddocs %}

{% docs column_dow_date_received %}

The day of week the claim was received

{% enddocs %}