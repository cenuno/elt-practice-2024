SELECT 
	ica_m.member_id, 
	ica_m.membership_end_date, 
	ica_m.phone_number, 
	ica_m.state,
	ica_m.zip,
	ica_m.client_id, 
	ica_m.client_name,
	ica_m.relation_name AS member_relation_name,
	ica_c.member_id IS NOT NULL AS has_claim,
	ica_c.date_received,
	ica_c.claim_category,
	ica_c.vendor,
	ica_c.hospital_service,
	ica_c.coding_system,
	ica_c.code,
	ica_c.primary_diagnosis,
	ica_c.total_billed,
	ica_c.processing_status,
	ica_c.relation_name AS claim_relation_name
FROM cnuno_dev_int_client_acme.int_client_acme__member AS ica_m
LEFT JOIN cnuno_dev_int_client_acme.int_client_acme__claim AS ica_c
	ON ica_m.member_id = ica_c.member_id
ORDER BY ica_m.member_id, ica_c.date_received
;