"""
Template Service for LegalMitra
Provides pre-built document templates for CA and Corporate professionals
"""

from pathlib import Path
from typing import Dict, List, Optional, Any
import json
from pydantic import BaseModel

# Import template modules
from .categories.gst_templates import get_gst_templates
from .categories.income_tax_templates import get_income_tax_templates
from .categories.corporate_templates import get_corporate_templates
from .categories.contract_templates import get_contract_templates
from .categories.compliance_templates import get_compliance_templates
from .categories.legal_notice_templates import get_legal_notice_templates
from .categories.banking_templates import get_banking_templates
from .categories.real_estate_templates import get_real_estate_templates
from .categories.litigation_templates import get_litigation_templates
from .categories.family_law_templates import get_family_law_templates
from .categories.criminal_law_templates import get_criminal_law_templates


class TemplateField(BaseModel):
    """Field definition for template"""
    name: str
    label: str
    type: str  # text, number, date, dropdown, multiline
    required: bool = True
    options: Optional[List[str]] = None  # for dropdown
    placeholder: Optional[str] = None
    help_text: Optional[str] = None


class Template(BaseModel):
    """Template definition"""
    id: str
    name: str
    category: str
    description: str
    applicable_for: List[str]  # ["CA", "Corporate", "Tax Professional"]
    fields: List[TemplateField]
    template_text: str
    tags: List[str]
    ai_enhanced: bool = True  # Whether to use AI to enhance the template


