"""Corporate & ROC Templates"""

def get_corporate_templates():
    """Returns all corporate/ROC related templates"""
    return [
        {
            "id": "director_appointment_resolution",
            "name": "Board Resolution - Director Appointment",
            "category": "corporate",
            "description": "Board resolution for appointment of director",
            "applicable_for": ["CA", "Corporate", "CS"],
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
                    "required": True,
                    "placeholder": "U12345MH2020PTC123456"
                },
                {
                    "name": "director_name",
                    "label": "Director Name",
                    "type": "text",
                    "required": True
                },
                {
                    "name": "din",
                    "label": "DIN",
                    "type": "text",
                    "required": True,
                    "placeholder": "01234567"
                },
                {
                    "name": "appointment_date",
                    "label": "Date of Appointment",
                    "type": "date",
                    "required": True
                },
                {
                    "name": "designation",
                    "label": "Designation",
                    "type": "dropdown",
                    "required": True,
                    "options": [
                        "Managing Director",
                        "Executive Director",
                        "Non-Executive Director",
                        "Independent Director",
                        "Additional Director"
                    ]
                }
            ],
            "template_text": """BOARD RESOLUTION FOR APPOINTMENT OF DIRECTOR

{company_name}
CIN: {cin}

RESOLVED THAT pursuant to the provisions of Section 152, 161, 168 and other applicable provisions of the Companies Act, 2013 and the Articles of Association of the Company, consent of the Board be and is hereby accorded to appoint:

Name: {director_name}
DIN: {din}
Designation: {designation}
Date of Appointment: {appointment_date}

As a Director of the Company with effect from {appointment_date}.

FURTHER RESOLVED THAT the above appointment be placed before the members for their approval in the next General Meeting.

FURTHER RESOLVED THAT necessary Form DIR-12 be filed with the Registrar of Companies within prescribed time limits.

For {company_name}

_________________
Director

Place:
Date:""",
            "tags": ["Corporate", "Director", "Appointment", "Board Resolution", "ROC"],
            "ai_enhanced": False
        },
        {
            "id": "roc_form_mgt7",
            "name": "ROC Annual Return (MGT-7) Filing Letter",
            "category": "corporate",
            "description": "Covering letter for filing annual return Form MGT-7",
            "applicable_for": ["CA", "CS", "Corporate"],
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
                    "required": True,
                    "placeholder": "2023-24"
                },
                {
                    "name": "agm_date",
                    "label": "AGM Date",
                    "type": "date",
                    "required": True
                }
            ],
            "template_text": """To,
The Registrar of Companies,
[State]

Subject: Filing of Annual Return in Form MGT-7 for FY {financial_year}

CIN: {cin}

Respected Sir/Madam,

We, {company_name} (CIN: {cin}), hereby submit the Annual Return in Form MGT-7 for the Financial Year {financial_year}.

DETAILS:
- Company Name: {company_name}
- CIN: {cin}
- Financial Year: {financial_year}
- AGM held on: {agm_date}
- Filing Date: [DATE]

The Annual Return has been duly certified by a practicing Company Secretary and is being filed within the prescribed time limit.

All applicable fees have been paid through the MCA portal.

Kindly register the same and provide acknowledgment.

Thanking you,

For {company_name}

Company Secretary/Authorized Signatory
Name:
Membership No:
Date:
Place:

Enclosures:
1. Form MGT-7 (Certified)
2. Payment receipt
3. Board Resolution""",
            "tags": ["ROC", "Annual Return", "MGT-7", "Compliance", "Filing"],
            "ai_enhanced": True
        },
        {
            "id": "share_transfer_sh4",
            "name": "Share Transfer Form (SH-4)",
            "category": "corporate",
            "description": "Share transfer intimation to ROC in Form SH-4",
            "applicable_for": ["CA", "CS", "Corporate"],
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
                    "name": "transferor_name",
                    "label": "Transferor Name",
                    "type": "text",
                    "required": True
                },
                {
                    "name": "transferee_name",
                    "label": "Transferee Name",
                    "type": "text",
                    "required": True
                },
                {
                    "name": "number_of_shares",
                    "label": "Number of Shares",
                    "type": "number",
                    "required": True
                },
                {
                    "name": "transfer_date",
                    "label": "Date of Transfer",
                    "type": "date",
                    "required": True
                }
            ],
            "template_text": """FORM SH-4
NOTICE TO REGISTRAR OF COMPANIES FOR TRANSFER OF SHARES

{company_name}
CIN: {cin}

We hereby inform that the following share transfer has been registered:

TRANSFEROR DETAILS:
Name: {transferor_name}
Shares transferred: {number_of_shares}

TRANSFEREE DETAILS:
Name: {transferee_name}
Shares received: {number_of_shares}

Date of Transfer: {transfer_date}

[AI will expand with complete Form SH-4 details]

For {company_name}

Director/Company Secretary
Date:""",
            "tags": ["Share Transfer", "SH-4", "ROC", "Corporate"],
            "ai_enhanced": True
        },
        {
            "id": "board_resolution_bank_account",
            "name": "Board Resolution - Bank Account Opening",
            "category": "corporate",
            "description": "Board resolution for opening company bank account",
            "applicable_for": ["CA", "CS", "Corporate"],
            "fields": [
                {
                    "name": "company_name",
                    "label": "Company Name",
                    "type": "text",
                    "required": True
                },
                {
                    "name": "bank_name",
                    "label": "Bank Name",
                    "type": "text",
                    "required": True
                },
                {
                    "name": "branch_name",
                    "label": "Branch Name",
                    "type": "text",
                    "required": True
                },
                {
                    "name": "account_type",
                    "label": "Account Type",
                    "type": "dropdown",
                    "required": True,
                    "options": [
                        "Current Account",
                        "Savings Account",
                        "Overdraft Account"
                    ]
                },
                {
                    "name": "authorized_signatories",
                    "label": "Authorized Signatories",
                    "type": "multiline",
                    "required": True,
                    "placeholder": "List names and designations"
                }
            ],
            "template_text": """BOARD RESOLUTION
FOR OPENING BANK ACCOUNT

{company_name}

RESOLVED THAT a {account_type} be opened with {bank_name}, {branch_name} in the name of the Company.

FURTHER RESOLVED THAT the following persons be and are hereby authorized to operate the said bank account on behalf of the Company:

{authorized_signatories}

FURTHER RESOLVED THAT all cheques, drafts, and other banking instruments shall be signed by any TWO of the above authorized signatories jointly.

FURTHER RESOLVED THAT the authorized signatories be empowered to execute all necessary forms, documents, and agreements with the bank.

For {company_name}

_______________
Director

Date:
Place:""",
            "tags": ["Board Resolution", "Bank Account", "Corporate", "Banking"],
            "ai_enhanced": False
        },
        {
            "id": "agm_notice",
            "name": "Annual General Meeting (AGM) Notice",
            "category": "corporate",
            "description": "Notice for convening Annual General Meeting",
            "applicable_for": ["CA", "CS", "Corporate"],
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
                    "name": "agm_date",
                    "label": "AGM Date",
                    "type": "date",
                    "required": True
                },
                {
                    "name": "agm_time",
                    "label": "AGM Time",
                    "type": "text",
                    "required": True,
                    "placeholder": "11:00 AM"
                },
                {
                    "name": "agm_venue",
                    "label": "AGM Venue/Platform",
                    "type": "multiline",
                    "required": True,
                    "placeholder": "Registered Office or Video Conference details"
                },
                {
                    "name": "financial_year",
                    "label": "Financial Year",
                    "type": "text",
                    "required": True,
                    "placeholder": "2023-24"
                },
                {
                    "name": "agenda_items",
                    "label": "Agenda Items",
                    "type": "multiline",
                    "required": True,
                    "placeholder": "1. Adoption of Financial Statements\n2. Declaration of Dividend\n3. Appointment of Auditor"
                }
            ],
            "template_text": """NOTICE OF ANNUAL GENERAL MEETING

{company_name}
CIN: {cin}

NOTICE is hereby given that the Annual General Meeting of the Members of {company_name} will be held on {agm_date} at {agm_time} at:

{agm_venue}

To transact the following business:

ORDINARY BUSINESS:

{agenda_items}

SPECIAL BUSINESS (if any):
[To be specified]

NOTES:
1. A member entitled to attend and vote is entitled to appoint a proxy.
2. The Register of Members will remain closed from [DATE] to {agm_date}.
3. Financial Year under consideration: {financial_year}

[AI expands with detailed agenda, proxy form, and statutory disclosures]

By Order of the Board
For {company_name}

Company Secretary
Name:
Membership No:
Date:
Place:""",
            "tags": ["AGM", "Annual General Meeting", "Corporate", "Notice", "Shareholders"],
            "ai_enhanced": True
        },
        {
            "id": "egm_notice",
            "name": "Extraordinary General Meeting (EGM) Notice",
            "category": "corporate",
            "description": "Notice for convening Extraordinary General Meeting",
            "applicable_for": ["CA", "CS", "Corporate"],
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
                    "name": "egm_date",
                    "label": "EGM Date",
                    "type": "date",
                    "required": True
                },
                {
                    "name": "egm_time",
                    "label": "EGM Time",
                    "type": "text",
                    "required": True
                },
                {
                    "name": "egm_venue",
                    "label": "EGM Venue/Platform",
                    "type": "multiline",
                    "required": True
                },
                {
                    "name": "special_business",
                    "label": "Special Business/Purpose",
                    "type": "multiline",
                    "required": True,
                    "placeholder": "Change of name, Increase in capital, Related party transactions, etc."
                }
            ],
            "template_text": """NOTICE OF EXTRAORDINARY GENERAL MEETING

{company_name}
CIN: {cin}

NOTICE is hereby given that an Extraordinary General Meeting (EGM) of the Members of {company_name} will be held on {egm_date} at {egm_time} at:

{egm_venue}

To consider and, if thought fit, to pass the following resolution(s):

SPECIAL BUSINESS:

{special_business}

NOTES:
1. Explanatory Statement pursuant to Section 102 of the Companies Act, 2013 is annexed.
2. A member entitled to attend and vote may appoint a proxy.
3. Proxy forms must be deposited at the Registered Office 48 hours before the meeting.

[AI expands with explanatory statement, voting details, and special resolution format]

By Order of the Board
For {company_name}

Company Secretary
Date:
Place:""",
            "tags": ["EGM", "Extraordinary General Meeting", "Corporate", "Special Resolution"],
            "ai_enhanced": True
        },
        {
            "id": "dividend_declaration_resolution",
            "name": "Board Resolution - Dividend Declaration",
            "category": "corporate",
            "description": "Board resolution for declaring dividend",
            "applicable_for": ["CA", "CS", "Corporate"],
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
                    "required": True,
                    "placeholder": "2023-24"
                },
                {
                    "name": "dividend_rate",
                    "label": "Dividend Rate (%)",
                    "type": "number",
                    "required": True,
                    "placeholder": "10"
                },
                {
                    "name": "dividend_amount",
                    "label": "Total Dividend Amount (Rs.)",
                    "type": "number",
                    "required": True
                },
                {
                    "name": "record_date",
                    "label": "Record Date",
                    "type": "date",
                    "required": True
                },
                {
                    "name": "payment_date",
                    "label": "Payment Date",
                    "type": "date",
                    "required": True
                }
            ],
            "template_text": """BOARD RESOLUTION FOR DECLARATION OF DIVIDEND

{company_name}
CIN: {cin}

RESOLVED THAT based on the financial performance of the Company for the Financial Year {financial_year} and subject to approval of members at the Annual General Meeting, a dividend at the rate of {dividend_rate}% per equity share be and is hereby recommended.

DIVIDEND DETAILS:
- Financial Year: {financial_year}
- Dividend Rate: {dividend_rate}%
- Total Dividend Amount: Rs. {dividend_amount}
- Record Date: {record_date}
- Payment Date: {payment_date}

FURTHER RESOLVED THAT the dividend shall be paid to all shareholders whose names appear in the Register of Members on the Record Date.

FURTHER RESOLVED THAT the dividend be subject to deduction of tax at source as per applicable provisions of the Income Tax Act, 1961.

FURTHER RESOLVED THAT the above recommendation be placed before the members for their approval at the ensuing Annual General Meeting.

[AI expands with statutory compliances and TDS provisions]

For {company_name}

Director/Chairperson
Date:
Place:""",
            "tags": ["Dividend", "Board Resolution", "Corporate", "Shareholders", "Distribution"],
            "ai_enhanced": True
        },
        {
            "id": "share_allotment_resolution",
            "name": "Board Resolution - Share Allotment",
            "category": "corporate",
            "description": "Board resolution for allotment of shares",
            "applicable_for": ["CA", "CS", "Corporate"],
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
                    "name": "allottee_details",
                    "label": "Allottee Details",
                    "type": "multiline",
                    "required": True,
                    "placeholder": "Name, PAN, Number of Shares, Amount"
                },
                {
                    "name": "share_type",
                    "label": "Type of Shares",
                    "type": "dropdown",
                    "required": True,
                    "options": [
                        "Equity Shares",
                        "Preference Shares",
                        "CCPS (Compulsorily Convertible Preference Shares)"
                    ]
                },
                {
                    "name": "total_shares",
                    "label": "Total Number of Shares",
                    "type": "number",
                    "required": True
                },
                {
                    "name": "face_value",
                    "label": "Face Value per Share (Rs.)",
                    "type": "number",
                    "required": True
                },
                {
                    "name": "premium_amount",
                    "label": "Premium per Share (Rs.)",
                    "type": "number",
                    "required": False,
                    "placeholder": "0 if no premium"
                }
            ],
            "template_text": """BOARD RESOLUTION FOR ALLOTMENT OF SHARES

{company_name}
CIN: {cin}

RESOLVED THAT pursuant to the provisions of Section 39, 42, 62 and other applicable provisions of the Companies Act, 2013 and the Articles of Association of the Company, consent of the Board be and is hereby accorded to allot the following {share_type}:

ALLOTMENT DETAILS:
{allottee_details}

Total Shares: {total_shares}
Face Value: Rs. {face_value} per share
Premium: Rs. {premium_amount} per share

FURTHER RESOLVED THAT the shares shall be subject to the Memorandum and Articles of Association of the Company and shall rank pari passu with the existing shares.

FURTHER RESOLVED THAT Form PAS-3 be filed with the Registrar of Companies within 30 days of allotment.

FURTHER RESOLVED THAT Share Certificates be issued to the allottees within the prescribed time limit.

[AI expands with consideration received, payment terms, and ROC filing requirements]

For {company_name}

Director
Date:
Place:""",
            "tags": ["Share Allotment", "Board Resolution", "Corporate", "PAS-3", "Capital"],
            "ai_enhanced": True
        },
        {
            "id": "loan_approval_resolution",
            "name": "Board Resolution - Loan Approval",
            "category": "corporate",
            "description": "Board resolution for borrowing/taking loan",
            "applicable_for": ["CA", "CS", "Corporate"],
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
                    "name": "lender_name",
                    "label": "Lender Name (Bank/NBFC)",
                    "type": "text",
                    "required": True
                },
                {
                    "name": "loan_amount",
                    "label": "Loan Amount (Rs.)",
                    "type": "number",
                    "required": True
                },
                {
                    "name": "loan_purpose",
                    "label": "Purpose of Loan",
                    "type": "multiline",
                    "required": True,
                    "placeholder": "Working capital, Business expansion, etc."
                },
                {
                    "name": "security_offered",
                    "label": "Security/Collateral Offered",
                    "type": "multiline",
                    "required": True,
                    "placeholder": "Mortgage of property, Hypothecation of assets, Personal guarantee, etc."
                }
            ],
            "template_text": """BOARD RESOLUTION FOR BORROWING/LOAN

{company_name}
CIN: {cin}

RESOLVED THAT pursuant to the provisions of Section 179, 180 and other applicable provisions of the Companies Act, 2013 and the Articles of Association, consent of the Board be and is hereby accorded to borrow a sum not exceeding Rs. {loan_amount} from {lender_name}.

PURPOSE:
{loan_purpose}

SECURITY:
{security_offered}

FURTHER RESOLVED THAT the Directors be and are hereby authorized to execute all necessary loan agreements, deeds, documents, and instruments on behalf of the Company.

FURTHER RESOLVED THAT the Company may create such charges, mortgages, or hypothecations on the assets of the Company as may be required by the lender.

FURTHER RESOLVED THAT Form CHG-1 (for creation of charge) be filed with the Registrar of Companies within 30 days.

[AI expands with Section 180 compliance, limits, and charge creation details]

For {company_name}

Director/Chairperson
Date:
Place:""",
            "tags": ["Loan", "Borrowing", "Board Resolution", "Corporate", "Section 180"],
            "ai_enhanced": True
        },
        {
            "id": "registered_office_change_inc22",
            "name": "Change of Registered Office (INC-22)",
            "category": "corporate",
            "description": "Application for change of registered office address",
            "applicable_for": ["CA", "CS", "Corporate"],
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
                    "name": "old_address",
                    "label": "Old Registered Office Address",
                    "type": "multiline",
                    "required": True
                },
                {
                    "name": "new_address",
                    "label": "New Registered Office Address",
                    "type": "multiline",
                    "required": True
                },
                {
                    "name": "change_type",
                    "label": "Type of Change",
                    "type": "dropdown",
                    "required": True,
                    "options": [
                        "Within same city/town/village",
                        "From one city to another in same state",
                        "From one state to another state"
                    ]
                },
                {
                    "name": "effective_date",
                    "label": "Effective Date of Change",
                    "type": "date",
                    "required": True
                }
            ],
            "template_text": """FORM INC-22
NOTICE OF SITUATION OR CHANGE OF SITUATION OF REGISTERED OFFICE

{company_name}
CIN: {cin}

Type of Change: {change_type}

OLD ADDRESS:
{old_address}

NEW ADDRESS:
{new_address}

Effective Date: {effective_date}

ATTACHMENTS:
1. Board Resolution
2. Special Resolution (if applicable)
3. NOC from Landlord/Proof of Ownership
4. Utility bill of new address

DECLARATION:
We declare that the new premises are owned/held on lease by the Company and are suitable for carrying on the business of the Company.

[AI expands with INC-22 format, regional director approval (if interstate), and statutory requirements]

For {company_name}

Director
DIN:
Date:
Place:""",
            "tags": ["Registered Office", "INC-22", "Corporate", "ROC", "Address Change"],
            "ai_enhanced": True
        },
        {
            "id": "authorized_capital_increase",
            "name": "Increase in Authorized Capital (SH-7)",
            "category": "corporate",
            "description": "Resolution and form for increasing authorized share capital",
            "applicable_for": ["CA", "CS", "Corporate"],
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
                    "name": "existing_capital",
                    "label": "Existing Authorized Capital (Rs.)",
                    "type": "number",
                    "required": True
                },
                {
                    "name": "increase_amount",
                    "label": "Increase in Capital (Rs.)",
                    "type": "number",
                    "required": True
                },
                {
                    "name": "new_capital",
                    "label": "New Authorized Capital (Rs.)",
                    "type": "number",
                    "required": True
                },
                {
                    "name": "reason",
                    "label": "Reason for Increase",
                    "type": "multiline",
                    "required": True,
                    "placeholder": "Fund raising, Business expansion, etc."
                }
            ],
            "template_text": """SPECIAL RESOLUTION FOR INCREASE IN AUTHORIZED CAPITAL

{company_name}
CIN: {cin}

RESOLVED THAT pursuant to the provisions of Section 61, 64 and other applicable provisions of the Companies Act, 2013, the Authorized Share Capital of the Company be increased from Rs. {existing_capital} to Rs. {new_capital} by creation of additional shares.

CAPITAL STRUCTURE:
Existing Authorized Capital: Rs. {existing_capital}
Increase: Rs. {increase_amount}
New Authorized Capital: Rs. {new_capital}

REASON:
{reason}

FURTHER RESOLVED THAT the Memorandum of Association of the Company be altered by substituting Clause V (Capital Clause) accordingly.

FURTHER RESOLVED THAT Form SH-7 along with altered Memorandum be filed with the Registrar of Companies.

FURTHER RESOLVED THAT stamp duty and ROC fees be paid as applicable.

[AI expands with MOA alteration clause, SH-7 format, and stamp duty calculation]

For {company_name}

Chairperson
Date:
Place:""",
            "tags": ["Authorized Capital", "SH-7", "Corporate", "Capital Increase", "MOA Amendment"],
            "ai_enhanced": True
        },
        {
            "id": "aoc4_financial_statements",
            "name": "AOC-4 Financial Statements Filing",
            "category": "corporate",
            "description": "Filing of Financial Statements and other documents with ROC",
            "applicable_for": ["CA", "CS", "Corporate"],
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
                    "required": True,
                    "placeholder": "2023-24"
                },
                {
                    "name": "agm_date",
                    "label": "AGM Date",
                    "type": "date",
                    "required": True
                },
                {
                    "name": "profit_loss",
                    "label": "Net Profit/Loss (Rs.)",
                    "type": "number",
                    "required": True,
                    "placeholder": "Enter negative for loss"
                },
                {
                    "name": "total_assets",
                    "label": "Total Assets (Rs.)",
                    "type": "number",
                    "required": True
                }
            ],
            "template_text": """FORM AOC-4
FILING OF FINANCIAL STATEMENTS

{company_name}
CIN: {cin}

Financial Year: {financial_year}
Date of AGM: {agm_date}

FINANCIAL HIGHLIGHTS:
Net Profit/(Loss): Rs. {profit_loss}
Total Assets: Rs. {total_assets}

DOCUMENTS ATTACHED:
1. Balance Sheet as at [DATE]
2. Statement of Profit & Loss
3. Cash Flow Statement
4. Directors' Report
5. Auditor's Report
6. Board Resolution for approval
7. AGM Resolution for adoption

CERTIFICATIONS:
- Financial Statements audited by Statutory Auditor
- Approved by Board of Directors
- Adopted by Members in AGM

[AI expands with complete AOC-4 format, XBRL filing requirements, and statutory disclosures]

For {company_name}

Director
DIN:
Date:
Place:

Company Secretary (if applicable)
Name:
Membership No:""",
            "tags": ["AOC-4", "Financial Statements", "ROC Filing", "Corporate", "Annual Filing"],
            "ai_enhanced": True
        }
    ]
