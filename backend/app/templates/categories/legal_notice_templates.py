"""Legal Notice Templates"""

def get_legal_notice_templates():
    """Returns all legal notice templates"""
    return [
        {
            "id": "cease_desist_letter",
            "name": "Cease and Desist Letter",
            "category": "legal_notices",
            "description": "Legal notice to stop infringement or unauthorized activity",
            "applicable_for": ["Legal", "Corporate"],
            "fields": [
                {
                    "name": "sender_name",
                    "label": "Sender Name",
                    "type": "text",
                    "required": True
                },
                {
                    "name": "recipient_name",
                    "label": "Recipient Name",
                    "type": "text",
                    "required": True
                },
                {
                    "name": "infringement_description",
                    "label": "Description of Infringement/Issue",
                    "type": "multiline",
                    "required": True
                },
                {
                    "name": "compliance_deadline",
                    "label": "Compliance Deadline (days)",
                    "type": "number",
                    "required": True,
                    "placeholder": "7"
                }
            ],
            "template_text": """CEASE AND DESIST NOTICE

To: {recipient_name}

From: {sender_name}

Date: [DATE]

Subject: Cease and Desist from Unauthorized Activity

Dear Sir/Madam,

This letter serves as formal notice to immediately cease and desist from the following unauthorized activity:

{infringement_description}

[AI will expand with:
- Legal basis for the demand
- Evidence of infringement
- Consequences of non-compliance
- Deadline for compliance
- Legal remedies available]

You are required to comply with this notice within {compliance_deadline} days from the date of this letter.

Failure to comply will result in legal action without further notice.

Sincerely,

{sender_name}
Date:""",
            "tags": ["Cease and Desist", "Legal Notice", "Infringement"],
            "ai_enhanced": True
        },
        {
            "id": "consumer_complaint_notice",
            "name": "Consumer Complaint Notice",
            "category": "legal_notices",
            "description": "Legal notice for consumer complaint/deficiency in service",
            "applicable_for": ["Consumer", "Legal"],
            "fields": [
                {
                    "name": "complainant_name",
                    "label": "Complainant Name",
                    "type": "text",
                    "required": True
                },
                {
                    "name": "company_name",
                    "label": "Company/Service Provider Name",
                    "type": "text",
                    "required": True
                },
                {
                    "name": "product_service",
                    "label": "Product/Service",
                    "type": "text",
                    "required": True
                },
                {
                    "name": "complaint_details",
                    "label": "Complaint Details",
                    "type": "multiline",
                    "required": True
                },
                {
                    "name": "relief_sought",
                    "label": "Relief/Compensation Sought",
                    "type": "multiline",
                    "required": True
                }
            ],
            "template_text": """CONSUMER COMPLAINT NOTICE

To: {company_name}

From: {complainant_name}

Subject: Complaint regarding deficiency in service/product

Product/Service: {product_service}

COMPLAINT:
{complaint_details}

RELIEF SOUGHT:
{relief_sought}

[AI will expand with:
- Detailed chronology of events
- Evidence and documentation
- Relevant consumer protection laws
- Deadline for response
- Warning of consumer forum complaint]

Please resolve this matter within 15 days, failing which appropriate legal action will be initiated.

{complainant_name}
Date:""",
            "tags": ["Consumer Complaint", "Legal Notice", "Deficiency"],
            "ai_enhanced": True
        },
        {
            "id": "payment_demand_notice",
            "name": "Payment Demand Notice",
            "category": "legal_notices",
            "description": "Legal notice demanding payment of dues",
            "applicable_for": ["Legal", "Corporate"],
            "fields": [
                {
                    "name": "creditor_name",
                    "label": "Creditor Name",
                    "type": "text",
                    "required": True
                },
                {
                    "name": "debtor_name",
                    "label": "Debtor Name",
                    "type": "text",
                    "required": True
                },
                {
                    "name": "amount_due",
                    "label": "Amount Due (Rs.)",
                    "type": "number",
                    "required": True
                },
                {
                    "name": "invoice_details",
                    "label": "Invoice/Agreement Details",
                    "type": "multiline",
                    "required": True
                },
                {
                    "name": "payment_deadline",
                    "label": "Payment Deadline (days)",
                    "type": "number",
                    "required": True,
                    "placeholder": "7"
                }
            ],
            "template_text": """LEGAL NOTICE FOR PAYMENT OF DUES

To: {debtor_name}

From: {creditor_name}

Subject: Demand for Payment of Outstanding Dues

Amount Due: Rs. {amount_due}

INVOICE/AGREEMENT DETAILS:
{invoice_details}

[AI will expand with:
- Detailed account statement
- Legal basis for claim
- Interest and penalty clauses
- Consequences of non-payment
- Court jurisdiction]

You are hereby required to pay Rs. {amount_due} within {payment_deadline} days, failing which legal proceedings will be initiated.

{creditor_name}
Date:""",
            "tags": ["Payment Demand", "Legal Notice", "Debt Recovery"],
            "ai_enhanced": True
        },
        {
            "id": "defamation_notice",
            "name": "Defamation Notice",
            "category": "legal_notices",
            "description": "Legal notice for defamatory statements",
            "applicable_for": ["Legal", "Individual", "Corporate"],
            "fields": [
                {
                    "name": "aggrieved_person",
                    "label": "Aggrieved Person/Company Name",
                    "type": "text",
                    "required": True
                },
                {
                    "name": "defamer_name",
                    "label": "Person who Made Defamatory Statement",
                    "type": "text",
                    "required": True
                },
                {
                    "name": "defamatory_statement",
                    "label": "Defamatory Statement/Publication",
                    "type": "multiline",
                    "required": True
                },
                {
                    "name": "platform",
                    "label": "Platform/Medium",
                    "type": "text",
                    "required": True,
                    "placeholder": "Social media, newspaper, website, etc."
                },
                {
                    "name": "damages_claimed",
                    "label": "Damages Claimed (Rs.)",
                    "type": "number",
                    "required": False
                }
            ],
            "template_text": """LEGAL NOTICE FOR DEFAMATION

To: {defamer_name}

From: {aggrieved_person}

Subject: Notice for Defamatory Statements

Platform: {platform}

DEFAMATORY STATEMENT:
{defamatory_statement}

The above statement is false, defamatory, and has caused serious damage to the reputation of {aggrieved_person}.

DEMAND:
1. Immediate retraction and public apology
2. Removal of defamatory content
3. Compensation for damages: Rs. {damages_claimed}

[AI will expand with legal provisions under defamation law, evidence of damage, etc.]

Comply within 7 days, failing which civil and criminal proceedings will be initiated.

For {aggrieved_person}
Advocate
Date:""",
            "tags": ["Defamation", "Legal Notice", "Reputation", "IPC 499"],
            "ai_enhanced": True
        },
        {
            "id": "trademark_infringement_notice",
            "name": "Trademark Infringement Notice",
            "category": "legal_notices",
            "description": "Legal notice for trademark infringement",
            "applicable_for": ["Legal", "Corporate", "IP"],
            "fields": [
                {
                    "name": "trademark_owner",
                    "label": "Trademark Owner Name",
                    "type": "text",
                    "required": True
                },
                {
                    "name": "infringer_name",
                    "label": "Infringer Name",
                    "type": "text",
                    "required": True
                },
                {
                    "name": "trademark_details",
                    "label": "Trademark Details",
                    "type": "multiline",
                    "required": True,
                    "placeholder": "Mark, Registration Number, Class"
                },
                {
                    "name": "infringement_details",
                    "label": "Infringement Details",
                    "type": "multiline",
                    "required": True
                }
            ],
            "template_text": """TRADEMARK INFRINGEMENT NOTICE

To: {infringer_name}

From: {trademark_owner}

Subject: Notice for Trademark Infringement

REGISTERED TRADEMARK:
{trademark_details}

INFRINGEMENT:
{infringement_details}

You are using our registered trademark without authorization, causing confusion and dilution of our brand.

DEMAND:
1. Immediate cessation of trademark use
2. Destruction of infringing materials
3. Undertaking not to infringe in future
4. Damages and costs

[AI will expand with Trademarks Act provisions, confusion evidence, etc.]

Comply within 15 days or face legal action under Trademarks Act, 1999.

For {trademark_owner}
Advocate
Date:""",
            "tags": ["Trademark", "IP", "Infringement", "Legal Notice"],
            "ai_enhanced": True
        },
        {
            "id": "breach_of_contract_notice",
            "name": "Breach of Contract Notice",
            "category": "legal_notices",
            "description": "Legal notice for breach of contractual obligations",
            "applicable_for": ["Legal", "Corporate"],
            "fields": [
                {
                    "name": "aggrieved_party",
                    "label": "Aggrieved Party Name",
                    "type": "text",
                    "required": True
                },
                {
                    "name": "defaulting_party",
                    "label": "Defaulting Party Name",
                    "type": "text",
                    "required": True
                },
                {
                    "name": "contract_date",
                    "label": "Contract Date",
                    "type": "date",
                    "required": True
                },
                {
                    "name": "breach_details",
                    "label": "Breach Details",
                    "type": "multiline",
                    "required": True,
                    "placeholder": "Specific obligations breached"
                },
                {
                    "name": "compensation_claimed",
                    "label": "Compensation Claimed (Rs.)",
                    "type": "number",
                    "required": True
                }
            ],
            "template_text": """BREACH OF CONTRACT NOTICE

To: {defaulting_party}

From: {aggrieved_party}

Subject: Notice for Breach of Contract dated {contract_date}

BREACH OF CONTRACT:
{breach_details}

Your failure to perform contractual obligations has caused significant loss and damage.

DEMAND:
1. Specific performance of contract terms
2. Compensation for losses: Rs. {compensation_claimed}
3. Interest and costs

[AI will expand with contract clauses breached, damages calculation, remedies under Indian Contract Act]

Remedy the breach within 15 days or face arbitration/civil suit.

For {aggrieved_party}
Advocate
Date:""",
            "tags": ["Breach of Contract", "Legal Notice", "Contract Law"],
            "ai_enhanced": True
        },
        {
            "id": "employment_termination_notice",
            "name": "Employment Termination Notice",
            "category": "legal_notices",
            "description": "Legal notice for wrongful termination or employment dispute",
            "applicable_for": ["Legal", "Employee", "HR"],
            "fields": [
                {
                    "name": "employee_name",
                    "label": "Employee Name",
                    "type": "text",
                    "required": True
                },
                {
                    "name": "employer_name",
                    "label": "Employer Name",
                    "type": "text",
                    "required": True
                },
                {
                    "name": "termination_date",
                    "label": "Termination Date",
                    "type": "date",
                    "required": True
                },
                {
                    "name": "grounds",
                    "label": "Grounds for Challenge",
                    "type": "multiline",
                    "required": True,
                    "placeholder": "Wrongful termination, non-payment of dues, violation of labour laws, etc."
                },
                {
                    "name": "relief_sought",
                    "label": "Relief Sought",
                    "type": "multiline",
                    "required": True,
                    "placeholder": "Reinstatement, compensation, pending dues, etc."
                }
            ],
            "template_text": """EMPLOYMENT TERMINATION DISPUTE NOTICE

To: {employer_name}

From: {employee_name}

Subject: Notice Regarding Wrongful/Illegal Termination

Termination Date: {termination_date}

GROUNDS FOR CHALLENGE:
{grounds}

RELIEF SOUGHT:
{relief_sought}

[AI will expand with relevant labour law provisions, Industrial Disputes Act, service record, etc.]

Resolve this matter within 15 days, failing which complaint will be filed with Labour Commissioner/Industrial Tribunal.

{employee_name}
Date:""",
            "tags": ["Employment", "Termination", "Labour Law", "Legal Notice"],
            "ai_enhanced": True
        },
        {
            "id": "property_encroachment_notice",
            "name": "Property Encroachment Notice",
            "category": "legal_notices",
            "description": "Legal notice for property encroachment or trespass",
            "applicable_for": ["Legal", "Property Owner"],
            "fields": [
                {
                    "name": "owner_name",
                    "label": "Property Owner Name",
                    "type": "text",
                    "required": True
                },
                {
                    "name": "encroacher_name",
                    "label": "Encroacher/Trespasser Name",
                    "type": "text",
                    "required": True
                },
                {
                    "name": "property_details",
                    "label": "Property Details",
                    "type": "multiline",
                    "required": True,
                    "placeholder": "Address, Survey Number, Area"
                },
                {
                    "name": "encroachment_details",
                    "label": "Encroachment Details",
                    "type": "multiline",
                    "required": True,
                    "placeholder": "Nature of encroachment, date noticed, area affected"
                }
            ],
            "template_text": """PROPERTY ENCROACHMENT NOTICE

To: {encroacher_name}

From: {owner_name}

Subject: Notice to Vacate and Remove Encroachment

PROPERTY DETAILS:
{property_details}

ENCROACHMENT:
{encroachment_details}

You are illegally occupying/encroaching upon my property without any right, title, or authority.

DEMAND:
1. Immediate vacation of property
2. Removal of all encroachments/structures
3. Handover peaceful possession
4. Compensation for unlawful occupation

[AI will expand with title documents, trespass law, suit for possession, injunction remedies]

Vacate within 7 days or face civil and criminal proceedings for trespass.

For {owner_name}
Advocate
Date:""",
            "tags": ["Property", "Encroachment", "Trespass", "Legal Notice", "Real Estate"],
            "ai_enhanced": True
        }
    ]
