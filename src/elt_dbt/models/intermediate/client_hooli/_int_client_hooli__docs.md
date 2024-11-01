{% docs table_int_client_hooli__member %}

This table contains one row per member id where we only keep the latest record based on `membership_end_date` across all `_membership_YYYYMM` tables for client hooli.

{% enddocs %}

{% docs table_int_client_hooli__claim %}

This table contains one row per member id per claim number across all `_claim_YYYYMM` tables for client hooli.

{% enddocs %}

{% docs table_int_client_hooli__member_claim %}

This table contains one row per member id per claim number across all `_membership_YYYYMM` and `_claim_YYYYMM` tables for client hooli.

{% enddocs %}