class TemplateService:
    """Service for managing document templates"""

    def __init__(self):
        self.templates_dir = Path(__file__).parent / "data"
        self.templates_dir.mkdir(exist_ok=True)
        self.catalog_file = self.templates_dir / "catalog.json"
        self._catalog_loaded = False
        self.catalog = {}
        # Lazy load catalog to reduce startup memory

    def _load_catalog(self):
        """Load template catalog (lazy loading)"""
        if self._catalog_loaded:
            return
        
        if self.catalog_file.exists():
            try:
                with open(self.catalog_file, 'r', encoding='utf-8') as f:
                    self.catalog = json.load(f)
            except Exception as e:
                print(f"Warning: Could not load catalog: {e}")
                self.catalog = self._create_default_catalog()
        else:
            self.catalog = self._create_default_catalog()
            self._save_catalog()
        
        self._catalog_loaded = True

    def _save_catalog(self):
        """Save template catalog"""
        with open(self.catalog_file, 'w', encoding='utf-8') as f:
            json.dump(self.catalog, f, indent=2, ensure_ascii=False)

    def _create_default_catalog(self) -> Dict:
        """Create default CA/Corporate template catalog"""
        return {
            "categories": {
                "gst": {
                    "name": "GST Templates",
                    "description": "GST registration, returns, notices, appeals",
                    "icon": "receipt_long"
                },
                "income_tax": {
                    "name": "Income Tax Templates",
                    "description": "Tax audits, TDS, advance tax, appeals",
                    "icon": "account_balance"
                },
                "corporate": {
                    "name": "Corporate Templates",
                    "description": "Board resolutions, ROC filings, agreements",
                    "icon": "business"
                },
                "sebi_regulatory": {
                    "name": "SEBI & Regulatory",
                    "description": "SEBI compliance, disclosures, audits",
                    "icon": "gavel"
                },
                "contracts": {
                    "name": "Business Contracts",
                    "description": "Service agreements, NDAs, employment",
                    "icon": "handshake"
                },
                "compliance": {
                    "name": "Compliance & Certifications",
                    "description": "Certificates, compliance reports",
                    "icon": "verified"
                },
                "legal_notices": {
                    "name": "Legal Notices",
                    "description": "Legal notices, demand letters, cease & desist",
                    "icon": "mail"
                },
                "banking": {
                    "name": "Banking & Finance",
                    "description": "Loan applications, bank guarantees, LC, overdrafts",
                    "icon": "account_balance_wallet"
                },
                "real_estate": {
                    "name": "Real Estate",
                    "description": "Sale deed, rent agreement, property documents",
                    "icon": "home"
                },
                "litigation": {
                    "name": "Litigation & Court Practice",
                    "description": "Plaints, IAs, bail applications, appeals, court filings",
                    "icon": "gavel"
                },
                "family_law": {
                    "name": "Family & Personal Law",
                    "description": "Divorce, maintenance, custody, wills, succession",
                    "icon": "family_restroom"
                },
                "criminal_law": {
                    "name": "Criminal Law",
                    "description": "FIR, complaints, bail, quashing, criminal proceedings",
                    "icon": "policy"
                }
            },
            "templates": self._get_default_templates()
        }

    def _get_default_templates(self) -> List[Dict]:
        """Get comprehensive CA/Corporate template library - Now loaded from modular files"""
        templates = []

        # Load templates from category modules
        templates.extend(get_gst_templates())
        templates.extend(get_income_tax_templates())
        templates.extend(get_corporate_templates())
        templates.extend(get_contract_templates())
        templates.extend(get_compliance_templates())
        templates.extend(get_legal_notice_templates())
        templates.extend(get_banking_templates())
        templates.extend(get_real_estate_templates())
        templates.extend(get_litigation_templates())
        templates.extend(get_family_law_templates())
        templates.extend(get_criminal_law_templates())

        return templates

    def _get_default_templates_old(self) -> List[Dict]:
        """OLD IMPLEMENTATION - Kept for reference, can be deleted later"""
        return [
            # ==================== GST TEMPLATES ====================
            {
                "id": "gst_registration_letter",
                "name": "GST Registration Application Letter",
                "category": "gst",
                "description": "Application letter for GST registration under GST Act 2017",
                "applicable_for": ["CA", "Tax Professional", "Corporate"],
                "fields": [
                    {"name": "applicant_name", "label": "Applicant Name", "type": "text", "required": True, "placeholder": "Company/Individual Name"},
                    {"name": "pan", "label": "PAN Number", "type": "text", "required": True, "placeholder": "AAAPZ1234C"},
                    {"name": "business_type", "label": "Type of Business", "type": "dropdown", "required": True, "options": ["Manufacturing", "Trading", "Services", "Mixed"]},
                    {"name": "state", "label": "State", "type": "text", "required": True, "placeholder": "e.g., Karnataka"},
                    {"name": "turnover", "label": "Expected Annual Turnover", "type": "text", "required": True, "placeholder": "50,00,000"},
                    {"name": "address", "label": "Business Address", "type": "multiline", "required": True, "placeholder": "Complete address"}
                ],
                "template_text": """To,
The Assistant Commissioner,
GST Department,
{state}

Date: [DATE]

Subject: Application for GST Registration

Respected Sir/Madam,

I/We, {applicant_name} (PAN: {pan}), hereby apply for registration under the Goods and Services Tax Act, 2017.

BUSINESS DETAILS:
- Nature of Business: {business_type}
- Expected Annual Turnover: Rs. {turnover}
- State of Registration: {state}
- Business Address: {address}

All required documents including PAN, address proof, and identity proof are enclosed herewith.

Kindly process our application at the earliest and grant GST registration.

Thanking you,

{applicant_name}
PAN: {pan}

Enclosures:
1. PAN Card copy
2. Address Proof
3. Identity Proof
4. Bank Account Details""",
                "tags": ["GST", "Registration", "Tax", "Application"],
                "ai_enhanced": True
            },

            {
                "id": "gst_refund_application",
                "name": "GST Refund Application",
                "category": "gst",
                "description": "Application for GST refund claim",
                "applicable_for": ["CA", "Tax Professional"],
                "fields": [
                    {"name": "taxpayer_name", "label": "Taxpayer Name", "type": "text", "required": True},
                    {"name": "gstin", "label": "GSTIN", "type": "text", "required": True, "placeholder": "29AAAAA0000A1Z5"},
                    {"name": "refund_period", "label": "Refund Period", "type": "text", "required": True, "placeholder": "April 2025 to June 2025"},
                    {"name": "refund_amount", "label": "Refund Amount (Rs.)", "type": "number", "required": True},
                    {"name": "refund_reason", "label": "Reason for Refund", "type": "dropdown", "required": True, "options": ["Export of Goods/Services", "Inverted Duty Structure", "ITC Accumulated", "Tax Paid by Mistake"]},
                    {"name": "supporting_docs", "label": "Supporting Documents", "type": "multiline", "required": True, "placeholder": "List all documents attached"}
                ],
                "template_text": """To,
The Commissioner of GST,
[City/State]

Date: [DATE]

Subject: Application for Refund of GST under Section 54 of CGST Act, 2017

Respected Sir/Madam,

I/We, {taxpayer_name}, registered under GSTIN: {gstin}, hereby submit this application for refund of GST.

REFUND DETAILS:
- Refund Period: {refund_period}
- Refund Amount: Rs. {refund_amount}
- Reason for Refund: {refund_reason}

DETAILS OF REFUND CLAIM:
[AI will expand this section based on refund reason]

SUPPORTING DOCUMENTS:
{supporting_docs}

We request you to kindly process this refund claim and credit the refund amount to our registered bank account at the earliest.

Thanking you,

For {taxpayer_name}
GSTIN: {gstin}
Authorized Signatory

Date:
Place:""",
                "tags": ["GST", "Refund", "Tax", "Claim"],
                "ai_enhanced": True
            },

            # ==================== INCOME TAX TEMPLATES ====================
            {
                "id": "tax_audit_report_3cb_3cd",
                "name": "Tax Audit Report Form 3CB-3CD",
                "category": "income_tax",
                "description": "Tax audit report under Section 44AB of Income Tax Act",
                "applicable_for": ["CA"],
                "fields": [
                    {"name": "assessee_name", "label": "Name of Assessee", "type": "text", "required": True},
                    {"name": "pan", "label": "PAN", "type": "text", "required": True},
                    {"name": "assessment_year", "label": "Assessment Year", "type": "text", "required": True, "placeholder": "2025-26"},
                    {"name": "financial_year", "label": "Financial Year", "type": "text", "required": True, "placeholder": "2024-25"},
                    {"name": "turnover", "label": "Gross Turnover/Receipts (Rs.)", "type": "number", "required": True},
                    {"name": "nature_of_business", "label": "Nature of Business", "type": "text", "required": True},
                    {"name": "auditor_name", "label": "Auditor Name", "type": "text", "required": True},
                    {"name": "auditor_firm", "label": "Auditor Firm Name", "type": "text", "required": True},
                    {"name": "auditor_membership_no", "label": "Membership Number", "type": "text", "required": True},
                    {"name": "auditor_frn", "label": "Firm Registration Number", "type": "text", "required": True}
                ],
                "template_text": """TAX AUDIT REPORT
FORM NO. 3CB & 3CD
[Pursuant to Section 44AB of the Income Tax Act, 1961]

Assessment Year: {assessment_year}
Financial Year: {financial_year}

===== PART A - FORM 3CB =====

We have audited the books of account and documents of:

Name: {assessee_name}
PAN: {pan}
Nature of Business: {nature_of_business}
Gross Turnover/Receipts: Rs. {turnover}

For the previous year relevant to assessment year {assessment_year}.

AUDITOR'S CERTIFICATE:

We report that the accounts of {assessee_name} have been audited by us and in our opinion, they have been maintained in the manner required under Section 44AA of the Income Tax Act, 1961.

===== PART B - FORM 3CD =====
(Particulars to be furnished under Section 44AB)

1. Name and address of assessee: {assessee_name}
2. PAN: {pan}
3. Status: [Individual/HUF/Firm/Company/AOP/BOI/LLP]
4. Previous year: {financial_year}
5. Assessment year: {assessment_year}
6. Nature of business/profession: {nature_of_business}

[Detailed particulars as per Form 3CD clauses 1-44 will be populated by AI based on business nature]

For {auditor_firm}
Chartered Accountants
FRN: {auditor_frn}

{auditor_name}
Partner
Membership No: {auditor_membership_no}
UDIN: [To be generated]

Date:
Place:""",
                "tags": ["Income Tax", "Audit", "Form 3CB", "Form 3CD", "Section 44AB"],
                "ai_enhanced": True
            },

            {
                "id": "advance_tax_computation",
                "name": "Advance Tax Computation Statement",
                "category": "income_tax",
                "description": "Computation of advance tax payable in installments",
                "applicable_for": ["CA", "Tax Professional"],
                "fields": [
                    {"name": "taxpayer_name", "label": "Taxpayer Name", "type": "text", "required": True},
                    {"name": "pan", "label": "PAN", "type": "text", "required": True},
                    {"name": "assessment_year", "label": "Assessment Year", "type": "text", "required": True, "placeholder": "2025-26"},
                    {"name": "estimated_income", "label": "Estimated Total Income (Rs.)", "type": "number", "required": True},
                    {"name": "income_from_business", "label": "Income from Business/Profession (Rs.)", "type": "number", "required": True},
                    {"name": "income_from_salary", "label": "Income from Salary (Rs.)", "type": "number", "required": False},
                    {"name": "capital_gains", "label": "Capital Gains (Rs.)", "type": "number", "required": False},
                    {"name": "deductions_80c_80d", "label": "Deductions u/s 80C, 80D etc. (Rs.)", "type": "number", "required": False}
                ],
                "template_text": """ADVANCE TAX COMPUTATION STATEMENT
Assessment Year: {assessment_year}

Taxpayer: {taxpayer_name}
PAN: {pan}

COMPUTATION OF TOTAL INCOME:
1. Income from Salary: Rs. {income_from_salary}
2. Income from Business/Profession: Rs. {income_from_business}
3. Capital Gains: Rs. {capital_gains}
4. Income from Other Sources: Rs. [To be calculated]

Gross Total Income: Rs. {estimated_income}

Less: Deductions under Chapter VI-A
- Section 80C: Rs. [Amount]
- Section 80D: Rs. [Amount]
- Other deductions: Rs. {deductions_80c_80d}

Total Income: Rs. [Net Taxable Income]

TAX COMPUTATION:
[Tax slab rates to be applied by AI based on taxpayer category]

Add: Surcharge (if applicable): Rs. [Amount]
Add: Health & Education Cess @ 4%: Rs. [Amount]

Total Tax Liability: Rs. [Total Amount]
Less: TDS/TCS: Rs. [Amount]

Net Tax Payable: Rs. [Amount]

ADVANCE TAX INSTALLMENTS (Due Dates):
1. By 15th June: 15% of tax = Rs. [Amount]
2. By 15th September: 45% of tax = Rs. [Amount]
3. By 15th December: 75% of tax = Rs. [Amount]
4. By 15th March: 100% of tax = Rs. [Amount]

Note: Interest u/s 234B and 234C will apply for late/short payment.

Prepared by: [CA Name]
Date:""",
                "tags": ["Income Tax", "Advance Tax", "Computation", "Tax Planning"],
                "ai_enhanced": True
            },

            # ==================== CORPORATE TEMPLATES ====================
            {
                "id": "board_resolution_bank_account",
                "name": "Board Resolution - Opening Bank Account",
                "category": "corporate",
                "description": "Resolution for opening company bank account with authorized signatories",
                "applicable_for": ["CA", "Corporate", "CS"],
                "fields": [
                    {"name": "company_name", "label": "Company Name", "type": "text", "required": True},
                    {"name": "cin", "label": "CIN", "type": "text", "required": True, "placeholder": "U12345KA2020PTC123456"},
                    {"name": "meeting_date", "label": "Board Meeting Date", "type": "date", "required": True},
                    {"name": "bank_name", "label": "Bank Name", "type": "text", "required": True},
                    {"name": "branch_address", "label": "Branch Address", "type": "multiline", "required": True},
                    {"name": "account_type", "label": "Account Type", "type": "dropdown", "required": True, "options": ["Current Account", "Savings Account", "CC/OD Account"]},
                    {"name": "authorized_signatories", "label": "Authorized Signatories", "type": "multiline", "required": True, "placeholder": "1. Name - Designation - DIN\\n2. Name - Designation - DIN"},
                    {"name": "signing_mode", "label": "Mode of Operation", "type": "dropdown", "required": True, "options": ["Singly", "Jointly", "Either or Survivor", "Any Two Jointly"]}
                ],
                "template_text": """BOARD RESOLUTION
FOR OPENING OF BANK ACCOUNT

{company_name}
(CIN: {cin})

Extract of Resolution passed at the Board Meeting held on {meeting_date}

RESOLVED THAT pursuant to the provisions of Section 179 of the Companies Act, 2013, and the Articles of Association of the Company, the Board of Directors hereby resolves to open a {account_type} with:

Bank Name: {bank_name}
Branch Address: {branch_address}

RESOLVED FURTHER THAT the following persons be and are hereby authorized as signatories for operating the said bank account:

{authorized_signatories}

RESOLVED FURTHER THAT the mode of operation of the said bank account shall be: {signing_mode}

RESOLVED FURTHER THAT the authorized signatories are hereby empowered to:
1. Execute all necessary account opening forms and documents
2. Operate the account as per the mode specified above
3. Sign cheques, demand drafts, and payment instructions
4. Give standing instructions and mandates
5. Complete all formalities required by the bank

RESOLVED FURTHER THAT a certified copy of this resolution be submitted to {bank_name} and the same shall be treated as sufficient authority for opening and operating the bank account.

For {company_name}

_____________________          _____________________
Director                       Director
DIN:                          DIN:

Date:
Place:

Note: This is a true extract from the minutes of the Board Meeting""",
                "tags": ["Corporate", "Board Resolution", "Banking", "Authorization"],
                "ai_enhanced": True
            },

            {
                "id": "board_resolution_loan",
                "name": "Board Resolution - Taking Loan",
                "category": "corporate",
                "description": "Resolution for borrowing funds from banks/financial institutions",
                "applicable_for": ["CA", "Corporate", "CFO"],
                "fields": [
                    {"name": "company_name", "label": "Company Name", "type": "text", "required": True},
                    {"name": "cin", "label": "CIN", "type": "text", "required": True},
                    {"name": "meeting_date", "label": "Board Meeting Date", "type": "date", "required": True},
                    {"name": "loan_amount", "label": "Loan Amount (Rs.)", "type": "number", "required": True},
                    {"name": "lender_name", "label": "Lender/Bank Name", "type": "text", "required": True},
                    {"name": "loan_purpose", "label": "Purpose of Loan", "type": "multiline", "required": True},
                    {"name": "security_offered", "label": "Security/Collateral Offered", "type": "multiline", "required": True},
                    {"name": "authorized_person", "label": "Person Authorized to Sign Loan Documents", "type": "text", "required": True, "placeholder": "Name, Designation, DIN"}
                ],
                "template_text": """BOARD RESOLUTION
FOR BORROWING OF FUNDS

{company_name}
(CIN: {cin})

Extract of Resolution passed at the Board Meeting held on {meeting_date}

WHEREAS the Company requires funds for the purpose of {loan_purpose};

AND WHEREAS the Board deems it necessary and expedient to borrow funds from {lender_name};

NOW THEREFORE, IT IS HEREBY RESOLVED THAT:

1. Pursuant to Section 180(1)(c) of the Companies Act, 2013, and subject to such approvals as may be necessary, the consent of the Board be and is hereby accorded to borrow a sum not exceeding Rs. {loan_amount} (Rupees [Amount in Words]) from {lender_name}.

2. The loan shall be utilized for the following purpose:
{loan_purpose}

3. The Company offers the following security/collateral for the said borrowing:
{security_offered}

4. Mr./Ms. {authorized_person} be and is hereby authorized to:
   a) Negotiate and finalize the terms and conditions of the loan
   b) Execute all loan agreements, mortgage deeds, hypothecation deeds, and other documents
   c) Create charge/mortgage on the assets of the Company as security
   d) File necessary forms with ROC for registration of charge
   e) Do all acts, deeds, and things necessary in this regard

5. RESOLVED FURTHER THAT the necessary Form CHG-1 be filed with the Registrar of Companies within the prescribed time limit for registration of charge created.

6. RESOLVED FURTHER THAT a certified copy of this resolution be furnished to {lender_name} and other concerned authorities.

For {company_name}

_____________________          _____________________
Director                       Director
DIN:                          DIN:

Date:
Place:

Certified True Copy""",
                "tags": ["Corporate", "Board Resolution", "Loan", "Borrowing", "Section 180"],
                "ai_enhanced": True
            },

            # ==================== CONTRACTS ====================
            {
                "id": "nda_mutual",
                "name": "Mutual Non-Disclosure Agreement (NDA)",
                "category": "contracts",
                "description": "Bilateral NDA for protecting confidential information",
                "applicable_for": ["Corporate", "CA", "Lawyer"],
                "fields": [
                    {"name": "party1_name", "label": "Party 1 Name", "type": "text", "required": True},
                    {"name": "party1_address", "label": "Party 1 Address", "type": "multiline", "required": True},
                    {"name": "party2_name", "label": "Party 2 Name", "type": "text", "required": True},
                    {"name": "party2_address", "label": "Party 2 Address", "type": "multiline", "required": True},
                    {"name": "purpose", "label": "Purpose of Disclosure", "type": "multiline", "required": True, "placeholder": "e.g., Exploring potential business collaboration"},
                    {"name": "duration_years", "label": "Confidentiality Period (Years)", "type": "number", "required": True, "placeholder": "3"},
                    {"name": "jurisdiction", "label": "Governing Law Jurisdiction", "type": "text", "required": True, "placeholder": "Bangalore"}
                ],
                "template_text": """MUTUAL NON-DISCLOSURE AGREEMENT

This Agreement is entered into on this [DATE] between:

PARTY 1:
{party1_name}
Address: {party1_address}
(hereinafter referred to as "Party 1")

AND

PARTY 2:
{party2_name}
Address: {party2_address}
(hereinafter referred to as "Party 2")

(Party 1 and Party 2 shall collectively be referred to as "Parties" and individually as "Party")

WHEREAS the Parties wish to explore {purpose} and in connection therewith, may disclose to each other certain confidential and proprietary information;

NOW THEREFORE, in consideration of the mutual covenants and agreements contained herein, the Parties agree as follows:

1. DEFINITION OF CONFIDENTIAL INFORMATION
   "Confidential Information" means all information disclosed by either Party to the other Party, whether orally, in writing, or in any other form, including but not limited to:
   - Business plans, strategies, and financial information
   - Technical data, trade secrets, and know-how
   - Customer lists, supplier information, and marketing strategies
   - Any other information marked as "Confidential"

2. OBLIGATIONS OF RECEIVING PARTY
   Each Party agrees to:
   a) Hold all Confidential Information in strict confidence
   b) Not disclose Confidential Information to any third party without prior written consent
   c) Use Confidential Information solely for the purpose stated above
   d) Protect Confidential Information with the same degree of care as its own confidential information
   e) Not reverse engineer, disassemble, or decompile any prototypes or samples provided

3. EXCLUSIONS
   This Agreement does not apply to information that:
   a) Was publicly known prior to disclosure
   b) Becomes publicly known through no breach of this Agreement
   c) Was rightfully possessed prior to disclosure
   d) Is independently developed without use of Confidential Information
   e) Is disclosed pursuant to legal requirement or court order

4. TERM AND TERMINATION
   This Agreement shall remain in effect for {duration_years} years from the date of execution. The obligations of confidentiality shall survive termination of this Agreement.

5. RETURN OF MATERIALS
   Upon termination or upon written request, each Party shall return or destroy all Confidential Information and certify such destruction in writing.

6. NO LICENSE
   Nothing in this Agreement grants any license, expressly or impliedly, to either Party's intellectual property rights.

7. GOVERNING LAW AND JURISDICTION
   This Agreement shall be governed by the laws of India. The courts at {jurisdiction} shall have exclusive jurisdiction.

8. MISCELLANEOUS
   - This Agreement constitutes the entire agreement between the Parties
   - No amendment shall be valid unless in writing and signed by both Parties
   - This Agreement may be executed in counterparts

IN WITNESS WHEREOF, the Parties have executed this Agreement on the date first above written.

For {party1_name}                  For {party2_name}

_____________________              _____________________
Authorized Signatory               Authorized Signatory
Name:                              Name:
Designation:                       Designation:
Date:                              Date:""",
                "tags": ["NDA", "Confidentiality", "Contract", "Agreement"],
                "ai_enhanced": True
            },

            {
                "id": "service_agreement",
                "name": "Professional Services Agreement",
                "category": "contracts",
                "description": "Agreement for providing professional services",
                "applicable_for": ["Corporate", "CA", "Consultant"],
                "fields": [
                    {"name": "client_name", "label": "Client Name", "type": "text", "required": True},
                    {"name": "client_address", "label": "Client Address", "type": "multiline", "required": True},
                    {"name": "service_provider_name", "label": "Service Provider Name", "type": "text", "required": True},
                    {"name": "service_provider_address", "label": "Service Provider Address", "type": "multiline", "required": True},
                    {"name": "services_description", "label": "Description of Services", "type": "multiline", "required": True},
                    {"name": "service_fee", "label": "Service Fee (Rs.)", "type": "number", "required": True},
                    {"name": "payment_terms", "label": "Payment Terms", "type": "text", "required": True, "placeholder": "e.g., 30 days from invoice date"},
                    {"name": "agreement_duration", "label": "Agreement Duration", "type": "text", "required": True, "placeholder": "e.g., 1 year"},
                    {"name": "jurisdiction", "label": "Jurisdiction", "type": "text", "required": True}
                ],
                "template_text": """PROFESSIONAL SERVICES AGREEMENT

This Agreement is made on [DATE] between:

CLIENT:
{client_name}
{client_address}
(hereinafter referred to as "Client")

AND

SERVICE PROVIDER:
{service_provider_name}
{service_provider_address}
(hereinafter referred to as "Service Provider")

1. SCOPE OF SERVICES
   The Service Provider agrees to provide the following services to the Client:
   {services_description}

2. TERM
   This Agreement shall commence on [START DATE] and continue for a period of {agreement_duration}, unless terminated earlier as provided herein.

3. FEES AND PAYMENT
   3.1 The Client agrees to pay the Service Provider a fee of Rs. {service_fee} for the services rendered.
   3.2 Payment terms: {payment_terms}
   3.3 All fees are exclusive of applicable taxes (GST), which shall be borne by the Client.

4. DELIVERABLES AND TIMELINES
   [AI will expand based on services description]

5. INTELLECTUAL PROPERTY
   All intellectual property created during the provision of services shall be [owned by Client/Service Provider/jointly owned as per discussion].

6. CONFIDENTIALITY
   Both parties agree to maintain confidentiality of any proprietary information exchanged during the term of this Agreement.

7. TERMINATION
   Either party may terminate this Agreement by providing [30/60/90] days' written notice to the other party.

8. LIMITATION OF LIABILITY
   The Service Provider's liability under this Agreement shall be limited to the fees paid by the Client.

9. INDEMNIFICATION
   Each party shall indemnify the other against any claims arising from breach of this Agreement.

10. GOVERNING LAW
    This Agreement shall be governed by the laws of India. Courts at {jurisdiction} shall have exclusive jurisdiction.

11. ENTIRE AGREEMENT
    This Agreement constitutes the entire understanding between the parties.

IN WITNESS WHEREOF, the parties have executed this Agreement:

For {client_name}                  For {service_provider_name}

_____________________              _____________________
Authorized Signatory               Authorized Signatory
Name:                              Name:
Date:                              Date:""",
                "tags": ["Services", "Contract", "Agreement", "Professional"],
                "ai_enhanced": True
            },

            # ==================== COMPLIANCE CERTIFICATES ====================
            {
                "id": "compliance_certificate_banks",
                "name": "Compliance Certificate for Banks",
                "category": "compliance",
                "description": "Certificate of compliance with loan covenants for banks",
                "applicable_for": ["CA", "CFO", "Corporate"],
                "fields": [
                    {"name": "company_name", "label": "Company Name", "type": "text", "required": True},
                    {"name": "cin", "label": "CIN", "type": "text", "required": True},
                    {"name": "bank_name", "label": "Bank Name", "type": "text", "required": True},
                    {"name": "loan_account_no", "label": "Loan Account Number", "type": "text", "required": True},
                    {"name": "financial_year", "label": "Financial Year", "type": "text", "required": True, "placeholder": "2024-25"},
                    {"name": "debt_equity_ratio", "label": "Debt-Equity Ratio", "type": "text", "required": True, "placeholder": "e.g., 1.5:1"},
                    {"name": "dscr", "label": "DSCR (Debt Service Coverage Ratio)", "type": "text", "required": True, "placeholder": "e.g., 2.0"},
                    {"name": "current_ratio", "label": "Current Ratio", "type": "text", "required": True, "placeholder": "e.g., 1.8:1"},
                    {"name": "ca_name", "label": "CA Name", "type": "text", "required": True},
                    {"name": "ca_firm", "label": "CA Firm Name", "type": "text", "required": True},
                    {"name": "ca_membership_no", "label": "Membership Number", "type": "text", "required": True},
                    {"name": "ca_frn", "label": "Firm Registration Number", "type": "text", "required": True}
                ],
                "template_text": """CERTIFICATE OF COMPLIANCE WITH LOAN COVENANTS

To,
The Branch Manager
{bank_name}
[Branch Address]

Date: [DATE]

Sub: Certificate of Compliance with Loan Covenants - Loan A/c No. {loan_account_no}

Dear Sir/Madam,

This is to certify that we have examined the books of accounts, records, and documents of {company_name} (CIN: {cin}) for the financial year {financial_year} in relation to the terms and covenants of the loan agreement dated [AGREEMENT DATE] with {bank_name}.

Based on our examination and to the best of our knowledge and information, and according to the explanations given to us, we certify that:

1. FINANCIAL COVENANTS COMPLIANCE:
   - Debt-Equity Ratio: {debt_equity_ratio} (Covenant: [Required Ratio])
   - DSCR (Debt Service Coverage Ratio): {dscr} (Covenant: [Required DSCR])
   - Current Ratio: {current_ratio} (Covenant: [Required Ratio])
   - All financial covenants have been complied with.

2. REPAYMENT COMPLIANCE:
   - There are no defaults in repayment of principal or interest during the period under review.
   - All installments due up to [DATE] have been paid on time.

3. END-USE OF FUNDS:
   - The funds borrowed from {bank_name} have been utilized for the purposes stated in the loan agreement.
   - No diversion of funds has occurred.

4. SECURITY DOCUMENTATION:
   - All required security documentation is in order and charges are duly registered.
   - The collateral security remains unencumbered except for the charge created in favor of {bank_name}.

5. OTHER COVENANTS:
   - The Company has complied with all non-financial covenants including submission of periodic statements, insurance policies, and regulatory compliances.
   - No event of default as defined in the loan agreement has occurred.

This certificate is issued at the request of {company_name} for submission to {bank_name} in compliance with the loan agreement terms.

For {ca_firm}
Chartered Accountants
FRN: {ca_frn}

{ca_name}
Partner
Membership No: {ca_membership_no}
UDIN: [To be generated]

Date:
Place:

Note: This certificate is based on the information and explanations provided by the management of the company.""",
                "tags": ["Compliance", "Banking", "Certificate", "Loan Covenant"],
                "ai_enhanced": True
            },

            {
                "id": "net_worth_certificate",
                "name": "Net Worth Certificate",
                "category": "compliance",
                "description": "Certificate stating the net worth of a company/individual",
                "applicable_for": ["CA"],
                "fields": [
                    {"name": "entity_name", "label": "Entity Name", "type": "text", "required": True},
                    {"name": "entity_type", "label": "Entity Type", "type": "dropdown", "required": True, "options": ["Company", "LLP", "Partnership Firm", "Proprietorship", "Individual"]},
                    {"name": "pan", "label": "PAN/CIN", "type": "text", "required": True},
                    {"name": "as_on_date", "label": "Net Worth as on Date", "type": "date", "required": True},
                    {"name": "total_assets", "label": "Total Assets (Rs.)", "type": "number", "required": True},
                    {"name": "total_liabilities", "label": "Total Liabilities (Rs.)", "type": "number", "required": True},
                    {"name": "net_worth_amount", "label": "Net Worth (Rs.)", "type": "number", "required": True},
                    {"name": "ca_name", "label": "CA Name", "type": "text", "required": True},
                    {"name": "ca_firm", "label": "CA Firm", "type": "text", "required": True},
                    {"name": "ca_membership_no", "label": "Membership Number", "type": "text", "required": True}
                ],
                "template_text": """NET WORTH CERTIFICATE

To Whomsoever It May Concern

Date: [DATE]

This is to certify that we have examined the books of accounts and financial records of:

Name: {entity_name}
PAN/CIN: {pan}
Entity Type: {entity_type}

Based on our examination and the financial statements as on {as_on_date}, we certify that the Net Worth of {entity_name} is as follows:

COMPUTATION OF NET WORTH:

Total Assets:                        Rs. {total_assets}

Less: Total External Liabilities:    Rs. {total_liabilities}
      (Excluding Capital/Reserves)

NET WORTH:                           Rs. {net_worth_amount}

BREAKUP OF ASSETS:
[AI will provide detailed breakup based on entity type]

BREAKUP OF LIABILITIES:
[AI will provide detailed breakup based on entity type]

The above certificate is issued based on the books of accounts, balance sheet, and other financial records made available to us.

For {ca_firm}
Chartered Accountants

{ca_name}
Partner/Proprietor
Membership No: {ca_membership_no}
UDIN: [To be generated]

Date:
Place:

Note: This certificate is issued at the request of {entity_name} and is valid as on {as_on_date}.""",
                "tags": ["Compliance", "Net Worth", "Certificate", "Financial"],
                "ai_enhanced": True
            },

            # ==================== LEGAL NOTICES ====================
            {
                "id": "legal_notice_recovery",
                "name": "Legal Notice - Recovery of Dues",
                "category": "legal_notices",
                "description": "Legal notice for recovery of outstanding payment",
                "applicable_for": ["Lawyer", "CA", "Corporate"],
                "fields": [
                    {"name": "sender_name", "label": "Sender/Client Name", "type": "text", "required": True},
                    {"name": "sender_address", "label": "Sender Address", "type": "multiline", "required": True},
                    {"name": "recipient_name", "label": "Recipient/Defaulter Name", "type": "text", "required": True},
                    {"name": "recipient_address", "label": "Recipient Address", "type": "multiline", "required": True},
                    {"name": "amount_due", "label": "Amount Due (Rs.)", "type": "number", "required": True},
                    {"name": "invoice_details", "label": "Invoice/Transaction Details", "type": "multiline", "required": True, "placeholder": "Invoice nos., dates, services/goods provided"},
                    {"name": "due_date", "label": "Original Due Date", "type": "date", "required": True},
                    {"name": "lawyer_name", "label": "Lawyer Name", "type": "text", "required": True},
                    {"name": "lawyer_address", "label": "Lawyer Address", "type": "multiline", "required": True}
                ],
                "template_text": """LEGAL NOTICE

To,
{recipient_name}
{recipient_address}

Date: [DATE]

LEGAL NOTICE UNDER SECTION 138 OF NEGOTIABLE INSTRUMENTS ACT / CONTRACT ACT

Dear Sir/Madam,

UNDER INSTRUCTIONS FROM AND ON BEHALF OF: {sender_name}

I am writing this legal notice under instructions from my client, {sender_name}, residing at {sender_address}, in the matter of recovery of outstanding dues.

FACTS OF THE CASE:

1. My client and you have entered into a business transaction wherein my client provided goods/services as detailed below:
   {invoice_details}

2. The total outstanding amount due and payable by you to my client is Rs. {amount_due} (Rupees [Amount in Words]).

3. The payment was due on {due_date}, but despite repeated reminders and requests, you have failed and neglected to make the payment.

4. This willful default and deliberate refusal to pay the legitimate dues has caused financial loss and mental agony to my client.

NOTICE:

Under instructions from my client, I hereby call upon you to pay the outstanding amount of Rs. {amount_due} along with interest @ [X]% per annum from {due_date} till the date of actual payment, within 15 (fifteen) days from the receipt of this notice.

FURTHER NOTICE:

Please note that if you fail to make the payment within the stipulated time of 15 days, my client shall be constrained to initiate appropriate legal proceedings against you including filing a civil suit for recovery, criminal complaint under Section 138 of the Negotiable Instruments Act (if applicable), or any other legal remedy available under law.

All such legal proceedings shall be at your risk, cost, and consequences. My client reserves the right to claim interest, damages, legal costs, and any other relief as deemed fit.

This notice is issued without prejudice to any rights, remedies, and contentions available to my client under law, all of which are expressly reserved.

Kindly treat this as most urgent and serious.

Yours faithfully,

{lawyer_name}
Advocate
{lawyer_address}

For and on behalf of: {sender_name}

Note: This notice is sent by Registered Post AD / Speed Post / Email""",
                "tags": ["Legal Notice", "Recovery", "Demand", "Payment"],
                "ai_enhanced": True
            },

            {
                "id": "legal_notice_termination",
                "name": "Legal Notice - Termination of Agreement",
                "category": "legal_notices",
                "description": "Legal notice for termination of contract/agreement",
                "applicable_for": ["Lawyer", "Corporate"],
                "fields": [
                    {"name": "sender_name", "label": "Sender Name", "type": "text", "required": True},
                    {"name": "sender_address", "label": "Sender Address", "type": "multiline", "required": True},
                    {"name": "recipient_name", "label": "Recipient Name", "type": "text", "required": True},
                    {"name": "recipient_address", "label": "Recipient Address", "type": "multiline", "required": True},
                    {"name": "agreement_type", "label": "Type of Agreement", "type": "text", "required": True, "placeholder": "e.g., Service Agreement, Lease Agreement"},
                    {"name": "agreement_date", "label": "Agreement Date", "type": "date", "required": True},
                    {"name": "breach_details", "label": "Details of Breach/Reason for Termination", "type": "multiline", "required": True},
                    {"name": "notice_period", "label": "Notice Period (days)", "type": "number", "required": True, "placeholder": "30"},
                    {"name": "lawyer_name", "label": "Lawyer Name", "type": "text", "required": True},
                    {"name": "lawyer_address", "label": "Lawyer Address", "type": "multiline", "required": True}
                ],
                "template_text": """LEGAL NOTICE

To,
{recipient_name}
{recipient_address}

Date: [DATE]

LEGAL NOTICE FOR TERMINATION OF AGREEMENT

Dear Sir/Madam,

UNDER INSTRUCTIONS FROM AND ON BEHALF OF: {sender_name}

I am writing this legal notice under instructions from my client, {sender_name}, residing at {sender_address}.

RE: TERMINATION OF {agreement_type} DATED {agreement_date}

1. BACKGROUND:
   My client and you had entered into a {agreement_type} dated {agreement_date} ("Agreement").

2. BREACH OF CONTRACT:
   It has come to my client's notice that you have committed material breach of the Agreement as detailed below:

   {breach_details}

3. TERMINATION NOTICE:
   In view of the aforesaid material breach and violation of the terms of the Agreement, my client hereby terminates the Agreement with effect from {notice_period} days from the date of receipt of this notice.

4. DEMANDS:
   My client hereby calls upon you to:
   a) Immediately cease all activities under the terminated Agreement
   b) Return all documents, materials, and property belonging to my client
   c) Settle all outstanding dues, if any
   d) [Any other specific demands]

5. CONSEQUENCES OF NON-COMPLIANCE:
   Please note that if you fail to comply with the above demands within {notice_period} days, my client shall be constrained to initiate appropriate legal proceedings for:
   - Recovery of damages
   - Injunction
   - Specific performance
   - Any other relief deemed appropriate

All costs, charges, and expenses of such legal proceedings shall be borne by you.

6. RESERVATION OF RIGHTS:
   This notice is issued without prejudice to all rights and remedies available to my client under the Agreement and under law, all of which are expressly reserved.

Kindly treat this as most urgent.

Yours faithfully,

{lawyer_name}
Advocate
{lawyer_address}

For and on behalf of: {sender_name}""",
                "tags": ["Legal Notice", "Termination", "Contract", "Breach"],
                "ai_enhanced": True
            },

            # ==================== ADDITIONAL GST TEMPLATES ====================
            {
                "id": "gst_notice_reply",
                "name": "GST Notice Reply Template",
                "category": "gst",
                "description": "Reply to GST department show cause notice or demand notice",
                "applicable_for": ["CA", "Tax Professional", "Corporate"],
                "fields": [
                    {"name": "taxpayer_name", "label": "Taxpayer/Company Name", "type": "text", "required": True, "placeholder": "ABC Private Limited"},
                    {"name": "gstin", "label": "GSTIN", "type": "text", "required": True, "placeholder": "29AAAAA0000A1Z5"},
                    {"name": "notice_number", "label": "Notice Reference Number", "type": "text", "required": True, "placeholder": "GST/SCN/2025/1234"},
                    {"name": "notice_date", "label": "Notice Date", "type": "text", "required": True, "placeholder": "15-Jan-2025"},
                    {"name": "notice_type", "label": "Type of Notice", "type": "dropdown", "required": True, "options": ["Show Cause Notice", "Demand Notice", "Audit Notice", "Scrutiny Notice"]},
                    {"name": "reply_points", "label": "Key Points for Reply", "type": "multiline", "required": True, "placeholder": "List main points you want to address"}
                ],
                "template_text": """To,
The Designated Officer
GST Department
[Office Address]

Date: [DATE]

Subject: Reply to {notice_type} - {notice_number} dated {notice_date}
Ref: GSTIN - {gstin}

Respected Sir/Madam,

We, {taxpayer_name} (GSTIN: {gstin}), hereby submit our reply to the {notice_type} bearing reference number {notice_number} dated {notice_date}.

DETAILED REPLY:
{reply_points}

[AI will expand with point-by-point responses, legal provisions, case laws, and supporting documentation]

PRAYER:
In view of the above submissions, we request your good office to:
1. Accept our reply and drop the proceedings
2. Grant us a personal hearing opportunity
3. Allow submission of additional documents if required

Thanking you,

For {taxpayer_name}
GSTIN: {gstin}
Authorized Signatory

Enclosures:
1. Supporting Documents
2. Relevant Invoices/Bills
3. Legal Citations""",
                "tags": ["GST", "Notice", "Reply", "Show Cause", "Tax"],
                "ai_enhanced": True
            },

            {
                "id": "gst_cancellation_application",
                "name": "GST Registration Cancellation",
                "category": "gst",
                "description": "Application for cancellation of GST registration",
                "applicable_for": ["CA", "Tax Professional", "Corporate"],
                "fields": [
                    {"name": "business_name", "label": "Business Name", "type": "text", "required": True},
                    {"name": "gstin", "label": "GSTIN", "type": "text", "required": True, "placeholder": "29AAAAA0000A1Z5"},
                    {"name": "reason", "label": "Reason for Cancellation", "type": "dropdown", "required": True, "options": ["Business Discontinued", "Composition Scheme Opted", "Merger/Amalgamation", "Change in Constitution"]},
                    {"name": "cancellation_date", "label": "Date from which cancellation sought", "type": "text", "required": True}
                ],
                "template_text": """To,
The Assistant Commissioner
GST Department
[Circle/Ward]

Date: [DATE]

Subject: Application for Cancellation of GST Registration

GSTIN: {gstin}
Business Name: {business_name}

Respected Sir/Madam,

I/We hereby apply for cancellation of GST registration from {cancellation_date} for the following reason:

Reason: {reason}

All pending returns have been filed and all taxes, interest, and penalties (if any) have been paid up to the date of application.

Final return will be filed within the prescribed timeline as per GST rules.

Kindly process this application and cancel the GST registration.

For {business_name}
GSTIN: {gstin}

Authorized Signatory
Date:
Place:

Enclosures:
1. Copy of last GST return filed
2. Tax payment challans
3. Supporting documents""",
                "tags": ["GST", "Cancellation", "Registration", "Tax"],
                "ai_enhanced": True
            },

            {
                "id": "gst_itc_rectification",
                "name": "Input Tax Credit Rectification",
                "category": "gst",
                "description": "Letter for rectification of Input Tax Credit (ITC) in GST returns",
                "applicable_for": ["CA", "Tax Professional"],
                "fields": [
                    {"name": "company_name", "label": "Company Name", "type": "text", "required": True},
                    {"name": "gstin", "label": "GSTIN", "type": "text", "required": True},
                    {"name": "return_period", "label": "Return Period", "type": "text", "required": True, "placeholder": "Apr 2025"},
                    {"name": "incorrect_itc", "label": "Incorrectly Claimed ITC (Rs.)", "type": "number", "required": True},
                    {"name": "correct_itc", "label": "Correct ITC (Rs.)", "type": "number", "required": True}
                ],
                "template_text": """To,
The Jurisdictional GST Officer
[Circle/Ward]

Date: [DATE]

Subject: Application for Rectification of Input Tax Credit in GSTR-3B

GSTIN: {gstin}
Return Period: {return_period}

Respected Sir/Madam,

We, {company_name} (GSTIN: {gstin}), wish to bring to your notice an error in claiming Input Tax Credit in our GSTR-3B return for the period {return_period}.

DETAILS OF ERROR:
ITC Claimed (Incorrect): Rs. {incorrect_itc}
Correct ITC Amount: Rs. {correct_itc}
Difference: Rs. {abs(int(incorrect_itc) - int(correct_itc))}

The error occurred due to [AI will suggest common reasons]. We request permission to rectify this error in the next return.

Supporting invoices and documents are enclosed for verification.

Thanking you,

For {company_name}
GSTIN: {gstin}

Enclosures:
1. Copy of incorrect return
2. Supporting invoices
3. Revised computation""",
                "tags": ["GST", "ITC", "Rectification", "Input Tax Credit"],
                "ai_enhanced": True
            },

            # ==================== ADDITIONAL INCOME TAX TEMPLATES ====================
            {
                "id": "tds_return_filing_letter",
                "name": "TDS Return Filing Letter",
                "category": "income_tax",
                "description": "Covering letter for TDS return filing (Form 24Q, 26Q, 27Q)",
                "applicable_for": ["CA", "Tax Professional", "Corporate"],
                "fields": [
                    {"name": "company_name", "label": "Company/Deductor Name", "type": "text", "required": True},
                    {"name": "tan", "label": "TAN", "type": "text", "required": True, "placeholder": "ABCD12345E"},
                    {"name": "form_type", "label": "TDS Return Form", "type": "dropdown", "required": True, "options": ["Form 24Q (Salary TDS)", "Form 26Q (Non-Salary TDS)", "Form 27Q (TDS on NRI)", "Form 27EQ (TCS Return)"]},
                    {"name": "quarter", "label": "Quarter", "type": "dropdown", "required": True, "options": ["Q1 (Apr-Jun)", "Q2 (Jul-Sep)", "Q3 (Oct-Dec)", "Q4 (Jan-Mar)"]},
                    {"name": "financial_year", "label": "Financial Year", "type": "text", "required": True, "placeholder": "2024-25"},
                    {"name": "total_tax_deducted", "label": "Total Tax Deducted (Rs.)", "type": "number", "required": True}
                ],
                "template_text": """To,
The Assessing Officer
Income Tax Department
[Ward/Circle]

Date: [DATE]

Subject: Filing of {form_type} for {quarter} of FY {financial_year}
TAN: {tan}

Respected Sir/Madam,

We, {company_name} (TAN: {tan}), hereby submit the {form_type} for {quarter} of Financial Year {financial_year}.

DETAILS:
- Form Type: {form_type}
- Quarter: {quarter}
- Financial Year: {financial_year}
- Total Tax Deducted: Rs. {total_tax_deducted}
- Filing Date: [DATE]

The return has been filed electronically. Acknowledgment is enclosed.

All taxes have been deposited within prescribed time and TDS certificates have been issued to all deductees.

Kindly process the return and update TDS credit in Form 26AS.

For {company_name}
TAN: {tan}

Authorized Signatory

Enclosures:
1. Return Acknowledgment
2. Challan Copies
3. Form 27A""",
                "tags": ["TDS", "Income Tax", "Return", "Form 24Q", "Form 26Q"],
                "ai_enhanced": True
            },

            {
                "id": "income_tax_appeal",
                "name": "Income Tax Appeal Format",
                "category": "income_tax",
                "description": "Appeal to CIT(A) against assessment order",
                "applicable_for": ["CA", "Tax Professional"],
                "fields": [
                    {"name": "appellant_name", "label": "Appellant Name", "type": "text", "required": True},
                    {"name": "pan", "label": "PAN", "type": "text", "required": True},
                    {"name": "assessment_year", "label": "Assessment Year", "type": "text", "required": True, "placeholder": "2025-26"},
                    {"name": "order_number", "label": "Assessment Order Number", "type": "text", "required": True},
                    {"name": "order_date", "label": "Order Date", "type": "text", "required": True},
                    {"name": "grounds_of_appeal", "label": "Grounds of Appeal", "type": "multiline", "required": True}
                ],
                "template_text": """BEFORE THE COMMISSIONER OF INCOME TAX (APPEALS)
[City]

APPEAL UNDER SECTION 246A OF THE INCOME TAX ACT, 1961

Appellant: {appellant_name}
PAN: {pan}
Assessment Year: {assessment_year}

Vs.

Respondent: The Income Tax Officer
Ward/Circle: [Ward]

GROUNDS OF APPEAL

The appellant most respectfully submits this appeal against the order dated {order_date} bearing number {order_number} on the following grounds:

{grounds_of_appeal}

[AI will expand with:
1. Detailed grounds with legal provisions
2. Facts of the case
3. Case laws supporting appellant
4. Prayer for relief]

PRAYER

In light of the above submissions, the appellant prays that this Hon'ble Authority may be pleased to:
(a) Set aside the impugned order
(b) Grant relief as claimed
(c) Pass such other orders as deemed fit

For {appellant_name}
PAN: {pan}

Authorized Representative
Date:
Place:""",
                "tags": ["Income Tax", "Appeal", "CIT(A)", "Assessment"],
                "ai_enhanced": True
            },

            {
                "id": "section_154_rectification",
                "name": "Rectification u/s 154 Application",
                "category": "income_tax",
                "description": "Application for rectification of mistake under Section 154",
                "applicable_for": ["CA", "Tax Professional"],
                "fields": [
                    {"name": "taxpayer_name", "label": "Taxpayer Name", "type": "text", "required": True},
                    {"name": "pan", "label": "PAN", "type": "text", "required": True},
                    {"name": "assessment_year", "label": "Assessment Year", "type": "text", "required": True},
                    {"name": "mistake_description", "label": "Description of Mistake", "type": "multiline", "required": True}
                ],
                "template_text": """To,
The Income Tax Officer
Ward/Circle: [Ward]

Date: [DATE]

Subject: Application for Rectification under Section 154 of Income Tax Act, 1961

PAN: {pan}
Assessment Year: {assessment_year}

Respected Sir/Madam,

I/We, {taxpayer_name} (PAN: {pan}), submit this application for rectification of mistake apparent from record under Section 154 of the Income Tax Act, 1961.

MISTAKE IDENTIFIED:
{mistake_description}

[AI will expand with:
- Nature of mistake (arithmetical/factual)
- Supporting evidence
- Correct position
- Financial impact]

This is an apparent mistake on record which requires rectification under Section 154.

Kindly rectify the mistake and issue a revised order.

For {taxpayer_name}
PAN: {pan}

Authorized Signatory

Enclosures:
1. Copy of original order
2. Supporting documents
3. Revised computation""",
                "tags": ["Income Tax", "Rectification", "Section 154", "Mistake"],
                "ai_enhanced": True
            },

            # ==================== ADDITIONAL CORPORATE TEMPLATES ====================
            {
                "id": "director_appointment_resolution",
                "name": "Board Resolution for Director Appointment",
                "category": "corporate",
                "description": "Resolution for appointment of director",
                "applicable_for": ["Corporate", "CA"],
                "fields": [
                    {"name": "company_name", "label": "Company Name", "type": "text", "required": True},
                    {"name": "cin", "label": "CIN", "type": "text", "required": True},
                    {"name": "director_name", "label": "Director Name", "type": "text", "required": True},
                    {"name": "din", "label": "DIN (if available)", "type": "text", "required": False},
                    {"name": "appointment_date", "label": "Appointment Date", "type": "text", "required": True}
                ],
                "template_text": """BOARD RESOLUTION FOR APPOINTMENT OF DIRECTOR

{company_name}
CIN: {cin}

RESOLVED THAT pursuant to the provisions of Section 149, 152 and other applicable provisions of the Companies Act, 2013 and the Rules made thereunder, Mr./Ms. {director_name} (DIN: {din}) be and is hereby appointed as an Additional Director of the Company with effect from {appointment_date}.

RESOLVED FURTHER THAT the Additional Director so appointed shall hold office up to the date of the next Annual General Meeting of the Company.

RESOLVED FURTHER THAT the Board recommends the appointment of Mr./Ms. {director_name} as a Director of the Company to the members for their approval in the ensuing General Meeting.

RESOLVED FURTHER THAT the necessary forms be filed with the Registrar of Companies within the prescribed time limit.

RESOLVED FURTHER THAT [Managing Director/Company Secretary] be and is hereby authorized to do all acts, deeds and things necessary for giving effect to the above resolution.

For {company_name}

_____________________
Director

_____________________
Director

Date:
Place:""",
                "tags": ["Corporate", "Director", "Appointment", "Board Resolution"],
                "ai_enhanced": True
            },

            {
                "id": "roc_form_mgt7",
                "name": "Annual Return MGT-7 Filing Letter",
                "category": "corporate",
                "description": "Covering letter for filing MGT-7 annual return",
                "applicable_for": ["Corporate", "CA"],
                "fields": [
                    {"name": "company_name", "label": "Company Name", "type": "text", "required": True},
                    {"name": "cin", "label": "CIN", "type": "text", "required": True},
                    {"name": "financial_year", "label": "Financial Year", "type": "text", "required": True, "placeholder": "2024-25"}
                ],
                "template_text": """To,
The Registrar of Companies
[State]

Date: [DATE]

Subject: Filing of Annual Return in Form MGT-7

CIN: {cin}
Company Name: {company_name}
Financial Year: {financial_year}

Respected Sir/Madam,

Please find enclosed Form MGT-7 (Annual Return) for the financial year ended March 31, 2025, pursuant to Section 92 of the Companies Act, 2013.

The return has been duly certified by a Practicing Company Secretary as required under law.

All applicable fees have been paid through the MCA portal.

Kindly acknowledge receipt and process the same.

For {company_name}
CIN: {cin}

_____________________
Director

Enclosures:
1. Form MGT-7
2. Certification by PCS
3. Payment Challan""",
                "tags": ["Corporate", "ROC", "MGT-7", "Annual Return", "Filing"],
                "ai_enhanced": True
            },

            {
                "id": "share_transfer_sh4",
                "name": "Share Transfer Form SH-4",
                "category": "corporate",
                "description": "Form for transfer of shares",
                "applicable_for": ["Corporate"],
                "fields": [
                    {"name": "company_name", "label": "Company Name", "type": "text", "required": True},
                    {"name": "transferor_name", "label": "Transferor Name", "type": "text", "required": True},
                    {"name": "transferee_name", "label": "Transferee Name", "type": "text", "required": True},
                    {"name": "num_shares", "label": "Number of Shares", "type": "number", "required": True},
                    {"name": "share_value", "label": "Value per Share (Rs.)", "type": "number", "required": True}
                ],
                "template_text": """FORM SH-4
[Pursuant to Section 56(1) of Companies Act, 2013]

NOTICE OF INTIMATION FOR TRANSFER/TRANSMISSION OF SHARES

Company Name: {company_name}

FROM: {transferor_name} (Transferor)
TO: {transferee_name} (Transferee)

Number of Shares: {num_shares}
Face Value per Share: Rs. {share_value}
Total Consideration: Rs. {num_shares * share_value}

The transferor hereby transfers the above shares to the transferee.

The Board of Directors may approve this transfer subject to verification of documents.

Transferor Signature: _____________________
Date:

Transferee Signature: _____________________
Date:

For use of Company:
Transfer approved vide Board Resolution dated: __________

Company Secretary
Date:""",
                "tags": ["Corporate", "Shares", "Transfer", "SH-4", "ROC"],
                "ai_enhanced": True
            },

            # ==================== ADDITIONAL CONTRACT TEMPLATES ====================
            {
                "id": "employment_agreement",
                "name": "Employment Agreement",
                "category": "contracts",
                "description": "Comprehensive employment contract",
                "applicable_for": ["Corporate", "CA"],
                "fields": [
                    {"name": "company_name", "label": "Company Name", "type": "text", "required": True},
                    {"name": "employee_name", "label": "Employee Name", "type": "text", "required": True},
                    {"name": "designation", "label": "Designation", "type": "text", "required": True},
                    {"name": "salary", "label": "Monthly Salary (Rs.)", "type": "number", "required": True},
                    {"name": "joining_date", "label": "Date of Joining", "type": "text", "required": True},
                    {"name": "notice_period", "label": "Notice Period (days)", "type": "number", "required": True, "placeholder": "30"}
                ],
                "template_text": """EMPLOYMENT AGREEMENT

This Agreement is made on [DATE]

BETWEEN

{company_name}, a company incorporated under the Companies Act (hereinafter called "the Company")

AND

{employee_name} (hereinafter called "the Employee")

WHEREAS the Company desires to employ the Employee and the Employee has agreed to serve the Company on the terms and conditions hereinafter contained.

1. APPOINTMENT
The Employee is appointed as {designation} with effect from {joining_date}.

2. SALARY AND BENEFITS
Monthly Salary: Rs. {salary}
[AI will add: Standard benefits, allowances, incentives]

3. DUTIES AND RESPONSIBILITIES
[AI will detail role-specific duties]

4. WORKING HOURS
[AI will add standard working hours]

5. LEAVE POLICY
[AI will add leave entitlements]

6. TERMINATION
Notice Period: {notice_period} days

7. CONFIDENTIALITY
[AI will add confidentiality clauses]

8. NON-COMPETE
[AI will add non-compete terms]

IN WITNESS WHEREOF the parties have executed this Agreement.

For {company_name}                    {employee_name}

_____________________                  _____________________
Authorized Signatory                   Employee Signature

Date:                                  Date:""",
                "tags": ["Contract", "Employment", "Agreement", "HR"],
                "ai_enhanced": True
            },

            {
                "id": "consultant_agreement",
                "name": "Consultant/Professional Services Agreement",
                "category": "contracts",
                "description": "Agreement for hiring consultants or professional services",
                "applicable_for": ["Corporate", "CA"],
                "fields": [
                    {"name": "client_name", "label": "Client/Company Name", "type": "text", "required": True},
                    {"name": "consultant_name", "label": "Consultant Name", "type": "text", "required": True},
                    {"name": "service_description", "label": "Services Description", "type": "multiline", "required": True},
                    {"name": "fees", "label": "Professional Fees (Rs.)", "type": "number", "required": True},
                    {"name": "duration", "label": "Contract Duration", "type": "text", "required": True, "placeholder": "6 months"}
                ],
                "template_text": """PROFESSIONAL SERVICES AGREEMENT

This Agreement is made on [DATE]

BETWEEN

{client_name} (hereinafter called "the Client")

AND

{consultant_name} (hereinafter called "the Consultant")

1. SERVICES
The Consultant agrees to provide the following services:
{service_description}

2. FEES
Professional Fees: Rs. {fees}
Payment Terms: [AI will add payment schedule]

3. DURATION
Contract Period: {duration}

4. DELIVERABLES
[AI will add specific deliverables]

5. CONFIDENTIALITY
[AI will add confidentiality terms]

6. INTELLECTUAL PROPERTY
[AI will add IP ownership clauses]

7. TERMINATION
[AI will add termination conditions]

8. INDEMNITY
[AI will add indemnity clauses]

IN WITNESS WHEREOF the parties have signed this Agreement.

{client_name}                         {consultant_name}

_____________________                 _____________________
Authorized Signatory                  Consultant

Date:                                 Date:""",
                "tags": ["Contract", "Consultant", "Professional Services", "Agreement"],
                "ai_enhanced": True
            },

            {
                "id": "vendor_agreement",
                "name": "Vendor/Supplier Agreement",
                "category": "contracts",
                "description": "Agreement with vendors for supply of goods/services",
                "applicable_for": ["Corporate"],
                "fields": [
                    {"name": "buyer_name", "label": "Buyer/Company Name", "type": "text", "required": True},
                    {"name": "vendor_name", "label": "Vendor Name", "type": "text", "required": True},
                    {"name": "goods_services", "label": "Goods/Services to be supplied", "type": "multiline", "required": True},
                    {"name": "payment_terms", "label": "Payment Terms", "type": "dropdown", "required": True, "options": ["30 Days", "45 Days", "60 Days", "Against Delivery", "Advance Payment"]}
                ],
                "template_text": """VENDOR AGREEMENT

This Agreement is made on [DATE]

BETWEEN

{buyer_name} (hereinafter called "the Buyer")

AND

{vendor_name} (hereinafter called "the Vendor")

1. SUPPLY OF GOODS/SERVICES
The Vendor agrees to supply:
{goods_services}

2. PAYMENT TERMS
Payment: {payment_terms}

3. QUALITY STANDARDS
[AI will add quality specifications]

4. DELIVERY TERMS
[AI will add delivery schedule and terms]

5. WARRANTIES
[AI will add warranty clauses]

6. RETURNS AND REPLACEMENTS
[AI will add return policy]

7. TERMINATION
[AI will add termination clauses]

8. DISPUTE RESOLUTION
[AI will add arbitration clause]

IN WITNESS WHEREOF:

For {buyer_name}                      For {vendor_name}

_____________________                 _____________________
Authorized Signatory                  Authorized Signatory

Date:                                 Date:""",
                "tags": ["Contract", "Vendor", "Supplier", "Purchase"],
                "ai_enhanced": True
            },

            {
                "id": "partnership_deed",
                "name": "Partnership Deed",
                "category": "contracts",
                "description": "Partnership agreement for business partnership",
                "applicable_for": ["CA", "Corporate"],
                "fields": [
                    {"name": "firm_name", "label": "Firm Name", "type": "text", "required": True},
                    {"name": "partner1_name", "label": "Partner 1 Name", "type": "text", "required": True},
                    {"name": "partner2_name", "label": "Partner 2 Name", "type": "text", "required": True},
                    {"name": "capital_partner1", "label": "Capital by Partner 1 (Rs.)", "type": "number", "required": True},
                    {"name": "capital_partner2", "label": "Capital by Partner 2 (Rs.)", "type": "number", "required": True},
                    {"name": "profit_ratio", "label": "Profit Sharing Ratio", "type": "text", "required": True, "placeholder": "50:50"}
                ],
                "template_text": """PARTNERSHIP DEED

This Partnership Deed is made on [DATE]

BETWEEN

{partner1_name} (hereinafter called "First Partner")

AND

{partner2_name} (hereinafter called "Second Partner")

Collectively referred to as "Partners"

1. FIRM NAME
The partnership firm shall be known as: {firm_name}

2. NATURE OF BUSINESS
[AI will add business description]

3. CAPITAL
Partner 1 Capital: Rs. {capital_partner1}
Partner 2 Capital: Rs. {capital_partner2}
Total Capital: Rs. {capital_partner1 + capital_partner2}

4. PROFIT SHARING
Profit/Loss Ratio: {profit_ratio}

5. DUTIES AND RESPONSIBILITIES
[AI will define roles of each partner]

6. BANKING AND ACCOUNTS
[AI will add banking arrangements]

7. DRAWINGS
[AI will add drawing limits]

8. ADMISSION OF NEW PARTNER
[AI will add admission terms]

9. RETIREMENT/DEATH
[AI will add exit clauses]

10. DISSOLUTION
[AI will add dissolution terms]

IN WITNESS WHEREOF the partners have signed:

{partner1_name}                       {partner2_name}

_____________________                 _____________________
Partner 1                             Partner 2

Date:                                 Date:

WITNESSES:
1. _____________________
2. _____________________""",
                "tags": ["Partnership", "Deed", "Agreement", "Business"],
                "ai_enhanced": True
            },

            # ==================== ADDITIONAL COMPLIANCE TEMPLATES ====================
            {
                "id": "pf_compliance_report",
                "name": "Provident Fund Compliance Report",
                "category": "compliance",
                "description": "Monthly PF compliance report",
                "applicable_for": ["Corporate", "CA"],
                "fields": [
                    {"name": "company_name", "label": "Company Name", "type": "text", "required": True},
                    {"name": "pf_number", "label": "PF Account Number", "type": "text", "required": True},
                    {"name": "month_year", "label": "Month & Year", "type": "text", "required": True, "placeholder": "January 2025"},
                    {"name": "total_employees", "label": "Total Employees Covered", "type": "number", "required": True},
                    {"name": "total_contribution", "label": "Total PF Contribution (Rs.)", "type": "number", "required": True}
                ],
                "template_text": """PROVIDENT FUND COMPLIANCE REPORT

Company: {company_name}
PF Account Number: {pf_number}
Period: {month_year}

1. EMPLOYEE COVERAGE
Total Employees: {total_employees}
PF Members: [To be filled]

2. CONTRIBUTION DETAILS
Employee Contribution (12%): Rs. [Amount]
Employer Contribution (12%): Rs. [Amount]
Total PF Contribution: Rs. {total_contribution}

3. PAYMENT STATUS
Due Date: [15th of next month]
Payment Date: [Actual date]
Challan Number: [Number]
Status: [Paid/Pending]

4. RETURN FILING
ECR Filed: [Yes/No]
Filing Date: [Date]

5. COMPLIANCE STATUS
✓ Contributions deposited on time
✓ ECR filed within due date
✓ Form 12A generated
✓ UAN activated for all members

Prepared by: _____________________
Date:

For {company_name}

_____________________
Authorized Signatory""",
                "tags": ["Compliance", "PF", "EPFO", "Labor"],
                "ai_enhanced": True
            },

            {
                "id": "esi_compliance_report",
                "name": "ESI Compliance Report",
                "category": "compliance",
                "description": "Monthly ESI compliance report",
                "applicable_for": ["Corporate", "CA"],
                "fields": [
                    {"name": "company_name", "label": "Company Name", "type": "text", "required": True},
                    {"name": "esi_number", "label": "ESI Code Number", "type": "text", "required": True},
                    {"name": "month_year", "label": "Month & Year", "type": "text", "required": True},
                    {"name": "total_contribution", "label": "Total ESI Contribution (Rs.)", "type": "number", "required": True}
                ],
                "template_text": """ESI COMPLIANCE REPORT

Company: {company_name}
ESI Code: {esi_number}
Period: {month_year}

1. COVERAGE
Total Covered Employees: [Number]

2. CONTRIBUTION
Employee Share (0.75%): Rs. [Amount]
Employer Share (3.25%): Rs. [Amount]
Total ESI: Rs. {total_contribution}

3. PAYMENT STATUS
Due Date: [21st of month]
Payment Date: [Date]
Challan Number: [Number]

4. RETURN FILING
Monthly Return Filed: [Yes/No]

5. COMPLIANCE CHECKLIST
✓ Contributions paid
✓ Return filed
✓ Registers maintained

Prepared by: _____________________

For {company_name}
_____________________
Authorized Signatory""",
                "tags": ["Compliance", "ESI", "Labor", "Social Security"],
                "ai_enhanced": True
            },

            # ==================== ADDITIONAL LEGAL NOTICE TEMPLATES ====================
            {
                "id": "cease_desist_letter",
                "name": "Cease and Desist Letter",
                "category": "legal_notices",
                "description": "Legal notice to stop infringement or unauthorized activity",
                "applicable_for": ["CA", "Corporate"],
                "fields": [
                    {"name": "sender_name", "label": "Your Name/Company", "type": "text", "required": True},
                    {"name": "recipient_name", "label": "Recipient Name", "type": "text", "required": True},
                    {"name": "infringement_details", "label": "Details of Infringement/Issue", "type": "multiline", "required": True},
                    {"name": "action_required", "label": "Action Required from Recipient", "type": "multiline", "required": True}
                ],
                "template_text": """CEASE AND DESIST NOTICE

Date: [DATE]

To,
{recipient_name}
[Address]

Dear Sir/Madam,

RE: CEASE AND DESIST NOTICE

This notice is issued on behalf of {sender_name} with respect to the following matter:

INFRINGEMENT/VIOLATION:
{infringement_details}

It has come to our attention that you are engaging in activities that constitute [infringement/violation/breach] of our [rights/agreement/trademark/copyright].

DEMAND:
You are hereby directed to immediately:
{action_required}

TIMELINE:
You are required to comply within 7 days from receipt of this notice.

CONSEQUENCES OF NON-COMPLIANCE:
Failure to comply will result in legal proceedings without further notice, and you shall be liable for:
1. Damages and compensation
2. Legal costs
3. Injunctive relief

This notice is issued without prejudice to our rights and remedies.

For {sender_name}

_____________________
Authorized Signatory

[Advocate details if sent through lawyer]""",
                "tags": ["Legal Notice", "Cease and Desist", "Infringement"],
                "ai_enhanced": True
            },

            {
                "id": "consumer_complaint_notice",
                "name": "Consumer Complaint Notice",
                "category": "legal_notices",
                "description": "Notice for consumer grievance/complaint",
                "applicable_for": ["Corporate"],
                "fields": [
                    {"name": "consumer_name", "label": "Consumer Name", "type": "text", "required": True},
                    {"name": "seller_name", "label": "Seller/Service Provider Name", "type": "text", "required": True},
                    {"name": "product_service", "label": "Product/Service Details", "type": "text", "required": True},
                    {"name": "complaint_details", "label": "Nature of Complaint", "type": "multiline", "required": True},
                    {"name": "amount_paid", "label": "Amount Paid (Rs.)", "type": "number", "required": True}
                ],
                "template_text": """CONSUMER COMPLAINT NOTICE

Date: [DATE]

To,
{seller_name}
[Address]

Dear Sir/Madam,

RE: CONSUMER COMPLAINT - DEFICIENCY IN SERVICE

This is to bring to your notice the following grievance:

CONSUMER DETAILS:
Name: {consumer_name}
Address: [Address]

TRANSACTION DETAILS:
Product/Service: {product_service}
Amount Paid: Rs. {amount_paid}
Date of Purchase: [Date]

COMPLAINT:
{complaint_details}

RELIEF SOUGHT:
1. Replacement of defective product / Re-performance of service
2. Refund of amount paid: Rs. {amount_paid}
3. Compensation for mental agony and harassment
4. Interest on amount from date of payment

You are required to redress this complaint within 15 days failing which a complaint will be filed before the Consumer Disputes Redressal Forum under the Consumer Protection Act, 2019.

This notice is issued under the Consumer Protection Act, 2019.

{consumer_name}

Signature: _____________________
Date:""",
                "tags": ["Legal Notice", "Consumer", "Complaint", "Consumer Protection Act"],
                "ai_enhanced": True
            },

            # ==================== ADDITIONAL GST TEMPLATES ====================
            {
                "id": "gstr1_return_summary",
                "name": "GSTR-1 Return Filing Summary Letter",
                "category": "gst",
                "description": "Covering letter for GSTR-1 (Outward Supplies) return filing",
                "applicable_for": ["CA", "Tax Professional", "Corporate"],
                "fields": [
                    {"name": "taxpayer_name", "label": "Taxpayer Name", "type": "text", "required": True},
                    {"name": "gstin", "label": "GSTIN", "type": "text", "required": True},
                    {"name": "return_period", "label": "Return Period", "type": "text", "required": True, "placeholder": "April 2025"},
                    {"name": "total_taxable_value", "label": "Total Taxable Value (Rs.)", "type": "number", "required": True},
                    {"name": "cgst_amount", "label": "CGST Amount (Rs.)", "type": "number", "required": True},
                    {"name": "sgst_amount", "label": "SGST Amount (Rs.)", "type": "number", "required": True},
                    {"name": "igst_amount", "label": "IGST Amount (Rs.)", "type": "number", "required": False},
                    {"name": "cess_amount", "label": "CESS Amount (Rs.)", "type": "number", "required": False}
                ],
                "template_text": """To,
The Jurisdictional GST Officer
[Circle/Ward]

Date: [DATE]

Subject: Filing of GSTR-1 for Return Period - {return_period}

GSTIN: {gstin}
Name: {taxpayer_name}

Respected Sir/Madam,

We hereby submit the GSTR-1 return for the period {return_period} through the GST portal.

RETURN SUMMARY:
- Return Period: {return_period}
- Total Taxable Value: Rs. {total_taxable_value}
- CGST: Rs. {cgst_amount}
- SGST: Rs. {sgst_amount}
- IGST: Rs. {igst_amount}
- CESS: Rs. {cess_amount}
- Total Tax Liability: Rs. {cgst_amount + sgst_amount + (igst_amount or 0) + (cess_amount or 0)}

The return has been filed electronically. Acknowledgment number and copy are enclosed.

All applicable taxes have been paid within the prescribed time limit.

Thanking you,

For {taxpayer_name}
GSTIN: {gstin}
Authorized Signatory

Enclosures:
1. GSTR-1 Return Acknowledgment
2. Payment Challans""",
                "tags": ["GST", "GSTR-1", "Return", "Outward Supplies"],
                "ai_enhanced": True
            },

            {
                "id": "gstr3b_return_summary",
                "name": "GSTR-3B Return Filing Letter",
                "category": "gst",
                "description": "Covering letter for GSTR-3B monthly return filing",
                "applicable_for": ["CA", "Tax Professional", "Corporate"],
                "fields": [
                    {"name": "taxpayer_name", "label": "Taxpayer Name", "type": "text", "required": True},
                    {"name": "gstin", "label": "GSTIN", "type": "text", "required": True},
                    {"name": "return_period", "label": "Return Period", "type": "text", "required": True, "placeholder": "April 2025"},
                    {"name": "outward_supply_value", "label": "Outward Taxable Supply Value (Rs.)", "type": "number", "required": True},
                    {"name": "itc_claimed", "label": "ITC Claimed (Rs.)", "type": "number", "required": True},
                    {"name": "net_tax_payable", "label": "Net Tax Payable (Rs.)", "type": "number", "required": True}
                ],
                "template_text": """To,
The Jurisdictional GST Officer
[Circle/Ward]

Date: [DATE]

Subject: Filing of GSTR-3B for Return Period - {return_period}

GSTIN: {gstin}
Name: {taxpayer_name}

Respected Sir/Madam,

We hereby submit the GSTR-3B return for the period {return_period} through the GST portal.

RETURN DETAILS:
- Return Period: {return_period}
- Outward Taxable Supply Value: Rs. {outward_supply_value}
- Input Tax Credit Claimed: Rs. {itc_claimed}
- Net Tax Payable: Rs. {net_tax_payable}

The return has been filed and taxes have been paid through:
- Cash Ledger: Rs. [Amount]
- ITC Utilized: Rs. [Amount]

Acknowledgment number: [ARN]

Thanking you,

For {taxpayer_name}
GSTIN: {gstin}

Enclosures:
1. GSTR-3B Acknowledgment
2. Payment Challans""",
                "tags": ["GST", "GSTR-3B", "Monthly Return", "Tax"],
                "ai_enhanced": True
            },

            {
                "id": "gst_composition_scheme_application",
                "name": "GST Composition Scheme Application",
                "category": "gst",
                "description": "Application to opt for Composition Scheme under Section 10 of CGST Act",
                "applicable_for": ["CA", "Tax Professional", "Corporate"],
                "fields": [
                    {"name": "taxpayer_name", "label": "Taxpayer Name", "type": "text", "required": True},
                    {"name": "gstin", "label": "GSTIN", "type": "text", "required": True},
                    {"name": "turnover_fy", "label": "Expected Turnover for FY (Rs.)", "type": "number", "required": True},
                    {"name": "effective_from", "label": "Scheme to be effective from", "type": "text", "required": True, "placeholder": "01-Apr-2025"}
                ],
                "template_text": """To,
The Assistant Commissioner
GST Department
[State]

Date: [DATE]

Subject: Application for Composition Scheme under Section 10 of CGST Act, 2017

GSTIN: {gstin}
Name: {taxpayer_name}

Respected Sir/Madam,

I/We, {taxpayer_name} (GSTIN: {gstin}), hereby apply to opt for Composition Scheme under Section 10 of the CGST Act, 2017.

DETAILS:
- Expected Annual Turnover: Rs. {turnover_fy} (within Rs. 1.5 Crore limit)
- Scheme effective from: {effective_from}
- Business nature: [Manufacturing/Trading/Restaurant Services]

We understand that:
1. We will pay tax at specified rates under the scheme
2. We cannot claim Input Tax Credit
3. We cannot make inter-state supplies
4. We will not collect tax from customers

Kindly process our application and grant Composition Scheme registration.

Thanking you,

For {taxpayer_name}
GSTIN: {gstin}

Enclosures:
1. Form GST CMP-02
2. Supporting documents""",
                "tags": ["GST", "Composition Scheme", "Section 10", "Registration"],
                "ai_enhanced": True
            },

            {
                "id": "gst_amendment_application",
                "name": "GST Registration Amendment Application",
                "category": "gst",
                "description": "Application for amendment in GST registration details (Form GST REG-14)",
                "applicable_for": ["CA", "Tax Professional", "Corporate"],
                "fields": [
                    {"name": "taxpayer_name", "label": "Taxpayer Name", "type": "text", "required": True},
                    {"name": "gstin", "label": "GSTIN", "type": "text", "required": True},
                    {"name": "amendment_type", "label": "Type of Amendment", "type": "dropdown", "required": True, "options": ["Change of Address", "Change of Business Name", "Additional Place of Business", "Change in Partners/Directors", "Change in Contact Details"]},
                    {"name": "amendment_details", "label": "Amendment Details", "type": "multiline", "required": True}
                ],
                "template_text": """To,
The Assistant Commissioner
GST Department
[Circle/Ward]

Date: [DATE]

Subject: Application for Amendment in GST Registration - Form GST REG-14

GSTIN: {gstin}
Name: {taxpayer_name}

Respected Sir/Madam,

We hereby apply for amendment in our GST registration details.

AMENDMENT REQUEST:
Type of Amendment: {amendment_type}

Details:
{amendment_details}

[AI will expand based on amendment type with specific changes, old and new values]

Supporting documents for the amendment are enclosed.

Kindly process this application and approve the amendment.

Thanking you,

For {taxpayer_name}
GSTIN: {gstin}

Enclosures:
1. Form GST REG-14
2. Supporting documents as per amendment type""",
                "tags": ["GST", "Amendment", "Registration", "Form REG-14"],
                "ai_enhanced": True
            },

            {
                "id": "gst_appeal_appellate_authority",
                "name": "GST Appeal to Appellate Authority",
                "category": "gst",
                "description": "Appeal against GST assessment order to Appellate Authority under Section 107",
                "applicable_for": ["CA", "Tax Professional", "Lawyer"],
                "fields": [
                    {"name": "appellant_name", "label": "Appellant Name", "type": "text", "required": True},
                    {"name": "gstin", "label": "GSTIN", "type": "text", "required": True},
                    {"name": "order_number", "label": "Order Number", "type": "text", "required": True},
                    {"name": "order_date", "label": "Order Date", "type": "text", "required": True},
                    {"name": "demand_amount", "label": "Demand Amount in Order (Rs.)", "type": "number", "required": True},
                    {"name": "grounds_of_appeal", "label": "Grounds of Appeal", "type": "multiline", "required": True}
                ],
                "template_text": """BEFORE THE APPELLATE AUTHORITY
[State] GST Department

APPEAL UNDER SECTION 107 OF CGST/SGST ACT, 2017

Appellant: {appellant_name}
GSTIN: {gstin}

Vs.

Respondent: The Jurisdictional GST Officer
[Ward/Circle]

ORDER APPEALED AGAINST:
- Order Number: {order_number}
- Order Date: {order_date}
- Demand Amount: Rs. {demand_amount}

GROUNDS OF APPEAL:

{grounds_of_appeal}

[AI will expand with:
1. Detailed grounds with legal provisions
2. Facts and chronology
3. Legal submissions with case laws
4. Calculation errors (if any)
5. Prayer for relief]

PRAYER:

In view of the above, it is prayed that this Hon'ble Authority may be pleased to:
(a) Set aside/quash the impugned order
(b) Grant refund/relief as claimed
(c) Pass such other orders as deemed fit

For {appellant_name}
GSTIN: {gstin}

Authorized Representative/Advocate
Date:
Place:

Enclosures:
1. Copy of impugned order
2. Supporting documents
3. Grounds of appeal""",
                "tags": ["GST", "Appeal", "Section 107", "Appellate Authority"],
                "ai_enhanced": True
            },

            # ==================== COMPANIES ACT TEMPLATES ====================
            {
                "id": "form_dir3_kyc",
                "name": "DIR-3 KYC Form Filing Letter",
                "category": "corporate",
                "description": "Covering letter for DIR-3 KYC annual filing by directors",
                "applicable_for": ["Corporate", "CA", "CS"],
                "fields": [
                    {"name": "director_name", "label": "Director Name", "type": "text", "required": True},
                    {"name": "din", "label": "DIN", "type": "text", "required": True},
                    {"name": "financial_year", "label": "Financial Year", "type": "text", "required": True, "placeholder": "2024-25"}
                ],
                "template_text": """To,
The Registrar of Companies
[State]

Date: [DATE]

Subject: Filing of DIR-3 KYC Form for Financial Year {financial_year}

DIN: {din}
Director Name: {director_name}

Respected Sir/Madam,

I hereby submit Form DIR-3 KYC for the financial year {financial_year} in compliance with Rule 12A of the Companies (Appointment and Qualification of Directors) Rules, 2014.

DETAILS:
- DIN: {din}
- Director Name: {director_name}
- Financial Year: {financial_year}
- Filing Date: [DATE]

The form has been filed electronically through the MCA portal. KYC details have been verified and updated.

Thanking you,

{director_name}
DIN: {din}

Enclosures:
1. Form DIR-3 KYC acknowledgment
2. Supporting documents""",
                "tags": ["Companies Act", "DIR-3", "KYC", "Director", "Compliance"],
                "ai_enhanced": True
            },

            {
                "id": "form_mbp1_disclosure",
                "name": "MBP-1 Director Interest Disclosure",
                "category": "corporate",
                "description": "Form MBP-1 for disclosure of director's interest in companies/firms",
                "applicable_for": ["Corporate", "CS"],
                "fields": [
                    {"name": "company_name", "label": "Company Name", "type": "text", "required": True},
                    {"name": "cin", "label": "CIN", "type": "text", "required": True},
                    {"name": "director_name", "label": "Director Name", "type": "text", "required": True},
                    {"name": "din", "label": "DIN", "type": "text", "required": True},
                    {"name": "interest_details", "label": "Interest Details", "type": "multiline", "required": True, "placeholder": "List companies/firms where director has interest"}
                ],
                "template_text": """FORM MBP-1
[Pursuant to Section 184(1) of Companies Act, 2013]

GENERAL NOTICE OF INTEREST

{company_name}
CIN: {cin}

I, {director_name} (DIN: {din}), hereby give notice that I have the following interest in other companies, firms, or bodies corporate:

{interest_details}

[AI will expand with proper format listing:
- Names of companies/firms
- Nature of interest (director, partner, shareholder)
- Extent of shareholding/interest]

I further confirm that:
1. The above information is true and correct
2. I will update this disclosure if any changes occur during the year
3. I will make fresh disclosure at the first board meeting of each financial year

For {company_name}

{director_name}
Director
DIN: {din}

Date:
Place:""",
                "tags": ["Companies Act", "MBP-1", "Section 184", "Director Interest"],
                "ai_enhanced": True
            },

            {
                "id": "form_inc22_address_change",
                "name": "INC-22 Change of Registered Office Address",
                "category": "corporate",
                "description": "Application for change of registered office address (Form INC-22)",
                "applicable_for": ["Corporate", "CS"],
                "fields": [
                    {"name": "company_name", "label": "Company Name", "type": "text", "required": True},
                    {"name": "cin", "label": "CIN", "type": "text", "required": True},
                    {"name": "old_address", "label": "Old Registered Office Address", "type": "multiline", "required": True},
                    {"name": "new_address", "label": "New Registered Office Address", "type": "multiline", "required": True},
                    {"name": "effective_date", "label": "Change Effective From", "type": "text", "required": True}
                ],
                "template_text": """To,
The Registrar of Companies
[State]

Date: [DATE]

Subject: Application for Change of Registered Office Address - Form INC-22

Company: {company_name}
CIN: {cin}

Respected Sir/Madam,

We hereby apply for change of registered office address of our company.

OLD ADDRESS:
{old_address}

NEW ADDRESS:
{new_address}

EFFECTIVE DATE: {effective_date}

The change of address was approved by the Board of Directors vide Resolution dated [DATE].

All documents including utility bills, lease deed, and board resolution are enclosed.

Kindly process and approve the change.

For {company_name}
CIN: {cin}

_____________________
Director

Enclosures:
1. Form INC-22
2. Board Resolution
3. Proof of new address
4. NOC from landlord (if applicable)""",
                "tags": ["Companies Act", "INC-22", "Registered Office", "Address Change"],
                "ai_enhanced": True
            },

            # ==================== ARBITRATION ACT TEMPLATES ====================
            {
                "id": "arbitration_notice",
                "name": "Arbitration Notice under Section 21",
                "category": "legal_notices",
                "description": "Notice invoking arbitration clause under Arbitration and Conciliation Act, 1996",
                "applicable_for": ["Lawyer", "Corporate", "CA"],
                "fields": [
                    {"name": "claimant_name", "label": "Claimant Name", "type": "text", "required": True},
                    {"name": "respondent_name", "label": "Respondent Name", "type": "text", "required": True},
                    {"name": "agreement_date", "label": "Agreement Date", "type": "text", "required": True},
                    {"name": "dispute_details", "label": "Details of Dispute", "type": "multiline", "required": True},
                    {"name": "arbitrator_name", "label": "Proposed Arbitrator Name (if any)", "type": "text", "required": False}
                ],
                "template_text": """ARBITRATION NOTICE
UNDER SECTION 21 OF THE ARBITRATION AND CONCILIATION ACT, 1996

To,
{respondent_name}
[Address]

Date: [DATE]

FROM: {claimant_name}

Dear Sir/Madam,

NOTICE OF INVOCATION OF ARBITRATION

We refer to the [Agreement/Contract] dated {agreement_date} entered into between us.

Pursuant to Clause [X] of the said agreement which contains an arbitration clause, we hereby invoke arbitration for resolution of the following dispute:

DISPUTE:
{dispute_details}

We hereby call upon you to:
1. Appoint an arbitrator within 30 days as per the agreement
2. Or agree to our proposed arbitrator: {arbitrator_name}

If you fail to appoint an arbitrator within the stipulated period, we shall proceed to appoint an arbitrator in accordance with the provisions of the Arbitration and Conciliation Act, 1996.

All our rights are reserved.

For {claimant_name}

Authorized Signatory
Date:""",
                "tags": ["Arbitration", "Section 21", "Legal Notice", "Dispute Resolution"],
                "ai_enhanced": True
            },

            # ==================== NEGOTIABLE INSTRUMENTS ACT ====================
            {
                "id": "cheque_bounce_notice_138",
                "name": "Legal Notice for Cheque Bounce (Section 138)",
                "category": "legal_notices",
                "description": "Notice under Section 138 of Negotiable Instruments Act for dishonored cheque",
                "applicable_for": ["Lawyer", "CA", "Corporate"],
                "fields": [
                    {"name": "sender_name", "label": "Sender/Payee Name", "type": "text", "required": True},
                    {"name": "drawer_name", "label": "Drawer/Accused Name", "type": "text", "required": True},
                    {"name": "cheque_number", "label": "Cheque Number", "type": "text", "required": True},
                    {"name": "cheque_date", "label": "Cheque Date", "type": "text", "required": True},
                    {"name": "cheque_amount", "label": "Cheque Amount (Rs.)", "type": "number", "required": True},
                    {"name": "bank_name", "label": "Bank Name", "type": "text", "required": True},
                    {"name": "bounce_reason", "label": "Reason for Dishonor", "type": "text", "required": True, "placeholder": "Insufficient funds"}
                ],
                "template_text": """LEGAL NOTICE
UNDER SECTION 138 OF THE NEGOTIABLE INSTRUMENTS ACT, 1881

To,
{drawer_name}
[Address]

Date: [DATE]

FROM: {sender_name}
[Address]

Dear Sir/Madam,

LEGAL NOTICE FOR DISHONOR OF CHEQUE

Under instructions from my client, {sender_name}, I am writing this notice regarding dishonor of cheque issued by you.

CHEQUE DETAILS:
- Cheque Number: {cheque_number}
- Date: {cheque_date}
- Amount: Rs. {cheque_amount}
- Drawn on: {bank_name}
- Payable to: {sender_name}

DISHONOR:
The above cheque was presented for payment but was dishonored with the remark: "{bounce_reason}".

The dishonor memo was received on [DATE].

NOTICE:
Pursuant to Section 138 of the Negotiable Instruments Act, 1881, you are called upon to pay the cheque amount of Rs. {cheque_amount} within 15 days from the receipt of this notice.

Failing which, criminal complaint under Section 138 shall be filed before the competent court, and you shall be liable for:
- Imprisonment up to 2 years
- Fine up to twice the cheque amount
- Both

Kindly make payment immediately.

For {sender_name}

[Lawyer Name]
Advocate
[Address]""",
                "tags": ["Negotiable Instruments Act", "Section 138", "Cheque Bounce", "Criminal"],
                "ai_enhanced": True
            },

            # ==================== LABOR LAWS - EXTENDED ====================
            {
                "id": "labor_license_application",
                "name": "Labor License Application (Shops & Establishments)",
                "category": "compliance",
                "description": "Application for labor license under Shops and Establishments Act",
                "applicable_for": ["Corporate", "CA"],
                "fields": [
                    {"name": "establishment_name", "label": "Establishment Name", "type": "text", "required": True},
                    {"name": "state", "label": "State", "type": "text", "required": True},
                    {"name": "number_of_employees", "label": "Number of Employees", "type": "number", "required": True},
                    {"name": "establishment_address", "label": "Establishment Address", "type": "multiline", "required": True},
                    {"name": "nature_of_business", "label": "Nature of Business", "type": "text", "required": True}
                ],
                "template_text": """To,
The Inspector of Shops and Establishments
[State]
[District]

Date: [DATE]

Subject: Application for Labor License

Establishment Name: {establishment_name}
State: {state}

Respected Sir/Madam,

We hereby apply for registration/license under the [State] Shops and Establishments Act.

ESTABLISHMENT DETAILS:
- Name: {establishment_name}
- Address: {establishment_address}
- Nature of Business: {nature_of_business}
- Number of Employees: {number_of_employees}

We understand that:
1. We will comply with all labor law provisions
2. We will maintain required registers and records
3. We will submit annual returns
4. We will allow inspection as per law

All required documents are enclosed.

Kindly process our application.

For {establishment_name}

Authorized Signatory

Enclosures:
1. Registration form
2. Address proof
3. ID proof of proprietor/partners/directors
4. Photo of establishment""",
                "tags": ["Labor Law", "Shops Act", "Establishment", "License"],
                "ai_enhanced": True
            },

            # ==================== SEBI & REGULATORY TEMPLATES ====================
            {
                "id": "sebi_disclosure_insider_trading",
                "name": "SEBI Disclosure - Insider Trading Compliance",
                "category": "sebi_regulatory",
                "description": "Disclosure under SEBI (Prohibition of Insider Trading) Regulations, 2015",
                "applicable_for": ["Corporate", "CS", "CFO"],
                "fields": [
                    {"name": "company_name", "label": "Company Name", "type": "text", "required": True},
                    {"name": "cin", "label": "CIN", "type": "text", "required": True},
                    {"name": "person_name", "label": "Insider Name", "type": "text", "required": True},
                    {"name": "pan_din", "label": "PAN/DIN", "type": "text", "required": True},
                    {"name": "designation", "label": "Designation", "type": "text", "required": True, "placeholder": "Director/Key Managerial Personnel"},
                    {"name": "transaction_type", "label": "Transaction Type", "type": "dropdown", "required": True, "options": ["Purchase", "Sale", "Pledge", "Release of Pledge", "Other"]},
                    {"name": "security_type", "label": "Type of Security", "type": "text", "required": True, "placeholder": "Equity Shares/Debentures"},
                    {"name": "quantity", "label": "Quantity", "type": "number", "required": True},
                    {"name": "transaction_date", "label": "Transaction Date", "type": "date", "required": True}
                ],
                "template_text": """DISCLOSURE UNDER REGULATION 7(2) OF SEBI (PROHIBITION OF INSIDER TRADING) REGULATIONS, 2015

{company_name}
CIN: {cin}

Date: [DATE]

To,
The Company Secretary
{company_name}
[Registered Office Address]

Dear Sir/Madam,

I, {person_name} (PAN/DIN: {pan_din}), holding the position of {designation} in {company_name}, hereby make the following disclosure as required under Regulation 7(2) of the SEBI (Prohibition of Insider Trading) Regulations, 2015.

DISCLOSURE DETAILS:

1. Name of Insider: {person_name}
2. Designation: {designation}
3. PAN/DIN: {pan_din}
4. Type of Transaction: {transaction_type}
5. Type of Security: {security_type}
6. Quantity: {quantity}
7. Transaction Date: {transaction_date}
8. Transaction Value: Rs. [Amount]

I confirm that:
- I am aware of my responsibilities under SEBI (PIT) Regulations, 2015
- This transaction has been disclosed within the prescribed timeline
- The information provided is true and correct

I further undertake to make timely disclosures of any future transactions as required under the Regulations.

For {company_name}

{person_name}
Designation: {designation}
PAN/DIN: {pan_din}

Date:
Place:""",
                "tags": ["SEBI", "Insider Trading", "Disclosure", "Regulation 7", "Compliance"],
                "ai_enhanced": True
            },

            {
                "id": "sebi_disclosure_related_party_transaction",
                "name": "SEBI Disclosure - Related Party Transaction",
                "category": "sebi_regulatory",
                "description": "Disclosure of material related party transaction under SEBI Listing Regulations",
                "applicable_for": ["Corporate", "CS", "CFO"],
                "fields": [
                    {"name": "company_name", "label": "Company Name", "type": "text", "required": True},
                    {"name": "cin", "label": "CIN", "type": "text", "required": True},
                    {"name": "related_party_name", "label": "Related Party Name", "type": "text", "required": True},
                    {"name": "relationship", "label": "Relationship with Company", "type": "dropdown", "required": True, "options": ["Director", "Key Managerial Personnel", "Relative of Director", "Subsidiary", "Associate Company", "Promoter", "Promoter Group"]},
                    {"name": "transaction_details", "label": "Transaction Details", "type": "multiline", "required": True, "placeholder": "Description of transaction, nature, terms"},
                    {"name": "transaction_value", "label": "Transaction Value (Rs.)", "type": "number", "required": True},
                    {"name": "transaction_date", "label": "Transaction Date", "type": "date", "required": True}
                ],
                "template_text": """DISCLOSURE OF MATERIAL RELATED PARTY TRANSACTION
UNDER REGULATION 23(1) OF SEBI (LISTING OBLIGATIONS AND DISCLOSURE REQUIREMENTS) REGULATIONS, 2015

{company_name}
CIN: {cin}

Date: [DATE]

To,
The Secretary
The Stock Exchanges
[BSE/NSE]

Subject: Disclosure of Material Related Party Transaction

Dear Sir/Madam,

Pursuant to Regulation 23(1) of the SEBI (Listing Obligations and Disclosure Requirements) Regulations, 2015, we hereby disclose the following material related party transaction entered into by {company_name}:

TRANSACTION DETAILS:

1. Company Name: {company_name}
2. CIN: {cin}
3. Related Party: {related_party_name}
4. Relationship: {relationship}
5. Transaction Details:
   {transaction_details}
6. Transaction Value: Rs. {transaction_value}
7. Transaction Date: {transaction_date}
8. Approving Authority: [Board of Directors/Audit Committee/Shareholders]

[AI will expand with:
- Details of approval process
- Fair value assessment
- Impact on company
- Compliance with policy]

The transaction has been entered into in the ordinary course of business and on an arm's length basis as per the Company's Related Party Transaction Policy.

For {company_name}
CIN: {cin}

_____________________
Company Secretary
Name: [Name]
SEBI Regn. No.: [If applicable]

Enclosures:
1. Copy of Board Resolution
2. Audit Committee approval (if applicable)
3. Related Party Transaction Policy""",
                "tags": ["SEBI", "Related Party", "Disclosure", "Regulation 23", "Listing Obligations"],
                "ai_enhanced": True
            },

            {
                "id": "sebi_disclosure_shares_pledge",
                "name": "SEBI Disclosure - Pledge/Release of Shares",
                "category": "sebi_regulatory",
                "description": "Disclosure of creation/release of pledge on shares under SEBI Listing Regulations",
                "applicable_for": ["Corporate", "CS"],
                "fields": [
                    {"name": "company_name", "label": "Company Name", "type": "text", "required": True},
                    {"name": "promoter_name", "label": "Promoter Name", "type": "text", "required": True},
                    {"name": "pan", "label": "PAN", "type": "text", "required": True},
                    {"name": "action_type", "label": "Action Type", "type": "dropdown", "required": True, "options": ["Creation of Pledge", "Release of Pledge", "Invocation of Pledge"]},
                    {"name": "pledged_shares", "label": "Number of Shares Pledged", "type": "number", "required": True},
                    {"name": "total_shareholding", "label": "Total Shareholding", "type": "number", "required": True},
                    {"name": "pledge_date", "label": "Date of Pledge/Release", "type": "date", "required": True},
                    {"name": "beneficiary", "label": "Beneficiary Name (if pledge created)", "type": "text", "required": False}
                ],
                "template_text": """DISCLOSURE UNDER REGULATION 31(2) OF SEBI (LISTING OBLIGATIONS AND DISCLOSURE REQUIREMENTS) REGULATIONS, 2015

DISCLOSURE OF {action_type.upper()} ON SHARES

{company_name}
CIN: [CIN]

Date: [DATE]

To,
The Secretary
The Stock Exchanges
[BSE/NSE]

Subject: Disclosure of {action_type} on Shares

Dear Sir/Madam,

Pursuant to Regulation 31(2) of the SEBI (Listing Obligations and Disclosure Requirements) Regulations, 2015, we hereby disclose the following information:

DISCLOSURE DETAILS:

1. Name of Company: {company_name}
2. Name of Promoter/Person: {promoter_name}
3. PAN: {pan}
4. Action: {action_type}
5. Date of Action: {pledge_date}
6. Number of Shares: {pledged_shares}
7. Percentage to Paid-up Capital: [{pledged_shares * 100 / total_shareholding}%]
8. Total Shareholding: {total_shareholding}
9. Total Pledged Shares (After this action): [Number]
10. Percentage of Shareholding Pledged: [Percentage]
{f'11. Beneficiary: {beneficiary}' if action_type == 'Creation of Pledge' else ''}

[AI will expand with:
- Details of pledge agreement
- Purpose of pledge
- Impact on shareholding pattern
- Total encumbered shares]

The Company confirms that all applicable disclosures have been made as per SEBI Regulations.

For {company_name}
CIN: [CIN]

_____________________
Company Secretary

Date:
Place:""",
                "tags": ["SEBI", "Pledge", "Shareholding", "Regulation 31", "Disclosure"],
                "ai_enhanced": True
            },

            {
                "id": "sebi_whistleblower_policy",
                "name": "SEBI Whistleblower/Vigil Mechanism Policy",
                "category": "sebi_regulatory",
                "description": "Whistleblower policy document as required under SEBI Listing Regulations",
                "applicable_for": ["Corporate", "CS"],
                "fields": [
                    {"name": "company_name", "label": "Company Name", "type": "text", "required": True},
                    {"name": "cin", "label": "CIN", "type": "text", "required": True},
                    {"name": "vigilance_officer_name", "label": "Vigilance Officer Name", "type": "text", "required": True},
                    {"name": "vigilance_officer_email", "label": "Vigilance Officer Email", "type": "text", "required": True},
                    {"name": "audit_committee_chairman", "label": "Audit Committee Chairman", "type": "text", "required": True}
                ],
                "template_text": """WHISTLEBLOWER / VIGIL MECHANISM POLICY

{company_name}
CIN: {cin}

[Pursuant to Regulation 22 of SEBI (Listing Obligations and Disclosure Requirements) Regulations, 2015 and Section 177 of Companies Act, 2013]

1. PREAMBLE

This Whistleblower Policy ("Policy") is formulated to provide a mechanism for employees, directors, and stakeholders of {company_name} to report instances of unethical behavior, actual or suspected fraud, or violation of the Company's Code of Conduct.

2. OBJECTIVES

- To encourage reporting of genuine concerns about unethical conduct
- To protect whistleblowers from victimization
- To ensure timely and fair investigation of complaints
- To ensure compliance with legal and regulatory requirements

3. SCOPE

This Policy applies to:
- All employees of the Company
- Directors and Key Managerial Personnel
- Contractors, vendors, and business partners
- Shareholders and other stakeholders

4. DEFINITIONS

"Whistleblower": A person who reports a concern under this Policy.
"Protected Disclosures": Disclosures made in good faith about unethical conduct.
"Vigilance Officer": The person designated to receive and investigate complaints.

5. VIGILANCE OFFICER

Name: {vigilance_officer_name}
Email: {vigilance_officer_email}
Designation: Company Secretary/Chief Compliance Officer

6. REPORTING MECHANISM

Complaints can be submitted:
- By email to: {vigilance_officer_email}
- By post to: Vigilance Officer, {company_name}, [Address]
- Through designated hotline: [Phone Number]

7. INVESTIGATION PROCESS

[AI will expand with detailed investigation procedure, timelines, and reporting mechanisms]

8. PROTECTION OF WHISTLEBLOWER

The Company will:
- Maintain confidentiality of the whistleblower's identity
- Protect from retaliation or victimization
- Not tolerate harassment or discrimination

9. AUDIT COMMITTEE OVERSIGHT

Chairman: {audit_committee_chairman}
The Audit Committee will review all complaints and ensure proper resolution.

10. ANNUAL REVIEW

This Policy will be reviewed annually by the Audit Committee and Board of Directors.

For {company_name}
CIN: {cin}

Approved by Board of Directors
Date: [DATE]

[AI will add detailed clauses covering all aspects of whistleblower protection and investigation]""",
                "tags": ["SEBI", "Whistleblower", "Vigil Mechanism", "Regulation 22", "Corporate Governance"],
                "ai_enhanced": True
            },

            {
                "id": "sebi_corporate_governance_report",
                "name": "SEBI Corporate Governance Report",
                "category": "sebi_regulatory",
                "description": "Corporate governance compliance report for listed companies under SEBI Listing Regulations",
                "applicable_for": ["Corporate", "CS"],
                "fields": [
                    {"name": "company_name", "label": "Company Name", "type": "text", "required": True},
                    {"name": "cin", "label": "CIN", "type": "text", "required": True},
                    {"name": "financial_year", "label": "Financial Year", "type": "text", "required": True, "placeholder": "2024-25"},
                    {"name": "board_meetings_held", "label": "Number of Board Meetings Held", "type": "number", "required": True},
                    {"name": "independent_directors", "label": "Number of Independent Directors", "type": "number", "required": True},
                    {"name": "women_directors", "label": "Number of Women Directors", "type": "number", "required": True}
                ],
                "template_text": """CORPORATE GOVERNANCE REPORT
UNDER REGULATION 27(2) OF SEBI (LISTING OBLIGATIONS AND DISCLOSURE REQUIREMENTS) REGULATIONS, 2015

{company_name}
CIN: {cin}
Financial Year: {financial_year}

CORPORATE GOVERNANCE COMPLIANCE REPORT

1. COMPANY'S PHILOSOPHY ON CORPORATE GOVERNANCE

[AI will add company's philosophy statement on corporate governance]

2. BOARD OF DIRECTORS

2.1 Composition of Board:
- Total Directors: [Number]
- Executive Directors: [Number]
- Non-Executive Directors: [Number]
- Independent Directors: {independent_directors}
- Women Directors: {women_directors}

2.2 Board Meetings:
- Number of meetings held during the year: {board_meetings_held}
- Attendance details: [AI will add attendance statistics]

2.3 Board Committees:
- Audit Committee
- Nomination and Remuneration Committee
- Stakeholders Relationship Committee
- Risk Management Committee

3. AUDIT COMMITTEE

[AI will expand with committee composition, meetings, and functions]

4. NOMINATION AND REMUNERATION COMMITTEE

[AI will expand with committee details and policies]

5. RELATED PARTY TRANSACTIONS

[AI will add details of related party transactions and compliance]

6. RISK MANAGEMENT

[AI will add risk management framework and procedures]

7. DISCLOSURES AND COMPLIANCE

[AI will add details of:
- Shareholder disclosures
- Code of conduct compliance
- Whistleblower mechanism
- Other regulatory compliances]

8. MEANS OF COMMUNICATION

- Financial results published in: [Newspapers]
- Website: [Company website]
- Email: [Investor email]

9. GENERAL SHAREHOLDER INFORMATION

[AI will add AGM details, dividend information, etc.]

10. CERTIFICATION

We confirm that the Company has complied with all applicable provisions of SEBI (Listing Obligations and Disclosure Requirements) Regulations, 2015 during the financial year {financial_year}.

For {company_name}
CIN: {cin}

_____________________
Managing Director

_____________________
Company Secretary
SEBI Regn. No.: [Number]

Date:
Place:""",
                "tags": ["SEBI", "Corporate Governance", "Regulation 27", "Compliance Report", "Listing Obligations"],
                "ai_enhanced": True
            },

            {
                "id": "sebi_security_and_cyber_security_policy",
                "name": "SEBI Information Security & Cyber Security Policy",
                "category": "sebi_regulatory",
                "description": "Information security and cyber security policy as required under SEBI Cyber Security Framework",
                "applicable_for": ["Corporate", "CS", "CFO"],
                "fields": [
                    {"name": "company_name", "label": "Company Name", "type": "text", "required": True},
                    {"name": "cin", "label": "CIN", "type": "text", "required": True},
                    {"name": "cio_ciso_name", "label": "CIO/CISO Name", "type": "text", "required": True},
                    {"name": "policy_effective_date", "label": "Policy Effective From", "type": "date", "required": True}
                ],
                "template_text": """INFORMATION SECURITY & CYBER SECURITY POLICY

{company_name}
CIN: {cin}

[Pursuant to SEBI Cyber Security Framework and Information Security Guidelines]

Policy Effective Date: {policy_effective_date}
Last Updated: [DATE]

1. INTRODUCTION

This Policy establishes the framework for managing information security and cyber security risks for {company_name}.

2. OBJECTIVES

- Protect Company's information assets
- Ensure business continuity
- Comply with regulatory requirements
- Protect stakeholder data and privacy

3. SCOPE

This Policy applies to:
- All IT systems and infrastructure
- Data and information assets
- Employees and third-party vendors
- All business processes

4. INFORMATION SECURITY MANAGEMENT

4.1 Information Classification:
- Confidential
- Internal Use
- Public

4.2 Access Control:
[AI will add access control procedures]

5. CYBER SECURITY FRAMEWORK

5.1 Chief Information Security Officer (CISO):
Name: {cio_ciso_name}
Designation: CIO/CISO

5.2 Security Measures:
[AI will add:
- Network security
- Application security
- Data encryption
- Incident response
- Business continuity plan]

6. RISK MANAGEMENT

[AI will add risk assessment and mitigation procedures]

7. INCIDENT REPORTING AND RESPONSE

[AI will add incident handling procedures and timelines]

8. VENDOR MANAGEMENT

[AI will add vendor security requirements and assessments]

9. TRAINING AND AWARENESS

[AI will add training programs for employees]

10. AUDIT AND COMPLIANCE

[AI will add audit procedures and compliance monitoring]

11. REVIEW AND UPDATES

This Policy will be reviewed annually and updated as required.

For {company_name}
CIN: {cin}

Approved by:
_____________________
Board of Directors
Date: [DATE]""",
                "tags": ["SEBI", "Cyber Security", "Information Security", "IT Security", "Compliance"],
                "ai_enhanced": True
            },

            {
                "id": "sebi_complaint_reply",
                "name": "SEBI Complaint/Show Cause Reply",
                "category": "sebi_regulatory",
                "description": "Reply to SEBI show cause notice or complaint",
                "applicable_for": ["Corporate", "CS", "Lawyer"],
                "fields": [
                    {"name": "company_name", "label": "Company Name", "type": "text", "required": True},
                    {"name": "cin", "label": "CIN", "type": "text", "required": True},
                    {"name": "notice_number", "label": "SEBI Notice/Complaint Number", "type": "text", "required": True},
                    {"name": "notice_date", "label": "Notice Date", "type": "text", "required": True},
                    {"name": "sebi_division", "label": "SEBI Division/Wing", "type": "text", "required": True, "placeholder": "Enforcement Division"},
                    {"name": "allegations", "label": "Allegations/Charges", "type": "multiline", "required": True},
                    {"name": "reply_points", "label": "Key Points for Reply", "type": "multiline", "required": True}
                ],
                "template_text": """To,
The Adjudicating Officer/Competent Authority
{sebi_division}
Securities and Exchange Board of India
SEBI Bhavan, Bandra Kurla Complex
Mumbai - 400051

Date: [DATE]

Subject: Reply to Show Cause Notice / Complaint No. {notice_number} dated {notice_date}

Ref: Company - {company_name}
CIN: {cin}

Respected Sir/Madam,

We refer to the Show Cause Notice / Complaint bearing reference {notice_number} dated {notice_date} issued by your office.

COMPANY DETAILS:
Name: {company_name}
CIN: {cin}
Registered Office: [Address]

ALLEGATIONS/CHARGES:

{allegations}

DETAILED REPLY:

{reply_points}

[AI will expand with:
1. Point-by-point response to each allegation
2. Facts and chronology
3. Legal provisions and case laws
4. Supporting evidence
5. Compliance measures taken]

SUBMISSIONS:

1. The allegations are denied for reasons stated above
2. The Company has complied with all applicable SEBI Regulations
3. All disclosures have been made in accordance with law
4. The Company is committed to maintaining highest standards of corporate governance

PRAYER:

In view of the above submissions, we pray that:
(a) The proceedings may be dropped
(b) The Company may be given a personal hearing opportunity
(c) Any further relief as deemed fit

All supporting documents are enclosed herewith.

Thanking you,

For {company_name}
CIN: {cin}

_____________________
Authorized Signatory
Name: [Name]
Designation: [Designation]

Date:
Place:

Enclosures:
1. Supporting Documents
2. Board Resolutions (if applicable)
3. Compliance Certificates""",
                "tags": ["SEBI", "Show Cause Notice", "Reply", "Complaint", "Regulatory"],
                "ai_enhanced": True
            },

            {
                "id": "rbi_compliance_certificate_nbfc",
                "name": "RBI Compliance Certificate - NBFC",
                "category": "sebi_regulatory",
                "description": "Compliance certificate for Non-Banking Financial Companies (NBFC) as required by RBI",
                "applicable_for": ["Corporate", "CA", "CFO"],
                "fields": [
                    {"name": "company_name", "label": "NBFC Company Name", "type": "text", "required": True},
                    {"name": "rbi_registration_no", "label": "RBI Registration Number", "type": "text", "required": True},
                    {"name": "financial_year", "label": "Financial Year", "type": "text", "required": True, "placeholder": "2024-25"},
                    {"name": "auditor_name", "label": "Auditor Name", "type": "text", "required": True},
                    {"name": "auditor_firm", "label": "Auditor Firm", "type": "text", "required": True}
                ],
                "template_text": """CERTIFICATE OF COMPLIANCE
[RBI MASTER DIRECTIONS - NON-BANKING FINANCIAL COMPANY (NBFC)]

To,
The Regional Director
Reserve Bank of India
[Regional Office]

Date: [DATE]

Subject: Annual Compliance Certificate for Financial Year {financial_year}

NBFC Name: {company_name}
RBI Registration No.: {rbi_registration_no}

We, {auditor_firm}, Chartered Accountants, have examined the books of accounts, records, and documents of {company_name} (RBI Registration No. {rbi_registration_no}) for the financial year ended March 31, [Year].

Based on our examination and to the best of our knowledge and information, and according to the explanations given to us, we certify that:

1. REGISTRATION AND AUTHORIZATION:
   - The Company holds valid Certificate of Registration (CoR) from RBI
   - All activities are within the scope of authorization
   - No unauthorized activities have been undertaken

2. PRUDENTIAL NORMS COMPLIANCE:
   - Capital Adequacy Ratio maintained as per RBI norms
   - Asset Classification norms complied with
   - Provisioning requirements met

3. REPORTING COMPLIANCE:
   - All periodic returns filed with RBI within prescribed timelines
   - Statistical returns submitted on time
   - Annual Financial Statements filed

4. INVESTMENT AND LENDING:
   - Investment in subsidiary/associate companies within limits
   - Lending to directors/relatives within prescribed norms
   - Single/Group exposure limits complied with

5. REGULATORY COMPLIANCE:
   - Fair Practices Code implemented
   - KYC/AML norms complied with
   - Customer grievance redressal mechanism operational

6. CORPORATE GOVERNANCE:
   - Board composition as per RBI guidelines
   - Audit Committee and other committees constituted
   - Fit and Proper criteria for directors complied

[AI will expand with detailed compliance checks as per RBI NBFC Directions]

For {auditor_firm}
Chartered Accountants

{auditor_name}
Partner
Membership No: [Number]
UDIN: [To be generated]

Date:
Place:

Note: This certificate is based on the information and explanations provided by the management.""",
                "tags": ["RBI", "NBFC", "Compliance", "Certificate", "Regulatory"],
                "ai_enhanced": True
            }
        ]

    def get_all_categories(self) -> Dict:
        """Get all template categories"""
        if not self._catalog_loaded:
            self._load_catalog()
        return self.catalog.get("categories", {})

    def get_templates_by_category(self, category: str) -> List[Template]:
        if not self._catalog_loaded:
            self._load_catalog()
        """Get templates for a specific category"""
        templates = [
            Template(**t) for t in self.catalog["templates"]
            if t["category"] == category
        ]
        return templates

    def get_template_by_id(self, template_id: str) -> Optional[Template]:
        if not self._catalog_loaded:
            self._load_catalog()
        """Get specific template by ID"""
        for t in self.catalog["templates"]:
            if t["id"] == template_id:
                return Template(**t)
        return None

    def search_templates(self, query: str, user_type: Optional[str] = None) -> List[Template]:
        if not self._catalog_loaded:
            self._load_catalog()
        """Search templates by query and user type"""
        results = []
        query_lower = query.lower()

        for t in self.catalog["templates"]:
            # Search in name, description, tags
            matches = (
                query_lower in t["name"].lower() or
                query_lower in t["description"].lower() or
                any(query_lower in tag.lower() for tag in t["tags"])
            )

            # Filter by user type if specified
            if user_type and user_type not in t["applicable_for"]:
                continue

            if matches:
                results.append(Template(**t))

        return results

    async def fill_template(
        self,
        template_id: str,
        field_values: Dict[str, Any],
        ai_enhance: bool = True
    ) -> str:
        """Fill template with provided values and optionally enhance with AI"""
        template = self.get_template_by_id(template_id)
        if not template:
            raise ValueError(f"Template {template_id} not found")

        # Basic string replacement
        filled_text = template.template_text
        for field_name, value in field_values.items():
            filled_text = filled_text.replace(f"{{{field_name}}}", str(value))

        # AI enhancement if requested
        if ai_enhance and template.ai_enhanced:
            from app.services.ai_service import ai_service

            enhancement_prompt = f"""You are a legal and corporate documentation expert for India.

The user has filled out a template for: {template.name}

Category: {template.category}
Description: {template.description}

Here is the filled template:

{filled_text}

Please enhance this document by:
1. Filling in any placeholder sections marked with [brackets] based on the context
2. Ensuring completeness - add any missing clauses or standard provisions
3. Improving professional language and formatting
4. Ensuring compliance with relevant Indian laws and regulations
5. Adding section numbers where appropriate
6. Expanding brief descriptions into complete legal language
7. Keep the overall structure but make it more comprehensive and professional

IMPORTANT:
- Maintain all user-provided information exactly as given
- Do not change dates, names, amounts, or specific details provided by user
- Only enhance, expand, and improve the template structure and language
- Make it ready for actual legal/business use

Return the enhanced, professional document:"""

            filled_text = await ai_service._generate_text(enhancement_prompt)

        return filled_text


# Singleton instance - lazy loading enabled
# Templates are loaded only when first accessed to save memory
template_service = TemplateService()
