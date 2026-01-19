"""Banking & Finance Templates"""

def get_banking_templates():
    """Returns all banking and finance related templates"""
    return [
        {
            "id": "loan_application_letter",
            "name": "Business Loan Application",
            "category": "banking",
            "description": "Application letter for business loan from bank",
            "applicable_for": ["Corporate", "Small Business", "CA"],
            "fields": [
                {"name": "company_name", "label": "Company Name", "type": "text", "required": True},
                {"name": "loan_amount", "label": "Loan Amount Required (Rs.)", "type": "number", "required": True},
                {"name": "loan_purpose", "label": "Purpose of Loan", "type": "multiline", "required": True},
                {"name": "repayment_period", "label": "Proposed Repayment Period (months)", "type": "number", "required": True},
                {"name": "collateral_details", "label": "Collateral/Security Details", "type": "multiline", "required": False}
            ],
            "template_text": """To,
The Branch Manager,
[Bank Name],
[Branch Address]

Subject: Application for Business Loan

Dear Sir/Madam,

We, {company_name}, request a business loan of Rs. {loan_amount} for the following purpose:

PURPOSE: {loan_purpose}

REPAYMENT: {repayment_period} months

COLLATERAL: {collateral_details}

[AI will expand with financial details, business profile, and loan terms]

Thanking you,
For {company_name}
Authorized Signatory""",
            "tags": ["Banking", "Loan", "Finance"],
            "ai_enhanced": True
        },
        {
            "id": "overdraft_facility_request",
            "name": "Overdraft Facility Request",
            "category": "banking",
            "description": "Request for overdraft facility on current account",
            "applicable_for": ["Corporate", "Business"],
            "fields": [
                {"name": "company_name", "label": "Company Name", "type": "text", "required": True},
                {"name": "account_number", "label": "Account Number", "type": "text", "required": True},
                {"name": "od_limit_requested", "label": "OD Limit Requested (Rs.)", "type": "number", "required": True},
                {"name": "business_justification", "label": "Business Justification", "type": "multiline", "required": True}
            ],
            "template_text": """Overdraft Facility Request\nCompany: {company_name}\nAccount: {account_number}\nLimit: Rs. {od_limit_requested}\nJustification: {business_justification}\n[AI expands]""",
            "tags": ["Banking", "Overdraft", "Credit"],
            "ai_enhanced": True
        },
        {
            "id": "bank_guarantee_request",
            "name": "Bank Guarantee Request",
            "category": "banking",
            "description": "Application for bank guarantee issuance",
            "applicable_for": ["Corporate", "CA"],
            "fields": [
                {"name": "company_name", "label": "Company Name", "type": "text", "required": True},
                {"name": "guarantee_amount", "label": "Guarantee Amount (Rs.)", "type": "number", "required": True},
                {"name": "beneficiary_name", "label": "Beneficiary Name", "type": "text", "required": True},
                {"name": "purpose", "label": "Purpose", "type": "text", "required": True},
                {"name": "validity_period", "label": "Validity Period (months)", "type": "number", "required": True}
            ],
            "template_text": """Bank Guarantee Request\nAmount: Rs. {guarantee_amount}\nBeneficiary: {beneficiary_name}\nPurpose: {purpose}\nValidity: {validity_period} months\n[AI expands]""",
            "tags": ["Banking", "Bank Guarantee"],
            "ai_enhanced": True
        },
        {
            "id": "letter_of_credit_application",
            "name": "Letter of Credit Application",
            "category": "banking",
            "description": "Application for opening Letter of Credit",
            "applicable_for": ["Corporate", "Import-Export"],
            "fields": [
                {"name": "applicant_name", "label": "Applicant Name", "type": "text", "required": True},
                {"name": "lc_amount", "label": "LC Amount", "type": "text", "required": True},
                {"name": "beneficiary_details", "label": "Beneficiary Details", "type": "multiline", "required": True},
                {"name": "goods_description", "label": "Description of Goods", "type": "multiline", "required": True}
            ],
            "template_text": """Letter of Credit Application\nApplicant: {applicant_name}\nAmount: {lc_amount}\nBeneficiary: {beneficiary_details}\nGoods: {goods_description}\n[AI expands]""",
            "tags": ["Banking", "LC", "Trade Finance"],
            "ai_enhanced": True
        },
        {
            "id": "loan_noc_request",
            "name": "Loan NOC Request",
            "category": "banking",
            "description": "Request for No Objection Certificate after loan closure",
            "applicable_for": ["Individual", "Corporate"],
            "fields": [
                {"name": "borrower_name", "label": "Borrower Name", "type": "text", "required": True},
                {"name": "loan_account_number", "label": "Loan Account Number", "type": "text", "required": True},
                {"name": "loan_type", "label": "Type of Loan", "type": "text", "required": True}
            ],
            "template_text": """Loan NOC Request\nBorrower: {borrower_name}\nLoan A/C: {loan_account_number}\nType: {loan_type}\n[AI expands]""",
            "tags": ["Banking", "NOC", "Loan Closure"],
            "ai_enhanced": True
        },
        {
            "id": "account_closure_letter",
            "name": "Bank Account Closure Letter",
            "category": "banking",
            "description": "Letter to close bank account",
            "applicable_for": ["Individual", "Corporate"],
            "fields": [
                {"name": "account_holder_name", "label": "Account Holder Name", "type": "text", "required": True},
                {"name": "account_number", "label": "Account Number", "type": "text", "required": True},
                {"name": "account_type", "label": "Account Type", "type": "dropdown", "required": True,
                 "options": ["Savings", "Current", "Fixed Deposit"]},
                {"name": "reason", "label": "Reason for Closure", "type": "text", "required": False}
            ],
            "template_text": """Account Closure Request\nHolder: {account_holder_name}\nA/C No: {account_number}\nType: {account_type}\nReason: {reason}\n[AI expands]""",
            "tags": ["Banking", "Account Closure"],
            "ai_enhanced": True
        },
        {
            "id": "cheque_stop_payment",
            "name": "Stop Payment Request",
            "category": "banking",
            "description": "Request to stop payment of cheque",
            "applicable_for": ["Individual", "Corporate"],
            "fields": [
                {"name": "account_holder", "label": "Account Holder Name", "type": "text", "required": True},
                {"name": "account_number", "label": "Account Number", "type": "text", "required": True},
                {"name": "cheque_number", "label": "Cheque Number", "type": "text", "required": True},
                {"name": "cheque_amount", "label": "Cheque Amount (Rs.)", "type": "number", "required": True},
                {"name": "reason", "label": "Reason for Stop Payment", "type": "multiline", "required": True}
            ],
            "template_text": """Stop Payment Request\nCheque No: {cheque_number}\nAmount: Rs. {cheque_amount}\nReason: {reason}\n[AI expands]""",
            "tags": ["Banking", "Cheque", "Stop Payment"],
            "ai_enhanced": True
        },
        {
            "id": "balance_confirmation_request",
            "name": "Balance Confirmation Request",
            "category": "banking",
            "description": "Request for bank balance confirmation letter",
            "applicable_for": ["Corporate", "CA"],
            "fields": [
                {"name": "company_name", "label": "Company Name", "type": "text", "required": True},
                {"name": "account_number", "label": "Account Number", "type": "text", "required": True},
                {"name": "as_on_date", "label": "Balance As On Date", "type": "date", "required": True},
                {"name": "purpose", "label": "Purpose", "type": "text", "required": True}
            ],
            "template_text": """Balance Confirmation Request\nCompany: {company_name}\nA/C: {account_number}\nAs on: {as_on_date}\nPurpose: {purpose}\n[AI expands]""",
            "tags": ["Banking", "Balance Confirmation", "Audit"],
            "ai_enhanced": True
        },
        {
            "id": "loan_restructuring_request",
            "name": "Loan Restructuring Request",
            "category": "banking",
            "description": "Application for loan restructuring/rescheduling",
            "applicable_for": ["Corporate", "Individual"],
            "fields": [
                {"name": "borrower_name", "label": "Borrower Name", "type": "text", "required": True},
                {"name": "loan_account", "label": "Loan Account Number", "type": "text", "required": True},
                {"name": "current_emi", "label": "Current EMI (Rs.)", "type": "number", "required": True},
                {"name": "proposed_emi", "label": "Proposed EMI (Rs.)", "type": "number", "required": True},
                {"name": "reasons", "label": "Reasons for Restructuring", "type": "multiline", "required": True}
            ],
            "template_text": """Loan Restructuring Request\nBorrower: {borrower_name}\nLoan A/C: {loan_account}\nCurrent EMI: Rs. {current_emi}\nProposed EMI: Rs. {proposed_emi}\nReasons: {reasons}\n[AI expands]""",
            "tags": ["Banking", "Loan", "Restructuring"],
            "ai_enhanced": True
        },
        {
            "id": "credit_facility_renewal",
            "name": "Credit Facility Renewal Request",
            "category": "banking",
            "description": "Request for renewal of credit facilities",
            "applicable_for": ["Corporate"],
            "fields": [
                {"name": "company_name", "label": "Company Name", "type": "text", "required": True},
                {"name": "facility_type", "label": "Type of Facility", "type": "dropdown", "required": True,
                 "options": ["Working Capital Loan", "Term Loan", "Cash Credit", "Letter of Credit", "Bank Guarantee"]},
                {"name": "current_limit", "label": "Current Limit (Rs.)", "type": "number", "required": True},
                {"name": "renewal_period", "label": "Renewal Period (months)", "type": "number", "required": True}
            ],
            "template_text": """Credit Facility Renewal\nCompany: {company_name}\nFacility: {facility_type}\nLimit: Rs. {current_limit}\nPeriod: {renewal_period} months\n[AI expands]""",
            "tags": ["Banking", "Credit", "Renewal"],
            "ai_enhanced": True
        }
    ]
