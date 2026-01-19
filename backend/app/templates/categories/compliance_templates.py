"""Compliance Templates"""

def get_compliance_templates():
    """Returns all compliance-related templates"""
    return [
        {
            "id": "pf_compliance_report",
            "name": "PF Compliance Report",
            "category": "compliance",
            "description": "Provident Fund compliance report and certification",
            "applicable_for": ["CA", "Corporate", "HR"],
            "fields": [
                {
                    "name": "company_name",
                    "label": "Company Name",
                    "type": "text",
                    "required": True
                },
                {
                    "name": "pf_code",
                    "label": "PF Code Number",
                    "type": "text",
                    "required": True
                },
                {
                    "name": "month_year",
                    "label": "Month & Year",
                    "type": "text",
                    "required": True,
                    "placeholder": "January 2024"
                },
                {
                    "name": "total_employees",
                    "label": "Total Employees",
                    "type": "number",
                    "required": True
                },
                {
                    "name": "members_list",
                    "label": "Members/Employees Details",
                    "type": "multiline",
                    "required": False,
                    "placeholder": "Employee Name 1 - UAN: 123456789012 - Contribution: Rs. 1,800\nEmployee Name 2 - UAN: 123456789013 - Contribution: Rs. 2,000",
                    "help_text": "List all PF members with their name, UAN, and contribution amount"
                },
                {
                    "name": "total_pf_amount",
                    "label": "Total PF Amount (Rs.)",
                    "type": "number",
                    "required": True
                }
            ],
            "template_text": """PROVIDENT FUND COMPLIANCE REPORT

Company: {company_name}
PF Code: {pf_code}
Period: {month_year}

SUMMARY:
- Total Employees: {total_employees}
- Total PF Contribution: Rs. {total_pf_amount}

MEMBER-WISE DETAILS:
{members_list}

[AI will expand with:
- Detailed PF calculations
- Employee-wise breakup if not provided above
- Payment dates
- Compliance status
- ECR filing confirmation]

CERTIFICATION:
We certify that PF contributions for {month_year} have been deposited within due date.

Authorized Signatory
For {company_name}
Date:""",
            "tags": ["PF", "Compliance", "Labor", "HR"],
            "ai_enhanced": True
        },
        {
            "id": "esi_compliance_report",
            "name": "ESI Compliance Report",
            "category": "compliance",
            "description": "Employee State Insurance compliance report",
            "applicable_for": ["CA", "Corporate", "HR"],
            "fields": [
                {
                    "name": "company_name",
                    "label": "Company Name",
                    "type": "text",
                    "required": True
                },
                {
                    "name": "esi_code",
                    "label": "ESI Code Number",
                    "type": "text",
                    "required": True
                },
                {
                    "name": "period",
                    "label": "Period",
                    "type": "text",
                    "required": True
                },
                {
                    "name": "total_esi_amount",
                    "label": "Total ESI Amount (Rs.)",
                    "type": "number",
                    "required": True
                }
            ],
            "template_text": """ESI COMPLIANCE REPORT

Company: {company_name}
ESI Code: {esi_code}
Period: {period}

Total ESI Contribution: Rs. {total_esi_amount}

[AI will expand with detailed ESI compliance details]

Certified by:
Authorized Signatory
Date:""",
            "tags": ["ESI", "Compliance", "Labor", "HR"],
            "ai_enhanced": True
        },
        {
            "id": "gst_annual_return",
            "name": "GST Annual Return (GSTR-9) Covering Letter",
            "category": "compliance",
            "description": "Covering letter for GST annual return filing",
            "applicable_for": ["CA", "Tax Professional", "Corporate"],
            "fields": [
                {
                    "name": "taxpayer_name",
                    "label": "Taxpayer Name",
                    "type": "text",
                    "required": True
                },
                {
                    "name": "gstin",
                    "label": "GSTIN",
                    "type": "text",
                    "required": True
                },
                {
                    "name": "financial_year",
                    "label": "Financial Year",
                    "type": "text",
                    "required": True,
                    "placeholder": "2023-24"
                },
                {
                    "name": "total_turnover",
                    "label": "Total Annual Turnover (Rs.)",
                    "type": "number",
                    "required": True
                }
            ],
            "template_text": """To,
The Jurisdictional GST Officer,

Subject: Filing of Annual Return in Form GSTR-9 for FY {financial_year}

GSTIN: {gstin}

Respected Sir/Madam,

We, {taxpayer_name} (GSTIN: {gstin}), hereby file our Annual Return in Form GSTR-9 for the Financial Year {financial_year}.

Annual Turnover: Rs. {total_turnover}

[AI will expand with reconciliation details, certifications, etc.]

Thanking you,

For {taxpayer_name}
Authorized Signatory
Date:""",
            "tags": ["GST", "Annual Return", "GSTR-9", "Compliance"],
            "ai_enhanced": True
        },
        {
            "id": "tds_certificate_compliance",
            "name": "TDS Compliance Certificate (Form 16/16A)",
            "category": "compliance",
            "description": "TDS certificate issuance and compliance report",
            "applicable_for": ["CA", "Corporate", "HR"],
            "fields": [
                {
                    "name": "deductor_name",
                    "label": "Deductor Name (Company)",
                    "type": "text",
                    "required": True
                },
                {
                    "name": "tan",
                    "label": "TAN",
                    "type": "text",
                    "required": True
                },
                {
                    "name": "financial_year",
                    "label": "Financial Year",
                    "type": "text",
                    "required": True,
                    "placeholder": "2023-24"
                },
                {
                    "name": "quarter",
                    "label": "Quarter",
                    "type": "dropdown",
                    "required": True,
                    "options": ["Q1 (Apr-Jun)", "Q2 (Jul-Sep)", "Q3 (Oct-Dec)", "Q4 (Jan-Mar)"]
                },
                {
                    "name": "total_tds_deducted",
                    "label": "Total TDS Deducted (Rs.)",
                    "type": "number",
                    "required": True
                }
            ],
            "template_text": """TDS COMPLIANCE CERTIFICATE

Deductor: {deductor_name}
TAN: {tan}
FY: {financial_year} - {quarter}

Total TDS Deducted: Rs. {total_tds_deducted}

[AI will expand with Form 16/16A format, payment details, challan references]

CERTIFICATION:
All TDS has been deducted and deposited as per Income Tax Act, 1961.

Authorized Signatory
Date:""",
            "tags": ["TDS", "Compliance", "Form 16", "Tax"],
            "ai_enhanced": True
        },
        {
            "id": "statutory_audit_report",
            "name": "Statutory Audit Report",
            "category": "compliance",
            "description": "Statutory audit report u/s 143 Companies Act",
            "applicable_for": ["CA"],
            "fields": [
                {
                    "name": "company_name",
                    "label": "Company Name",
                    "type": "text",
                    "required": True
                },
                {
                    "name": "cin",
                    "label": "CIN",
                    "type": "text",
                    "required": True
                },
                {
                    "name": "financial_year",
                    "label": "Financial Year",
                    "type": "text",
                    "required": True
                },
                {
                    "name": "auditor_name",
                    "label": "Auditor Name",
                    "type": "text",
                    "required": True
                },
                {
                    "name": "firm_registration",
                    "label": "Firm Registration Number",
                    "type": "text",
                    "required": True
                },
                {
                    "name": "audit_opinion",
                    "label": "Audit Opinion",
                    "type": "dropdown",
                    "required": True,
                    "options": ["Unmodified", "Qualified", "Adverse", "Disclaimer"]
                }
            ],
            "template_text": """INDEPENDENT AUDITOR'S REPORT

To the Members of {company_name}
CIN: {cin}

Report on Audit of Financial Statements for FY {financial_year}

OPINION:
{audit_opinion} Opinion

[AI will expand with full statutory audit report format, basis of opinion, key audit matters, etc.]

For {auditor_name}
Chartered Accountants
Firm Registration: {firm_registration}

Date:
Place:""",
            "tags": ["Audit", "Statutory Audit", "Companies Act", "CA"],
            "ai_enhanced": True
        },
        {
            "id": "professional_tax_return",
            "name": "Professional Tax Return",
            "category": "compliance",
            "description": "Professional tax compliance return",
            "applicable_for": ["CA", "Corporate", "HR"],
            "fields": [
                {
                    "name": "employer_name",
                    "label": "Employer Name",
                    "type": "text",
                    "required": True
                },
                {
                    "name": "pt_registration_no",
                    "label": "Professional Tax Registration No.",
                    "type": "text",
                    "required": True
                },
                {
                    "name": "return_period",
                    "label": "Return Period",
                    "type": "text",
                    "required": True,
                    "placeholder": "April 2024 - March 2025"
                },
                {
                    "name": "total_employees",
                    "label": "Total Employees",
                    "type": "number",
                    "required": True
                },
                {
                    "name": "total_pt_collected",
                    "label": "Total PT Collected (Rs.)",
                    "type": "number",
                    "required": True
                }
            ],
            "template_text": """PROFESSIONAL TAX RETURN

Employer: {employer_name}
PT Reg. No.: {pt_registration_no}
Period: {return_period}

Total Employees: {total_employees}
Total PT Collected: Rs. {total_pt_collected}

[AI will expand with month-wise breakup, payment challans, etc.]

Authorized Signatory
Date:""",
            "tags": ["Professional Tax", "PT", "Compliance", "State Tax"],
            "ai_enhanced": True
        },
        {
            "id": "fssai_compliance_report",
            "name": "FSSAI Compliance Report",
            "category": "compliance",
            "description": "Food Safety compliance report",
            "applicable_for": ["Food Business", "Corporate"],
            "fields": [
                {
                    "name": "business_name",
                    "label": "Business Name",
                    "type": "text",
                    "required": True
                },
                {
                    "name": "fssai_license_no",
                    "label": "FSSAI License Number",
                    "type": "text",
                    "required": True
                },
                {
                    "name": "compliance_period",
                    "label": "Compliance Period",
                    "type": "text",
                    "required": True
                },
                {
                    "name": "compliance_status",
                    "label": "Compliance Status",
                    "type": "dropdown",
                    "required": True,
                    "options": ["Fully Compliant", "Partial Compliance", "Non-Compliant"]
                }
            ],
            "template_text": """FSSAI COMPLIANCE REPORT

Business: {business_name}
FSSAI License: {fssai_license_no}
Period: {compliance_period}

Compliance Status: {compliance_status}

[AI will expand with hygiene standards, testing reports, documentation compliance, etc.]

Food Safety Officer/Manager
Signature:
Date:""",
            "tags": ["FSSAI", "Food Safety", "Compliance", "License"],
            "ai_enhanced": True
        },
        {
            "id": "labour_welfare_compliance",
            "name": "Labour Welfare Fund Compliance",
            "category": "compliance",
            "description": "Labour Welfare Fund compliance report",
            "applicable_for": ["CA", "Corporate", "HR"],
            "fields": [
                {
                    "name": "employer_name",
                    "label": "Employer Name",
                    "type": "text",
                    "required": True
                },
                {
                    "name": "lwf_registration",
                    "label": "LWF Registration Number",
                    "type": "text",
                    "required": True
                },
                {
                    "name": "period",
                    "label": "Period",
                    "type": "text",
                    "required": True
                },
                {
                    "name": "total_contribution",
                    "label": "Total LWF Contribution (Rs.)",
                    "type": "number",
                    "required": True
                }
            ],
            "template_text": """LABOUR WELFARE FUND COMPLIANCE REPORT

Employer: {employer_name}
LWF Reg. No.: {lwf_registration}
Period: {period}

Total Contribution: Rs. {total_contribution}

[AI will expand with employee-wise contribution, payment details, etc.]

Authorized Signatory
Date:""",
            "tags": ["LWF", "Labour", "Compliance", "Welfare Fund"],
            "ai_enhanced": True
        }
    ]
