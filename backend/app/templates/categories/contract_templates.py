"""Contract Templates"""

def get_contract_templates():
    """Returns all contract templates"""
    return [
        {
            "id": "employment_agreement",
            "name": "Employment Agreement",
            "category": "contracts",
            "description": "Standard employment contract template",
            "applicable_for": ["Corporate", "HR", "Legal"],
            "fields": [
                {
                    "name": "company_name",
                    "label": "Company Name",
                    "type": "text",
                    "required": True
                },
                {
                    "name": "employee_name",
                    "label": "Employee Name",
                    "type": "text",
                    "required": True
                },
                {
                    "name": "designation",
                    "label": "Designation/Position",
                    "type": "text",
                    "required": True
                },
                {
                    "name": "start_date",
                    "label": "Start Date",
                    "type": "date",
                    "required": True
                },
                {
                    "name": "salary",
                    "label": "Annual Salary (Rs.)",
                    "type": "number",
                    "required": True
                },
                {
                    "name": "notice_period",
                    "label": "Notice Period (days)",
                    "type": "number",
                    "required": True,
                    "placeholder": "30"
                }
            ],
            "template_text": """EMPLOYMENT AGREEMENT

This Agreement is made on [DATE] between:

EMPLOYER: {company_name}
EMPLOYEE: {employee_name}

1. POSITION AND DUTIES:
   The Employee is appointed as {designation} effective from {start_date}.

2. COMPENSATION:
   Annual Salary: Rs. {salary}

3. NOTICE PERIOD:
   {notice_period} days

[AI will expand with:
- Detailed job responsibilities
- Benefits and perks
- Working hours
- Leave policy
- Confidentiality clauses
- Non-compete clauses
- Termination conditions
- Other standard employment terms]

SIGNATURES:

For {company_name}                {employee_name}
Employer                           Employee

Date:
Place:""",
            "tags": ["Employment", "Contract", "HR", "Agreement"],
            "ai_enhanced": True
        },
        {
            "id": "consultant_agreement",
            "name": "Consultancy Agreement",
            "category": "contracts",
            "description": "Professional consultancy services agreement",
            "applicable_for": ["Corporate", "Professional", "Legal"],
            "fields": [
                {
                    "name": "client_name",
                    "label": "Client Name",
                    "type": "text",
                    "required": True
                },
                {
                    "name": "consultant_name",
                    "label": "Consultant Name",
                    "type": "text",
                    "required": True
                },
                {
                    "name": "services_description",
                    "label": "Services Description",
                    "type": "multiline",
                    "required": True
                },
                {
                    "name": "contract_duration",
                    "label": "Contract Duration (months)",
                    "type": "number",
                    "required": True
                },
                {
                    "name": "fees",
                    "label": "Professional Fees (Rs.)",
                    "type": "number",
                    "required": True
                }
            ],
            "template_text": """CONSULTANCY AGREEMENT

Between:
CLIENT: {client_name}
CONSULTANT: {consultant_name}

SERVICES:
{services_description}

TERMS:
- Duration: {contract_duration} months
- Fees: Rs. {fees}

[AI will expand with detailed terms, payment schedule, deliverables, IP rights, etc.]

CLIENT                             CONSULTANT
{client_name}                      {consultant_name}

Date:""",
            "tags": ["Consultancy", "Contract", "Professional Services"],
            "ai_enhanced": True
        },
        {
            "id": "vendor_agreement",
            "name": "Vendor/Supplier Agreement",
            "category": "contracts",
            "description": "Agreement with vendors for supply of goods/services",
            "applicable_for": ["Corporate", "Procurement"],
            "fields": [
                {
                    "name": "buyer_name",
                    "label": "Buyer/Company Name",
                    "type": "text",
                    "required": True
                },
                {
                    "name": "vendor_name",
                    "label": "Vendor/Supplier Name",
                    "type": "text",
                    "required": True
                },
                {
                    "name": "goods_services",
                    "label": "Goods/Services Description",
                    "type": "multiline",
                    "required": True
                },
                {
                    "name": "payment_terms",
                    "label": "Payment Terms",
                    "type": "text",
                    "required": True,
                    "placeholder": "e.g., Net 30 days"
                }
            ],
            "template_text": """VENDOR AGREEMENT

BUYER: {buyer_name}
VENDOR: {vendor_name}

SCOPE OF SUPPLY:
{goods_services}

PAYMENT TERMS:
{payment_terms}

[AI will expand with quality standards, delivery terms, warranties, etc.]

For {buyer_name}                   For {vendor_name}
Authorized Signatory               Authorized Signatory

Date:""",
            "tags": ["Vendor", "Supplier", "Procurement", "Contract"],
            "ai_enhanced": True
        },
        {
            "id": "partnership_deed",
            "name": "Partnership Deed",
            "category": "contracts",
            "description": "Partnership agreement between partners",
            "applicable_for": ["Legal", "Corporate", "CA"],
            "fields": [
                {
                    "name": "firm_name",
                    "label": "Firm/Partnership Name",
                    "type": "text",
                    "required": True
                },
                {
                    "name": "partner_names",
                    "label": "Partners' Names (comma separated)",
                    "type": "multiline",
                    "required": True,
                    "placeholder": "Partner 1 - 50% share\nPartner 2 - 50% share"
                },
                {
                    "name": "business_nature",
                    "label": "Nature of Business",
                    "type": "text",
                    "required": True
                },
                {
                    "name": "capital_contribution",
                    "label": "Total Capital (Rs.)",
                    "type": "number",
                    "required": True
                }
            ],
            "template_text": """PARTNERSHIP DEED

FIRM NAME: {firm_name}

PARTNERS:
{partner_names}

BUSINESS: {business_nature}

CAPITAL: Rs. {capital_contribution}

[AI will expand with profit sharing, decision making, dissolution terms, etc.]

SIGNATURES OF PARTNERS:

Date:
Place:""",
            "tags": ["Partnership", "Deed", "Business", "Contract"],
            "ai_enhanced": True
        },
        {
            "id": "nda_agreement",
            "name": "Non-Disclosure Agreement (NDA)",
            "category": "contracts",
            "description": "Confidentiality agreement",
            "applicable_for": ["Corporate", "Legal"],
            "fields": [
                {
                    "name": "disclosing_party",
                    "label": "Disclosing Party Name",
                    "type": "text",
                    "required": True
                },
                {
                    "name": "receiving_party",
                    "label": "Receiving Party Name",
                    "type": "text",
                    "required": True
                },
                {
                    "name": "purpose",
                    "label": "Purpose of Disclosure",
                    "type": "multiline",
                    "required": True
                },
                {
                    "name": "duration_years",
                    "label": "Confidentiality Duration (years)",
                    "type": "number",
                    "required": True,
                    "placeholder": "2"
                }
            ],
            "template_text": """NON-DISCLOSURE AGREEMENT

DISCLOSING PARTY: {disclosing_party}
RECEIVING PARTY: {receiving_party}

PURPOSE: {purpose}

CONFIDENTIALITY PERIOD: {duration_years} years

[AI will expand with detailed confidentiality obligations, exclusions, remedies, etc.]

DISCLOSING PARTY              RECEIVING PARTY
{disclosing_party}            {receiving_party}

Date:""",
            "tags": ["NDA", "Confidentiality", "Contract", "Agreement"],
            "ai_enhanced": True
        },
        {
            "id": "franchise_agreement",
            "name": "Franchise Agreement",
            "category": "contracts",
            "description": "Franchise business agreement between franchisor and franchisee",
            "applicable_for": ["Corporate", "Legal", "Business"],
            "fields": [
                {
                    "name": "franchisor_name",
                    "label": "Franchisor Name",
                    "type": "text",
                    "required": True
                },
                {
                    "name": "franchisee_name",
                    "label": "Franchisee Name",
                    "type": "text",
                    "required": True
                },
                {
                    "name": "brand_name",
                    "label": "Brand/Business Name",
                    "type": "text",
                    "required": True
                },
                {
                    "name": "territory",
                    "label": "Franchise Territory",
                    "type": "text",
                    "required": True,
                    "placeholder": "City/Region"
                },
                {
                    "name": "franchise_fee",
                    "label": "Initial Franchise Fee (Rs.)",
                    "type": "number",
                    "required": True
                },
                {
                    "name": "royalty_percentage",
                    "label": "Royalty Percentage (%)",
                    "type": "number",
                    "required": True
                },
                {
                    "name": "agreement_term",
                    "label": "Agreement Term (years)",
                    "type": "number",
                    "required": True
                }
            ],
            "template_text": """FRANCHISE AGREEMENT

FRANCHISOR: {franchisor_name}
FRANCHISEE: {franchisee_name}

BRAND: {brand_name}

TERRITORY: {territory}

FINANCIAL TERMS:
- Initial Franchise Fee: Rs. {franchise_fee}
- Royalty: {royalty_percentage}% of gross revenue
- Term: {agreement_term} years

[AI will expand with operational standards, training, marketing, IP rights, renewal terms, etc.]

FRANCHISOR                         FRANCHISEE
{franchisor_name}                  {franchisee_name}

Date:
Place:""",
            "tags": ["Franchise", "Business", "Contract", "Agreement"],
            "ai_enhanced": True
        },
        {
            "id": "distribution_agreement",
            "name": "Distribution Agreement",
            "category": "contracts",
            "description": "Agreement appointing distributor for products",
            "applicable_for": ["Corporate", "Business"],
            "fields": [
                {
                    "name": "manufacturer_name",
                    "label": "Manufacturer/Principal Name",
                    "type": "text",
                    "required": True
                },
                {
                    "name": "distributor_name",
                    "label": "Distributor Name",
                    "type": "text",
                    "required": True
                },
                {
                    "name": "products",
                    "label": "Products to be Distributed",
                    "type": "multiline",
                    "required": True
                },
                {
                    "name": "territory",
                    "label": "Distribution Territory",
                    "type": "text",
                    "required": True
                },
                {
                    "name": "minimum_purchase",
                    "label": "Minimum Annual Purchase (Rs.)",
                    "type": "number",
                    "required": True
                }
            ],
            "template_text": """DISTRIBUTION AGREEMENT

PRINCIPAL: {manufacturer_name}
DISTRIBUTOR: {distributor_name}

PRODUCTS:
{products}

TERRITORY: {territory}

MINIMUM PURCHASE: Rs. {minimum_purchase} per annum

[AI will expand with pricing, payment terms, exclusivity, marketing support, etc.]

PRINCIPAL                          DISTRIBUTOR
{manufacturer_name}                {distributor_name}

Date:""",
            "tags": ["Distribution", "Business", "Contract", "Channel Partner"],
            "ai_enhanced": True
        },
        {
            "id": "licensing_agreement",
            "name": "Licensing Agreement",
            "category": "contracts",
            "description": "License agreement for IP, technology, or trademark",
            "applicable_for": ["Corporate", "Legal", "IP"],
            "fields": [
                {
                    "name": "licensor_name",
                    "label": "Licensor Name",
                    "type": "text",
                    "required": True
                },
                {
                    "name": "licensee_name",
                    "label": "Licensee Name",
                    "type": "text",
                    "required": True
                },
                {
                    "name": "licensed_property",
                    "label": "Licensed Property/IP",
                    "type": "multiline",
                    "required": True,
                    "placeholder": "Patent, Trademark, Copyright, Technology, etc."
                },
                {
                    "name": "license_fee",
                    "label": "License Fee (Rs.)",
                    "type": "number",
                    "required": True
                },
                {
                    "name": "license_duration",
                    "label": "License Duration (years)",
                    "type": "number",
                    "required": True
                }
            ],
            "template_text": """LICENSING AGREEMENT

LICENSOR: {licensor_name}
LICENSEE: {licensee_name}

LICENSED PROPERTY:
{licensed_property}

TERMS:
- License Fee: Rs. {license_fee}
- Duration: {license_duration} years

[AI will expand with scope of license, restrictions, royalties, quality control, etc.]

LICENSOR                           LICENSEE
{licensor_name}                    {licensee_name}

Date:""",
            "tags": ["Licensing", "IP", "Contract", "Intellectual Property"],
            "ai_enhanced": True
        },
        {
            "id": "agency_agreement",
            "name": "Agency Agreement",
            "category": "contracts",
            "description": "Appointment of agent for business representation",
            "applicable_for": ["Corporate", "Business"],
            "fields": [
                {
                    "name": "principal_name",
                    "label": "Principal Name",
                    "type": "text",
                    "required": True
                },
                {
                    "name": "agent_name",
                    "label": "Agent Name",
                    "type": "text",
                    "required": True
                },
                {
                    "name": "agency_scope",
                    "label": "Scope of Agency",
                    "type": "multiline",
                    "required": True,
                    "placeholder": "Powers and duties of the agent"
                },
                {
                    "name": "commission_rate",
                    "label": "Commission Rate (%)",
                    "type": "number",
                    "required": True
                }
            ],
            "template_text": """AGENCY AGREEMENT

PRINCIPAL: {principal_name}
AGENT: {agent_name}

SCOPE OF AGENCY:
{agency_scope}

COMMISSION: {commission_rate}% on sales/transactions

[AI will expand with agent powers, limitations, territory, termination, etc.]

PRINCIPAL                          AGENT
{principal_name}                   {agent_name}

Date:""",
            "tags": ["Agency", "Business", "Contract", "Commission"],
            "ai_enhanced": True
        },
        {
            "id": "mou_agreement",
            "name": "Memorandum of Understanding (MOU)",
            "category": "contracts",
            "description": "MOU for business collaboration or partnership intent",
            "applicable_for": ["Corporate", "Business", "Legal"],
            "fields": [
                {
                    "name": "party1_name",
                    "label": "Party 1 Name",
                    "type": "text",
                    "required": True
                },
                {
                    "name": "party2_name",
                    "label": "Party 2 Name",
                    "type": "text",
                    "required": True
                },
                {
                    "name": "collaboration_purpose",
                    "label": "Purpose of Collaboration",
                    "type": "multiline",
                    "required": True
                },
                {
                    "name": "key_terms",
                    "label": "Key Terms & Understandings",
                    "type": "multiline",
                    "required": True
                }
            ],
            "template_text": """MEMORANDUM OF UNDERSTANDING

Between:
PARTY 1: {party1_name}
PARTY 2: {party2_name}

PURPOSE:
{collaboration_purpose}

KEY TERMS:
{key_terms}

[AI will expand with objectives, responsibilities, timelines, binding vs non-binding clauses, etc.]

PARTY 1                            PARTY 2
{party1_name}                      {party2_name}

Date:
Place:""",
            "tags": ["MOU", "Collaboration", "Business", "Agreement"],
            "ai_enhanced": True
        }
    ]
