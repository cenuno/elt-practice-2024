
{% docs column_member_id %}

Member id given to us by client acme that unique identifies a member.

{% enddocs %}

{% docs column_client_id %}

Client ID that uniquely identifies client acme.

{% enddocs %}

{% docs column_membership_end_date %}

Member id given to us by client acme

{% enddocs %}

{% docs column_client_name %}

Name of client where member originated from

{% enddocs %}

{% docs column_internal_filename %}

Internal filename of processed CSV that we processed from client

{% enddocs %}

{% docs column_external_filename %}

External filename of raw CSV given to us by client

{% enddocs %}

{% docs column_created_on %}

The timestamp when we originally processed the file associated with his member

{% enddocs %}

{% docs column_modified_on %}

The timestamp when we updated a particular member. If no update has occurred, the value should match the created_on column.

{% enddocs %}

{% docs column_relation_name %}

The name of the relation in schema.table_name format that data originated from in the database.

{% enddocs %}

{% docs column_date_of_birth %}

Member's date of birth

{% enddocs %}

{% docs source_client_acme_description %}

Client specific schema that contains member and claim information on a monthly basis

{% enddocs %}

{% docs column_claim_category %}

Healthcare claims can be divided into several categories, often based on the type of service provided or the part of the healthcare system involved. Examples include medical, dental, pharmacy, mental health, durable medical equipment and home health claims.

{% enddocs %}

{% docs column_claim_number %}

A claim number is a unique identifier assigned to each healthcare claim by the insurance company or healthcare provider. This number helps track and manage the specific claim throughout the payment process. When a claim is submitted to the insurance company, it is assigned a claim number that will be used for all related communications, processing, and follow-up actions.

{% enddocs %}

{% docs column_date_received %}

The date the formal request was made by a healthcare provider (like a doctor, hospital, or pharmacy) to an insurance company to receive payment for services rendered to a patient.

{% enddocs %}

{% docs column_vendor %}

Vendors are third-party companies that provide essential services and technologies to facilitate the healthcare claims process. They work with healthcare providers, hospitals, and insurance companies to streamline operations.

{% enddocs %}

{% docs column_hospital_service %}

Hospital systems are healthcare networks that often include multiple hospitals, clinics, and outpatient services. They are responsible for generating and submitting claims for the services they provide to patients.

{% enddocs %}

{% docs column_coding_system %}

Coding systems are critical to accurately documenting the medical services provided in a standardized way that insurers can interpret. They ensure that healthcare claims are processed correctly and that providers are reimbursed according to the services rendered. Example coding systems are ICD Codes (International Classification of Diseases), CPT Codes (Current Procedural Terminology), HCPCS Codes (Healthcare Common Procedure Coding System), and DRG Codes (Diagnosis-Related Groups).

{% enddocs %}

{% docs column_code %}

Healthcare claims use a variety of codes to identify the patient, services, and equipment, and to communicate adjustments to the claim. The code depends on the coding system used.

{% enddocs %}

{% docs column_primary_diagnosis %}

The primary diagnosis refers to the main medical condition that led the patient to seek care or that was treated during the healthcare encounter. It is the chief reason for the services provided and is represented using an ICD (International Classification of Diseases) code.

{% enddocs %}

{% docs column_total_billed %}

The total billed amount refers to the total cost of all services, treatments, procedures, and items (such as medications or equipment) provided to the patient during their healthcare encounter. This is the full amount that the healthcare provider charges for the services, which is submitted to the insurance company for reimbursement.

{% enddocs %}

{% docs column_processing_status %}

The processing status refers to the current stage in the insurance claim’s lifecycle, indicating whether the claim has been reviewed, approved, denied, or is still under evaluation. It helps track how far along the claim is in being resolved.

{% enddocs %}