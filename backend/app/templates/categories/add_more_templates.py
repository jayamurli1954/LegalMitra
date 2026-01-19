"""
Script to add 50+ more templates to reach 100+ total
Run this to expand the template library
"""

# Additional Income Tax Templates (15 more)
income_tax_additional = [
    {"id": "itr_filing_acknowledgement", "name": "ITR Filing Acknowledgement Letter", "category": "income_tax"},
    {"id": "advance_tax_payment_letter", "name": "Advance Tax Payment Letter", "category": "income_tax"},
    {"id": "tax_audit_report_3ca", "name": "Tax Audit Report (Form 3CA)", "category": "income_tax"},
    {"id": "tax_audit_report_3cb", "name": "Tax Audit Report (Form 3CB)", "category": "income_tax"},
    {"id": "form_15g_submission", "name": "Form 15G - No TDS Declaration", "category": "income_tax"},
    {"id": "form_15h_submission", "name": "Form 15H - Senior Citizen No TDS", "category": "income_tax"},
    {"id": "tds_lower_deduction_certificate", "name": "Application for Lower TDS Certificate", "category": "income_tax"},
    {"id": "nil_tds_certificate", "name": "Application for Nil TDS Certificate", "category": "income_tax"},
    {"id": "income_tax_refund_reissue", "name": "Refund Reissue Application", "category": "income_tax"},
    {"id": "pan_aadhaar_link_letter", "name": "PAN-Aadhaar Linking Letter", "category": "income_tax"},
    {"id": "tax_clearance_certificate", "name": "Tax Clearance Certificate Application", "category": "income_tax"},
    {"id": "condonation_delay_letter", "name": "Condonation of Delay Application", "category": "income_tax"},
    {"id": "reassessment_reply", "name": "Reply to Reassessment Notice", "category": "income_tax"},
    {"id": "income_tax_penalty_waiver", "name": "Penalty Waiver Application", "category": "income_tax"},
    {"id": "vivad_se_vishwas_application", "name": "Vivad Se Vishwas Scheme Application", "category": "income_tax"},
]

# Additional Corporate Templates (12 more)
corporate_additional = [
    {"id": "agm_notice", "name": "Annual General Meeting Notice", "category": "corporate"},
    {"id": "egm_notice", "name": "Extraordinary General Meeting Notice", "category": "corporate"},
    {"id": "board_meeting_notice", "name": "Board Meeting Notice", "category": "corporate"},
    {"id": "dividend_declaration_resolution", "name": "Dividend Declaration Resolution", "category": "corporate"},
    {"id": "share_allotment_resolution", "name": "Share Allotment Resolution", "category": "corporate"},
    {"id": "loan_approval_resolution", "name": "Loan Approval Resolution", "category": "corporate"},
    {"id": "change_registered_office", "name": "Change of Registered Office", "category": "corporate"},
    {"id": "increase_authorized_capital", "name": "Increase in Authorized Capital", "category": "corporate"},
    {"id": "appointment_auditor", "name": "Auditor Appointment Resolution", "category": "corporate"},
    {"id": "related_party_transaction", "name": "Related Party Transaction Approval", "category": "corporate"},
    {"id": "roc_aoc4_filing", "name": "AOC-4 Financial Statements Filing", "category": "corporate"},
    {"id": "striking_off_application", "name": "Application for Striking Off Company Name", "category": "corporate"},
]

# Additional Contract Templates (10 more)
contract_additional = [
    {"id": "franchise_agreement", "name": "Franchise Agreement", "category": "contracts"},
    {"id": "distributorship_agreement", "name": "Distributorship Agreement", "category": "contracts"},
    {"id": "licensing_agreement", "name": "Licensing Agreement", "category": "contracts"},
    {"id": "service_level_agreement", "name": "Service Level Agreement (SLA)", "category": "contracts"},
    {"id": "non_compete_agreement", "name": "Non-Compete Agreement", "category": "contracts"},
    {"id": "joint_venture_agreement", "name": "Joint Venture Agreement", "category": "contracts"},
    {"id": "shareholders_agreement", "name": "Shareholders Agreement", "category": "contracts"},
    {"id": "indemnity_bond", "name": "Indemnity Bond", "category": "contracts"},
    {"id": "lease_agreement_commercial", "name": "Commercial Lease Agreement", "category": "contracts"},
    {"id": "memorandum_understanding", "name": "Memorandum of Understanding (MOU)", "category": "contracts"},
]

