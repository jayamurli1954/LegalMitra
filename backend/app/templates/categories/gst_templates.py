"""GST Templates"""

def get_gst_templates():
    """Returns all GST-related templates"""
    return [
        {
            "id": "gst_refund_application",
            "name": "GST Refund Application",
            "category": "gst",
            "description": "Application for claiming GST refund under various categories",
            "applicable_for": ["CA", "Tax Professional", "Corporate"],
            "fields": [
                {
                    "name": "applicant_name",
                    "label": "Applicant/Company Name",
                    "type": "text",
                    "required": True,
                    "placeholder": "ABC Private Limited"
                },
                {
                    "name": "gstin",
                    "label": "GSTIN",
                    "type": "text",
                    "required": True,
                    "placeholder": "29AAAAA0000A1Z5"
                },
                {
                    "name": "refund_type",
                    "label": "Type of Refund",
                    "type": "dropdown",
                    "required": True,
                    "options": [
                        "Export of goods/services",
                        "Inverted duty structure",
                        "Excess tax payment",
                        "ITC accumulated",
                        "Zero-rated supplies"
                    ]
                },
                {
                    "name": "refund_amount",
                    "label": "Refund Amount (Rs.)",
                    "type": "number",
                    "required": True,
                    "placeholder": "100000"
                },
                {
                    "name": "tax_period",
                    "label": "Tax Period",
                    "type": "text",
                    "required": True,
                    "placeholder": "April 2024 - June 2024"
                }
            ],
            "template_text": """To,
The Jurisdictional GST Officer,
GST Department,
[Office Address]

Date: [DATE]

Subject: Application for GST Refund - {refund_type}

Ref: GSTIN - {gstin}

Respected Sir/Madam,

We, {applicant_name} (GSTIN: {gstin}), hereby submit this application for claiming refund of GST amounting to Rs. {refund_amount} for the tax period {tax_period}.

DETAILS OF REFUND CLAIM:
- Type of Refund: {refund_type}
- Amount Claimed: Rs. {refund_amount}
- Tax Period: {tax_period}
- GSTIN: {gstin}

[AI will expand this section with:
1. Detailed justification for refund claim
2. Relevant provisions of CGST/SGST Act
3. Documentary evidence and supporting details
4. Computation of refund amount
5. Bank account details for refund credit]

PRAYER:
We request your good office to process this refund application and credit the eligible amount to our registered bank account.

Thanking you,

For {applicant_name}
GSTIN: {gstin}

Authorized Signatory
Name:
Designation:
Date:
Place:

Enclosures:
1. Invoice copies
2. Shipping bills/Export documents
3. Bank statements
4. Computation statement
5. Other supporting documents""",
            "tags": ["GST", "Refund", "Export", "Tax"],
            "ai_enhanced": True
        },
        {
            "id": "gst_registration_application",
            "name": "GST Registration Application",
            "category": "gst",
            "description": "Application for new GST registration",
            "applicable_for": ["CA", "Tax Professional", "Corporate"],
            "fields": [
                {
                    "name": "business_name",
                    "label": "Legal Business Name",
                    "type": "text",
                    "required": True
                },
                {
                    "name": "pan",
                    "label": "PAN",
                    "type": "text",
                    "required": True,
                    "placeholder": "AAAAA0000A"
                },
                {
                    "name": "business_type",
                    "label": "Business Type",
                    "type": "dropdown",
                    "required": True,
                    "options": [
                        "Proprietorship",
                        "Partnership",
                        "Private Limited Company",
                        "Public Limited Company",
                        "LLP"
                    ]
                },
                {
                    "name": "business_address",
                    "label": "Principal Place of Business",
                    "type": "multiline",
                    "required": True
                },
                {
                    "name": "business_activity",
                    "label": "Nature of Business Activity",
                    "type": "multiline",
                    "required": True
                }
            ],
            "template_text": """APPLICATION FOR GST REGISTRATION

1. BUSINESS DETAILS:
   Legal Name: {business_name}
   PAN: {pan}
   Business Type: {business_type}

2. PRINCIPAL PLACE OF BUSINESS:
{business_address}

3. NATURE OF BUSINESS ACTIVITY:
{business_activity}

[AI will expand with:
- Complete Form GST REG-01 details
- Director/Partner/Proprietor information
- Authorized signatory details
- Bank account information
- HSN/SAC codes of goods/services
- Expected turnover
- State-specific requirements]

DECLARATION:
I hereby declare that the information provided is true and correct.

Applicant Signature:
Name:
Date:
Place:

Documents Enclosed:
1. PAN Card
2. Aadhaar Card
3. Business address proof
4. Bank account statement
5. Photographs
6. Authorization letter (if applicable)""",
            "tags": ["GST", "Registration", "New Business", "Compliance"],
            "ai_enhanced": True
        },
        {
            "id": "gst_notice_reply",
            "name": "GST Notice Reply Template",
            "category": "gst",
            "description": "Reply to GST department show cause notice or demand notice",
            "applicable_for": ["CA", "Tax Professional", "Corporate"],
            "fields": [
                {
                    "name": "taxpayer_name",
                    "label": "Taxpayer/Company Name",
                    "type": "text",
                    "required": True,
                    "placeholder": "ABC Private Limited"
                },
                {
                    "name": "gstin",
                    "label": "GSTIN",
                    "type": "text",
                    "required": True,
                    "placeholder": "29AAAAA0000A1Z5"
                },
                {
                    "name": "notice_number",
                    "label": "Notice Reference Number",
                    "type": "text",
                    "required": True,
                    "placeholder": "GST/SCN/2025/1234"
                },
                {
                    "name": "notice_date",
                    "label": "Notice Date",
                    "type": "date",
                    "required": True
                },
                {
                    "name": "notice_type",
                    "label": "Type of Notice",
                    "type": "dropdown",
                    "required": True,
                    "options": [
                        "Show Cause Notice",
                        "Demand Notice",
                        "Audit Notice",
                        "Scrutiny Notice",
                        "Other"
                    ]
                },
                {
                    "name": "reply_points",
                    "label": "Key Points for Reply",
                    "type": "multiline",
                    "required": True,
                    "placeholder": "List main points you want to address in the reply"
                }
            ],
            "template_text": """To,
The Designated Officer
GST Department,
[Office Address]

Date: [DATE]

Subject: Reply to {notice_type} - {notice_number} dated {notice_date}

Ref: GSTIN - {gstin}

Respected Sir/Madam,

We, {taxpayer_name} (GSTIN: {gstin}), hereby submit our reply to the {notice_type} bearing reference number {notice_number} dated {notice_date}.

DETAILED REPLY:

{reply_points}

[AI will expand this section with:
1. Point-by-point response to each allegation
2. Relevant legal provisions and case laws
3. Supporting documentation references
4. Request for personal hearing if applicable]

PRAYER:

In view of the above submissions, we request your good office to:
1. Accept our reply and drop the proceedings
2. Grant us a personal hearing to present our case
3. Allow us to submit additional documents if required

We trust that justice will be done and the matter will be decided in our favor.

Thanking you,

For {taxpayer_name}
GSTIN: {gstin}

Authorized Signatory
Name:
Designation:
Date:
Place:

Enclosures:
1. Supporting Documents
2. Relevant Invoices/Bills
3. Computation Statements
4. Legal Citations""",
            "tags": ["GST", "Notice", "Reply", "Show Cause", "Tax"],
            "ai_enhanced": True
        },
        {
            "id": "gst_cancellation_application",
            "name": "GST Registration Cancellation",
            "category": "gst",
            "description": "Application to cancel GST registration",
            "applicable_for": ["CA", "Tax Professional", "Corporate"],
            "fields": [
                {
                    "name": "business_name",
                    "label": "Business Name",
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
                    "name": "cancellation_reason",
                    "label": "Reason for Cancellation",
                    "type": "dropdown",
                    "required": True,
                    "options": [
                        "Business discontinued",
                        "Transfer of business",
                        "Change in constitution",
                        "Amalgamation/Merger",
                        "Other"
                    ]
                },
                {
                    "name": "effective_date",
                    "label": "Requested Effective Date",
                    "type": "date",
                    "required": True
                }
            ],
            "template_text": """To,
The Jurisdictional GST Officer,
GST Department,
[Office Address]

Subject: Application for Cancellation of GST Registration

GSTIN: {gstin}

Respected Sir/Madam,

We, {business_name} (GSTIN: {gstin}), hereby request cancellation of our GST registration.

DETAILS:
- Business Name: {business_name}
- GSTIN: {gstin}
- Reason for Cancellation: {cancellation_reason}
- Requested Effective Date: {effective_date}

[AI will expand with details about final returns, stock declaration, etc.]

Thanking you,

Authorized Signatory
Name:
Date:""",
            "tags": ["GST", "Cancellation", "Closure"],
            "ai_enhanced": True
        },
        {
            "id": "gst_itc_rectification",
            "name": "ITC Rectification Application",
            "category": "gst",
            "description": "Application to rectify Input Tax Credit errors",
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
                    "name": "tax_period",
                    "label": "Tax Period",
                    "type": "text",
                    "required": True,
                    "placeholder": "April 2024"
                },
                {
                    "name": "error_description",
                    "label": "Description of Error",
                    "type": "multiline",
                    "required": True
                }
            ],
            "template_text": """To,
The Jurisdictional GST Officer,

Subject: Application for Rectification of ITC

GSTIN: {gstin}
Tax Period: {tax_period}

Respected Sir/Madam,

We, {taxpayer_name}, request rectification of ITC for {tax_period}.

ERROR DETAILS:
{error_description}

[AI will expand with corrected values, justification, and supporting documents]

Thanking you,

For {taxpayer_name}
Authorized Signatory""",
            "tags": ["GST", "ITC", "Rectification", "Error Correction"],
            "ai_enhanced": True
        },
        {
            "id": "gst_composition_scheme",
            "name": "GST Composition Scheme Application",
            "category": "gst",
            "description": "Application to opt for composition scheme under GST",
            "applicable_for": ["CA", "Tax Professional", "Small Business"],
            "fields": [
                {"name": "business_name", "label": "Business Name", "type": "text", "required": True},
                {"name": "gstin", "label": "GSTIN", "type": "text", "required": True},
                {"name": "annual_turnover", "label": "Annual Turnover (Rs.)", "type": "number", "required": True},
                {"name": "business_type", "label": "Type of Business", "type": "dropdown", "required": True,
                 "options": ["Manufacturer", "Trader", "Restaurant", "Service Provider"]}
            ],
            "template_text": """Application for Composition Scheme under Section 10 of CGST Act
Business: {business_name}, GSTIN: {gstin}, Turnover: Rs. {annual_turnover}
[AI expands with eligibility and compliance details]""",
            "tags": ["GST", "Composition Scheme"], "ai_enhanced": True
        },
        {
            "id": "gst_eway_bill_cancellation",
            "name": "E-Way Bill Cancellation Request",
            "category": "gst",
            "description": "Request to cancel e-way bill",
            "applicable_for": ["CA", "Tax Professional", "Corporate"],
            "fields": [
                {"name": "business_name", "label": "Business Name", "type": "text", "required": True},
                {"name": "eway_bill_number", "label": "E-Way Bill Number", "type": "text", "required": True},
                {"name": "reason", "label": "Reason for Cancellation", "type": "multiline", "required": True}
            ],
            "template_text": """E-Way Bill Cancellation Request\nE-Way Bill No: {eway_bill_number}\nReason: {reason}\n[AI expands]""",
            "tags": ["GST", "E-Way Bill"], "ai_enhanced": True
        },
        {
            "id": "gst_revocation_cancellation",
            "name": "GST Registration Revocation Application",
            "category": "gst",
            "description": "Application to revoke cancellation of GST registration",
            "applicable_for": ["CA", "Tax Professional"],
            "fields": [
                {"name": "taxpayer_name", "label": "Taxpayer Name", "type": "text", "required": True},
                {"name": "gstin", "label": "GSTIN", "type": "text", "required": True},
                {"name": "cancellation_order_date", "label": "Cancellation Order Date", "type": "date", "required": True},
                {"name": "reasons", "label": "Reasons for Revocation", "type": "multiline", "required": True}
            ],
            "template_text": """Application for Revocation of GST Registration Cancellation\nGSTIN: {gstin}\nCancellation Date: {cancellation_order_date}\nReasons: {reasons}\n[AI expands]""",
            "tags": ["GST", "Revocation"], "ai_enhanced": True
        },
        {
            "id": "gst_payment_challan_dispute",
            "name": "GST Payment Challan Discrepancy Letter",
            "category": "gst",
            "description": "Letter for resolving payment challan discrepancies",
            "applicable_for": ["CA", "Tax Professional"],
            "fields": [
                {"name": "taxpayer_name", "label": "Taxpayer Name", "type": "text", "required": True},
                {"name": "gstin", "label": "GSTIN", "type": "text", "required": True},
                {"name": "challan_number", "label": "Challan Number", "type": "text", "required": True},
                {"name": "issue_description", "label": "Issue Description", "type": "multiline", "required": True}
            ],
            "template_text": """GST Payment Challan Discrepancy\nGSTIN: {gstin}\nChallan: {challan_number}\nIssue: {issue_description}\n[AI expands]""",
            "tags": ["GST", "Payment", "Challan"], "ai_enhanced": True
        },
        {
            "id": "gst_advance_ruling_application",
            "name": "GST Advance Ruling Application",
            "category": "gst",
            "description": "Application for advance ruling on GST matters",
            "applicable_for": ["CA", "Tax Professional", "Corporate"],
            "fields": [
                {"name": "applicant_name", "label": "Applicant Name", "type": "text", "required": True},
                {"name": "gstin", "label": "GSTIN", "type": "text", "required": True},
                {"name": "question", "label": "Question for Ruling", "type": "multiline", "required": True},
                {"name": "background", "label": "Background/Facts", "type": "multiline", "required": True}
            ],
            "template_text": """Application for Advance Ruling\nApplicant: {applicant_name}\nGSTIN: {gstin}\nQuestion: {question}\nBackground: {background}\n[AI expands]""",
            "tags": ["GST", "Advance Ruling"], "ai_enhanced": True
        },
        {
            "id": "gst_nil_return_letter",
            "name": "GST Nil Return Covering Letter",
            "category": "gst",
            "description": "Covering letter for nil GST return filing",
            "applicable_for": ["CA", "Small Business"],
            "fields": [
                {"name": "business_name", "label": "Business Name", "type": "text", "required": True},
                {"name": "gstin", "label": "GSTIN", "type": "text", "required": True},
                {"name": "return_period", "label": "Return Period", "type": "text", "required": True}
            ],
            "template_text": """Nil GST Return Filing\nBusiness: {business_name}\nGSTIN: {gstin}\nPeriod: {return_period}\n[AI expands]""",
            "tags": ["GST", "Nil Return"], "ai_enhanced": True
        },
        {
            "id": "gst_input_service_distributor",
            "name": "ISD Registration Application",
            "category": "gst",
            "description": "Application for Input Service Distributor registration",
            "applicable_for": ["CA", "Corporate"],
            "fields": [
                {"name": "company_name", "label": "Company Name", "type": "text", "required": True},
                {"name": "head_office_address", "label": "Head Office Address", "type": "multiline", "required": True},
                {"name": "branch_details", "label": "Branch Details", "type": "multiline", "required": True}
            ],
            "template_text": """ISD Registration Application\nCompany: {company_name}\nHead Office: {head_office_address}\nBranches: {branch_details}\n[AI expands]""",
            "tags": ["GST", "ISD"], "ai_enhanced": True
        }
    ]
