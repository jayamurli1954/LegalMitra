"""Income Tax Templates"""

def get_income_tax_templates():
    """Returns all Income Tax related templates"""
    return [
        {
            "id": "tds_return_filing_letter",
            "name": "TDS Return Filing Letter",
            "category": "income_tax",
            "description": "Covering letter for TDS return filing (Form 24Q, 26Q, 27Q)",
            "applicable_for": ["CA", "Tax Professional", "Corporate"],
            "fields": [
                {
                    "name": "company_name",
                    "label": "Company/Deductor Name",
                    "type": "text",
                    "required": True
                },
                {
                    "name": "tan",
                    "label": "TAN",
                    "type": "text",
                    "required": True,
                    "placeholder": "ABCD12345E"
                },
                {
                    "name": "form_type",
                    "label": "TDS Return Form",
                    "type": "dropdown",
                    "required": True,
                    "options": [
                        "Form 24Q (Salary TDS)",
                        "Form 26Q (Non-Salary TDS)",
                        "Form 27Q (TDS on NRI)",
                        "Form 27EQ (TCS Return)"
                    ]
                },
                {
                    "name": "quarter",
                    "label": "Quarter",
                    "type": "dropdown",
                    "required": True,
                    "options": [
                        "Q1 (Apr-Jun)",
                        "Q2 (Jul-Sep)",
                        "Q3 (Oct-Dec)",
                        "Q4 (Jan-Mar)"
                    ]
                },
                {
                    "name": "financial_year",
                    "label": "Financial Year",
                    "type": "text",
                    "required": True,
                    "placeholder": "2024-25"
                },
                {
                    "name": "total_tax_deducted",
                    "label": "Total Tax Deducted (Rs.)",
                    "type": "number",
                    "required": True
                }
            ],
            "template_text": """To,
The Assessing Officer,
Income Tax Department,
[Ward/Circle]

Date: [DATE]

Subject: Filing of {form_type} for {quarter} of FY {financial_year}

Ref: TAN - {tan}

Respected Sir/Madam,

We, {company_name} (TAN: {tan}), hereby submit the {form_type} for the quarter {quarter} of the Financial Year {financial_year}.

DETAILS OF TDS RETURN:
- Form Type: {form_type}
- Quarter: {quarter}
- Financial Year: {financial_year}
- Total Tax Deducted: Rs. {total_tax_deducted}
- Filing Date: [DATE]

The return has been filed electronically and the acknowledgment is enclosed herewith.

All taxes deducted have been deposited within the prescribed time limits and Form 16/16A have been issued to all deductees.

Kindly process the return and update the TDS credit in the respective deductees' Form 26AS.

Thanking you,

For {company_name}
TAN: {tan}

Authorized Signatory
Name:
Designation:
Place:

Enclosures:
1. TDS Return Acknowledgment
2. Challan Copies
3. Form 27A (if applicable)""",
            "tags": ["TDS", "Income Tax", "Return", "Form 24Q", "Form 26Q"],
            "ai_enhanced": True
        },
        {
            "id": "income_tax_appeal",
            "name": "Income Tax Appeal to CIT(A)",
            "category": "income_tax",
            "description": "Appeal to Commissioner of Income Tax (Appeals) against assessment order",
            "applicable_for": ["CA", "Tax Professional", "Corporate"],
            "fields": [
                {
                    "name": "appellant_name",
                    "label": "Appellant Name",
                    "type": "text",
                    "required": True
                },
                {
                    "name": "pan",
                    "label": "PAN",
                    "type": "text",
                    "required": True
                },
                {
                    "name": "assessment_year",
                    "label": "Assessment Year",
                    "type": "text",
                    "required": True,
                    "placeholder": "2024-25"
                },
                {
                    "name": "order_date",
                    "label": "Date of Assessment Order",
                    "type": "date",
                    "required": True
                },
                {
                    "name": "grounds_of_appeal",
                    "label": "Grounds of Appeal",
                    "type": "multiline",
                    "required": True
                }
            ],
            "template_text": """To,
The Commissioner of Income Tax (Appeals),
[Zone/Range]

APPEAL UNDER SECTION 246A OF THE INCOME TAX ACT, 1961

Assessment Year: {assessment_year}
PAN: {pan}

Appellant: {appellant_name}

GROUNDS OF APPEAL:

{grounds_of_appeal}

[AI will expand with:
1. Detailed grounds with legal provisions
2. Facts of the case
3. Submissions and arguments
4. Prayer for relief
5. Case law citations]

PRAYER:
The appellant prays that this Hon'ble office may be pleased to:
1. Set aside the impugned assessment order
2. Delete the additions/disallowances made
3. Grant any other relief deemed fit

Place:
Date:

Appellant Signature
{appellant_name}
PAN: {pan}""",
            "tags": ["Income Tax", "Appeal", "CIT(A)", "Assessment"],
            "ai_enhanced": True
        },
        {
            "id": "section_154_rectification",
            "name": "Rectification u/s 154",
            "category": "income_tax",
            "description": "Application for rectification of mistakes in income tax order",
            "applicable_for": ["CA", "Tax Professional", "Individual"],
            "fields": [
                {
                    "name": "taxpayer_name",
                    "label": "Taxpayer Name",
                    "type": "text",
                    "required": True
                },
                {
                    "name": "pan",
                    "label": "PAN",
                    "type": "text",
                    "required": True
                },
                {
                    "name": "assessment_year",
                    "label": "Assessment Year",
                    "type": "text",
                    "required": True
                },
                {
                    "name": "mistake_description",
                    "label": "Description of Mistake",
                    "type": "multiline",
                    "required": True
                }
            ],
            "template_text": """To,
The Assessing Officer,
Income Tax Department,
[Ward/Circle]

Subject: Application for Rectification u/s 154 of Income Tax Act

Assessment Year: {assessment_year}
PAN: {pan}

Respected Sir/Madam,

I/We, {taxpayer_name}, submit this application for rectification of the following apparent mistake in the assessment order:

MISTAKE APPARENT FROM RECORD:
{mistake_description}

[AI will expand with detailed explanation and correction requested]

We request rectification of the above mistake and issue a revised order.

Thanking you,

{taxpayer_name}
PAN: {pan}""",
            "tags": ["Income Tax", "Rectification", "Section 154", "Error"],
            "ai_enhanced": True
        },
        {
            "id": "itr1_filing_letter",
            "name": "ITR-1 Filing Acknowledgement Letter",
            "category": "income_tax",
            "description": "Covering letter for ITR-1 (Sahaj) filing",
            "applicable_for": ["CA", "Individual"],
            "fields": [
                {"name": "taxpayer_name", "label": "Taxpayer Name", "type": "text", "required": True},
                {"name": "pan", "label": "PAN", "type": "text", "required": True},
                {"name": "assessment_year", "label": "Assessment Year", "type": "text", "required": True, "placeholder": "2024-25"},
                {"name": "total_income", "label": "Total Income (Rs.)", "type": "number", "required": True},
                {"name": "tax_paid", "label": "Total Tax Paid (Rs.)", "type": "number", "required": True}
            ],
            "template_text": """ITR-1 (SAHAJ) FILING - AY {assessment_year}\nTaxpayer: {taxpayer_name}\nPAN: {pan}\nTotal Income: Rs. {total_income}\nTax Paid: Rs. {tax_paid}\n[AI expands with filing details and refund/demand status]""",
            "tags": ["Income Tax", "ITR-1", "Sahaj", "Filing"],
            "ai_enhanced": True
        },
        {
            "id": "itr4_presumptive",
            "name": "ITR-4 Presumptive Income Filing",
            "category": "income_tax",
            "description": "ITR-4 (Sugam) for presumptive income scheme",
            "applicable_for": ["CA", "Small Business", "Professional"],
            "fields": [
                {"name": "taxpayer_name", "label": "Taxpayer Name", "type": "text", "required": True},
                {"name": "pan", "label": "PAN", "type": "text", "required": True},
                {"name": "business_income", "label": "Gross Business Receipts (Rs.)", "type": "number", "required": True},
                {"name": "presumptive_income", "label": "Presumptive Income (Rs.)", "type": "number", "required": True}
            ],
            "template_text": """ITR-4 (SUGAM) - Presumptive Income\nTaxpayer: {taxpayer_name}\nPAN: {pan}\nGross Receipts: Rs. {business_income}\nPresumptive Income: Rs. {presumptive_income}\n[AI expands]""",
            "tags": ["Income Tax", "ITR-4", "Presumptive", "Section 44AD"],
            "ai_enhanced": True
        },
        {
            "id": "advance_tax_letter",
            "name": "Advance Tax Payment Letter",
            "category": "income_tax",
            "description": "Letter for advance tax payment calculation and deposit",
            "applicable_for": ["CA", "Corporate", "Professional"],
            "fields": [
                {"name": "taxpayer_name", "label": "Taxpayer Name", "type": "text", "required": True},
                {"name": "pan", "label": "PAN", "type": "text", "required": True},
                {"name": "financial_year", "label": "Financial Year", "type": "text", "required": True},
                {"name": "estimated_income", "label": "Estimated Total Income (Rs.)", "type": "number", "required": True},
                {"name": "advance_tax_amount", "label": "Advance Tax Amount (Rs.)", "type": "number", "required": True}
            ],
            "template_text": """ADVANCE TAX PAYMENT - FY {financial_year}\nTaxpayer: {taxpayer_name}\nPAN: {pan}\nEstimated Income: Rs. {estimated_income}\nAdvance Tax: Rs. {advance_tax_amount}\n[AI expands with installment breakup]""",
            "tags": ["Income Tax", "Advance Tax", "Payment"],
            "ai_enhanced": True
        },
        {
            "id": "form_15g_submission",
            "name": "Form 15G Submission (No TDS)",
            "category": "income_tax",
            "description": "Form 15G for no TDS deduction on interest income",
            "applicable_for": ["Individual", "Senior Citizen"],
            "fields": [
                {"name": "declarant_name", "label": "Declarant Name", "type": "text", "required": True},
                {"name": "pan", "label": "PAN", "type": "text", "required": True},
                {"name": "bank_name", "label": "Bank Name", "type": "text", "required": True},
                {"name": "estimated_income", "label": "Estimated Total Income (Rs.)", "type": "number", "required": True}
            ],
            "template_text": """FORM 15G - DECLARATION FOR NO TDS\nDeclarant: {declarant_name}\nPAN: {pan}\nBank: {bank_name}\nEstimated Income: Rs. {estimated_income}\n[AI expands with Form 15G format]""",
            "tags": ["Income Tax", "Form 15G", "No TDS"],
            "ai_enhanced": True
        },
        {
            "id": "form_15h_submission",
            "name": "Form 15H Submission (Senior Citizen)",
            "category": "income_tax",
            "description": "Form 15H for senior citizens - no TDS",
            "applicable_for": ["Senior Citizen", "Individual"],
            "fields": [
                {"name": "declarant_name", "label": "Declarant Name", "type": "text", "required": True},
                {"name": "pan", "label": "PAN", "type": "text", "required": True},
                {"name": "age", "label": "Age", "type": "number", "required": True, "placeholder": "60+"},
                {"name": "bank_name", "label": "Bank Name", "type": "text", "required": True}
            ],
            "template_text": """FORM 15H - SENIOR CITIZEN NO TDS\nDeclarant: {declarant_name}\nPAN: {pan}\nAge: {age}\nBank: {bank_name}\n[AI expands]""",
            "tags": ["Income Tax", "Form 15H", "Senior Citizen", "No TDS"],
            "ai_enhanced": True
        },
        {
            "id": "lower_tds_certificate_197",
            "name": "Lower TDS Certificate Application (197)",
            "category": "income_tax",
            "description": "Application for lower/nil TDS certificate u/s 197",
            "applicable_for": ["CA", "Individual", "Corporate"],
            "fields": [
                {"name": "applicant_name", "label": "Applicant Name", "type": "text", "required": True},
                {"name": "pan", "label": "PAN", "type": "text", "required": True},
                {"name": "financial_year", "label": "Financial Year", "type": "text", "required": True},
                {"name": "lower_rate_requested", "label": "Lower TDS Rate Requested (%)", "type": "number", "required": True},
                {"name": "justification", "label": "Justification for Lower Rate", "type": "multiline", "required": True}
            ],
            "template_text": """APPLICATION FOR LOWER TDS CERTIFICATE u/s 197\nApplicant: {applicant_name}\nPAN: {pan}\nFY: {financial_year}\nLower Rate: {lower_rate_requested}%\nJustification: {justification}\n[AI expands]""",
            "tags": ["Income Tax", "TDS", "Section 197", "Lower Rate"],
            "ai_enhanced": True
        },
        {
            "id": "nil_tds_certificate",
            "name": "Nil TDS Certificate Application",
            "category": "income_tax",
            "description": "Application for NIL TDS certificate",
            "applicable_for": ["CA", "Individual"],
            "fields": [
                {"name": "applicant_name", "label": "Applicant Name", "type": "text", "required": True},
                {"name": "pan", "label": "PAN", "type": "text", "required": True},
                {"name": "reason", "label": "Reason for Nil TDS", "type": "multiline", "required": True}
            ],
            "template_text": """NIL TDS CERTIFICATE APPLICATION\nApplicant: {applicant_name}\nPAN: {pan}\nReason: {reason}\n[AI expands]""",
            "tags": ["Income Tax", "TDS", "Nil Certificate"],
            "ai_enhanced": True
        },
        {
            "id": "tax_audit_3ca",
            "name": "Tax Audit Report (Form 3CA)",
            "category": "income_tax",
            "description": "Tax audit report for entities subject to audit u/s 44AB",
            "applicable_for": ["CA"],
            "fields": [
                {"name": "auditee_name", "label": "Auditee Name", "type": "text", "required": True},
                {"name": "pan", "label": "PAN", "type": "text", "required": True},
                {"name": "assessment_year", "label": "Assessment Year", "type": "text", "required": True},
                {"name": "auditor_name", "label": "Auditor Name", "type": "text", "required": True},
                {"name": "membership_no", "label": "CA Membership No", "type": "text", "required": True}
            ],
            "template_text": """FORM 3CA - TAX AUDIT REPORT\nAuditee: {auditee_name}\nPAN: {pan}\nAY: {assessment_year}\nAuditor: {auditor_name}\nMembership: {membership_no}\n[AI expands with Form 3CA details]""",
            "tags": ["Tax Audit", "Form 3CA", "Section 44AB"],
            "ai_enhanced": True
        },
        {
            "id": "tax_audit_3cb",
            "name": "Tax Audit Report (Form 3CB)",
            "category": "income_tax",
            "description": "Tax audit report Form 3CB",
            "applicable_for": ["CA"],
            "fields": [
                {"name": "auditee_name", "label": "Auditee Name", "type": "text", "required": True},
                {"name": "pan", "label": "PAN", "type": "text", "required": True},
                {"name": "financial_year", "label": "Financial Year", "type": "text", "required": True}
            ],
            "template_text": """FORM 3CB - TAX AUDIT REPORT\nAuditee: {auditee_name}\nPAN: {pan}\nFY: {financial_year}\n[AI expands]""",
            "tags": ["Tax Audit", "Form 3CB"],
            "ai_enhanced": True
        },
        {
            "id": "pan_aadhaar_linking",
            "name": "PAN-Aadhaar Linking Letter",
            "category": "income_tax",
            "description": "Letter for PAN-Aadhaar linking confirmation",
            "applicable_for": ["Individual", "CA"],
            "fields": [
                {"name": "taxpayer_name", "label": "Taxpayer Name", "type": "text", "required": True},
                {"name": "pan", "label": "PAN", "type": "text", "required": True},
                {"name": "aadhaar", "label": "Aadhaar Number", "type": "text", "required": True, "placeholder": "XXXX-XXXX-1234"}
            ],
            "template_text": """PAN-AADHAAR LINKING CONFIRMATION\nName: {taxpayer_name}\nPAN: {pan}\nAadhaar: {aadhaar}\n[AI expands]""",
            "tags": ["Income Tax", "PAN", "Aadhaar", "Linking"],
            "ai_enhanced": False
        },
        {
            "id": "tax_clearance_certificate",
            "name": "Tax Clearance Certificate Application",
            "category": "income_tax",
            "description": "Application for tax clearance certificate",
            "applicable_for": ["Individual", "Corporate", "CA"],
            "fields": [
                {"name": "applicant_name", "label": "Applicant Name", "type": "text", "required": True},
                {"name": "pan", "label": "PAN", "type": "text", "required": True},
                {"name": "purpose", "label": "Purpose", "type": "text", "required": True, "placeholder": "Foreign travel, tender, etc."}
            ],
            "template_text": """TAX CLEARANCE CERTIFICATE APPLICATION\nApplicant: {applicant_name}\nPAN: {pan}\nPurpose: {purpose}\n[AI expands]""",
            "tags": ["Income Tax", "Tax Clearance", "Certificate"],
            "ai_enhanced": True
        },
        {
            "id": "reassessment_reply",
            "name": "Reply to Reassessment Notice",
            "category": "income_tax",
            "description": "Reply to reassessment/reopening notice u/s 148",
            "applicable_for": ["CA", "Tax Professional"],
            "fields": [
                {"name": "taxpayer_name", "label": "Taxpayer Name", "type": "text", "required": True},
                {"name": "pan", "label": "PAN", "type": "text", "required": True},
                {"name": "notice_date", "label": "Notice Date", "type": "date", "required": True},
                {"name": "assessment_year", "label": "Assessment Year", "type": "text", "required": True},
                {"name": "reply_points", "label": "Reply/Objections", "type": "multiline", "required": True}
            ],
            "template_text": """REPLY TO REASSESSMENT NOTICE u/s 148\nTaxpayer: {taxpayer_name}\nPAN: {pan}\nNotice Date: {notice_date}\nAY: {assessment_year}\n\nOBJECTIONS:\n{reply_points}\n[AI expands with legal grounds]""",
            "tags": ["Income Tax", "Reassessment", "Section 148", "Notice Reply"],
            "ai_enhanced": True
        }
    ]