# Additional Compliance Templates (8 more)
compliance_additional = [
    {"id": "shops_establishments_registration", "name": "Shops & Establishments Registration", "category": "compliance"},
    {"id": "fssai_license_application", "name": "FSSAI License Application", "category": "compliance"},
    {"id": "pollution_control_noc", "name": "Pollution Control NOC Application", "category": "compliance"},
    {"id": "fire_safety_noc", "name": "Fire Safety NOC Application", "category": "compliance"},
    {"id": "trademark_application", "name": "Trademark Registration Application", "category": "compliance"},
    {"id": "copyright_registration", "name": "Copyright Registration Application", "category": "compliance"},
    {"id": "msme_udyam_registration", "name": "MSME Udyam Registration", "category": "compliance"},
    {"id": "import_export_code", "name": "Import Export Code (IEC) Application", "category": "compliance"},
]

# Additional Legal Notice Templates (8 more)
legal_notice_additional = [
    {"id": "employment_termination_notice", "name": "Employment Termination Notice", "category": "legal_notices"},
    {"id": "contract_breach_notice", "name": "Contract Breach Notice", "category": "legal_notices"},
    {"id": "eviction_notice", "name": "Eviction Notice", "category": "legal_notices"},
    {"id": "defamation_notice", "name": "Defamation Legal Notice", "category": "legal_notices"},
    {"id": "trademark_infringement_notice", "name": "Trademark Infringement Notice", "category": "legal_notices"},
    {"id": "copyright_infringement_notice", "name": "Copyright Infringement Notice", "category": "legal_notices"},
    {"id": "cheque_bounce_notice", "name": "Cheque Bounce Legal Notice (Section 138)", "category": "legal_notices"},
    {"id": "recovery_suit_notice", "name": "Recovery Suit Legal Notice", "category": "legal_notices"},
]

# New Category: Banking & Finance Templates (10 templates)
banking_finance = [
    {"id": "loan_application_letter", "name": "Business Loan Application", "category": "banking"},
    {"id": "overdraft_facility_request", "name": "Overdraft Facility Request", "category": "banking"},
    {"id": "bank_guarantee_request", "name": "Bank Guarantee Request", "category": "banking"},
    {"id": "letter_of_credit_application", "name": "Letter of Credit Application", "category": "banking"},
    {"id": "loan_noc_request", "name": "Loan NOC Request", "category": "banking"},
    {"id": "account_closure_letter", "name": "Bank Account Closure Letter", "category": "banking"},
    {"id": "cheque_stop_payment", "name": "Stop Payment Request", "category": "banking"},
    {"id": "balance_confirmation_request", "name": "Balance Confirmation Request", "category": "banking"},
    {"id": "loan_restructuring_request", "name": "Loan Restructuring Request", "category": "banking"},
    {"id": "credit_facility_renewal", "name": "Credit Facility Renewal Request", "category": "banking"},
]

# New Category: Real Estate Templates (8 templates)
real_estate = [
    {"id": "sale_deed", "name": "Property Sale Deed", "category": "real_estate"},
    {"id": "gift_deed", "name": "Property Gift Deed", "category": "real_estate"},
    {"id": "power_of_attorney_property", "name": "Power of Attorney for Property", "category": "real_estate"},
    {"id": "rent_agreement", "name": "Residential Rent Agreement", "category": "real_estate"},
    {"id": "leave_license_agreement", "name": "Leave and License Agreement", "category": "real_estate"},
    {"id": "builder_buyer_agreement", "name": "Builder-Buyer Agreement", "category": "real_estate"},
    {"id": "property_mortgage_deed", "name": "Property Mortgage Deed", "category": "real_estate"},
    {"id": "khata_transfer_application", "name": "Khata Transfer Application", "category": "real_estate"},
]

# Total additional templates: 15 + 12 + 10 + 8 + 8 + 10 + 8 = 71 new templates!

print("Template Expansion Plan")
print("=" * 50)
print(f"Income Tax Additional: {len(income_tax_additional)}")
print(f"Corporate Additional: {len(corporate_additional)}")
print(f"Contracts Additional: {len(contract_additional)}")
print(f"Compliance Additional: {len(compliance_additional)}")
print(f"Legal Notices Additional: {len(legal_notice_additional)}")
print(f"Banking & Finance (NEW): {len(banking_finance)}")
print(f"Real Estate (NEW): {len(real_estate)}")
print("=" * 50)
total_new = (len(income_tax_additional) + len(corporate_additional) +
             len(contract_additional) + len(compliance_additional) +
             len(legal_notice_additional) + len(banking_finance) + len(real_estate))
print(f"Total NEW templates to add: {total_new}")
print(f"Current templates: ~48")
print(f"After expansion: ~{48 + total_new} templates")
