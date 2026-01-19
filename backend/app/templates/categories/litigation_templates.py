"""Litigation & Court Practice Templates"""

def get_litigation_templates():
    """Returns all litigation and court filing templates"""
    return [
        {
            "id": "plaint_money_recovery",
            "name": "Plaint for Money Recovery (CPC)",
            "category": "litigation",
            "description": "Civil plaint for recovery of money/dues under CPC",
            "applicable_for": ["Lawyer", "Legal Professional"],
            "fields": [
                {"name": "court_name", "label": "Court Name", "type": "text", "required": True, "placeholder": "Court of Civil Judge, District"},
                {"name": "plaintiff_name", "label": "Plaintiff Name", "type": "text", "required": True},
                {"name": "defendant_name", "label": "Defendant Name", "type": "text", "required": True},
                {"name": "claim_amount", "label": "Claim Amount (Rs.)", "type": "number", "required": True},
                {"name": "cause_of_action", "label": "Cause of Action", "type": "multiline", "required": True},
                {"name": "facts", "label": "Facts of the Case", "type": "multiline", "required": True}
            ],
            "template_text": """IN THE {court_name}

CIVIL SUIT NO. ____/2026

{plaintiff_name} ... Plaintiff
Vs.
{defendant_name} ... Defendant

PLAINT

The Plaintiff most respectfully submits:

1. PARTIES:
   Plaintiff: {plaintiff_name}
   Defendant: {defendant_name}

2. FACTS:
{facts}

3. CAUSE OF ACTION:
{cause_of_action}

4. CLAIM:
   Amount: Rs. {claim_amount}

PRAYER:
It is therefore prayed that this Hon'ble Court may be pleased to:
a) Decree the suit in favor of the Plaintiff
b) Direct the Defendant to pay Rs. {claim_amount} with interest
c) Grant any other relief

Place:
Date:
                                                    Plaintiff/Advocate""",
            "tags": ["Litigation", "Civil", "Money Recovery", "Plaint"],
            "ai_enhanced": True
        },
        {
            "id": "written_statement_civil",
            "name": "Written Statement (Civil Suit)",
            "category": "litigation",
            "description": "Written statement/defense in civil suit",
            "applicable_for": ["Lawyer", "Legal Professional"],
            "fields": [
                {"name": "court_name", "label": "Court Name", "type": "text", "required": True},
                {"name": "suit_number", "label": "Suit Number", "type": "text", "required": True},
                {"name": "defendant_name", "label": "Defendant Name", "type": "text", "required": True},
                {"name": "plaintiff_name", "label": "Plaintiff Name", "type": "text", "required": True},
                {"name": "defense_points", "label": "Defense/Reply Points", "type": "multiline", "required": True}
            ],
            "template_text": """IN THE {court_name}

CIVIL SUIT NO. {suit_number}

WRITTEN STATEMENT

Defendant: {defendant_name}
Plaintiff: {plaintiff_name}

The Defendant submits this Written Statement:

REPLY TO PLAINT:
{defense_points}

[AI will expand with para-wise reply, legal defenses, and counter-claims if any]

PRAYER:
The suit may be dismissed with costs.

Defendant/Advocate
Date:""",
            "tags": ["Litigation", "Written Statement", "Civil Defense"],
            "ai_enhanced": True
        },
        {
            "id": "interim_application",
            "name": "Interim Application (IA)",
            "category": "litigation",
            "description": "Interim/Interlocutory Application format",
            "applicable_for": ["Lawyer", "Legal Professional"],
            "fields": [
                {"name": "court_name", "label": "Court Name", "type": "text", "required": True},
                {"name": "case_number", "label": "Case Number", "type": "text", "required": True},
                {"name": "applicant_name", "label": "Applicant Name", "type": "text", "required": True},
                {"name": "application_under", "label": "Application Under (Section/Order)", "type": "text", "required": True},
                {"name": "relief_sought", "label": "Relief Sought", "type": "multiline", "required": True},
                {"name": "grounds", "label": "Grounds", "type": "multiline", "required": True}
            ],
            "template_text": """IN THE {court_name}

{case_number}

INTERIM APPLICATION UNDER {application_under}

Applicant: {applicant_name}

RELIEF SOUGHT:
{relief_sought}

GROUNDS:
{grounds}

[AI expands with legal provisions and precedents]

PRAYER:
Grant the interim relief as prayed.

Applicant/Advocate
Date:""",
            "tags": ["Litigation", "IA", "Interim Application"],
            "ai_enhanced": True
        },
        {
            "id": "caveat_petition",
            "name": "Caveat Petition (Section 148A CPC)",
            "category": "litigation",
            "description": "Caveat petition to prevent ex-parte orders",
            "applicable_for": ["Lawyer", "Legal Professional"],
            "fields": [
                {"name": "court_name", "label": "Court Name", "type": "text", "required": True},
                {"name": "caveator_name", "label": "Caveator Name", "type": "text", "required": True},
                {"name": "opposite_party", "label": "Opposite Party Name", "type": "text", "required": True},
                {"name": "matter_details", "label": "Matter Details", "type": "multiline", "required": True}
            ],
            "template_text": """IN THE {court_name}

CAVEAT PETITION u/s 148A CPC

Caveator: {caveator_name}

The Caveator apprehends that {opposite_party} may file proceedings without notice.

MATTER:
{matter_details}

PRAYER:
No order be passed without hearing the Caveator.

Caveator/Advocate
Date:""",
            "tags": ["Litigation", "Caveat", "CPC"],
            "ai_enhanced": True
        },
        {
            "id": "execution_petition",
            "name": "Execution Petition",
            "category": "litigation",
            "description": "Petition for execution of decree/order",
            "applicable_for": ["Lawyer", "Legal Professional"],
            "fields": [
                {"name": "court_name", "label": "Court Name", "type": "text", "required": True},
                {"name": "decree_holder", "label": "Decree Holder Name", "type": "text", "required": True},
                {"name": "judgment_debtor", "label": "Judgment Debtor Name", "type": "text", "required": True},
                {"name": "decree_details", "label": "Decree Details", "type": "multiline", "required": True},
                {"name": "amount_due", "label": "Amount Due (Rs.)", "type": "number", "required": True}
            ],
            "template_text": """IN THE {court_name}

EXECUTION PETITION

Decree Holder: {decree_holder}
Judgment Debtor: {judgment_debtor}

DECREE:
{decree_details}

AMOUNT DUE: Rs. {amount_due}

PRAYER:
Execute the decree and recover the amount.

Decree Holder/Advocate
Date:""",
            "tags": ["Litigation", "Execution", "Decree"],
            "ai_enhanced": True
        },
        {
            "id": "condonation_delay",
            "name": "Application for Condonation of Delay",
            "category": "litigation",
            "description": "Application to condone delay in filing",
            "applicable_for": ["Lawyer", "Legal Professional"],
            "fields": [
                {"name": "court_name", "label": "Court Name", "type": "text", "required": True},
                {"name": "applicant_name", "label": "Applicant Name", "type": "text", "required": True},
                {"name": "delay_period", "label": "Period of Delay", "type": "text", "required": True},
                {"name": "reasons_for_delay", "label": "Reasons for Delay", "type": "multiline", "required": True}
            ],
            "template_text": """IN THE {court_name}

APPLICATION FOR CONDONATION OF DELAY

Applicant: {applicant_name}
Delay: {delay_period}

REASONS:
{reasons_for_delay}

[AI expands with sufficient cause and precedents]

PRAYER:
Condone the delay and admit the matter.

Applicant/Advocate
Date:""",
            "tags": ["Litigation", "Condonation", "Delay"],
            "ai_enhanced": True
        },
        {
            "id": "certified_copy_application",
            "name": "Application for Certified Copy",
            "category": "litigation",
            "description": "Application for certified copy of documents/orders",
            "applicable_for": ["Lawyer", "Individual", "Legal Professional"],
            "fields": [
                {"name": "court_name", "label": "Court Name", "type": "text", "required": True},
                {"name": "case_number", "label": "Case Number", "type": "text", "required": True},
                {"name": "applicant_name", "label": "Applicant Name", "type": "text", "required": True},
                {"name": "document_details", "label": "Document/Order Details Required", "type": "multiline", "required": True}
            ],
            "template_text": """IN THE {court_name}

CASE NO. {case_number}

APPLICATION FOR CERTIFIED COPY

Applicant: {applicant_name}

DOCUMENTS REQUIRED:
{document_details}

PRAYER:
Grant certified copy of the above documents.

Applicant/Advocate
Date:""",
            "tags": ["Litigation", "Certified Copy", "Court Documents"],
            "ai_enhanced": False
        },
        {
            "id": "order_7_rule_11",
            "name": "Application under Order 7 Rule 11 CPC",
            "category": "litigation",
            "description": "Application for rejection of plaint",
            "applicable_for": ["Lawyer", "Legal Professional"],
            "fields": [
                {"name": "court_name", "label": "Court Name", "type": "text", "required": True},
                {"name": "suit_number", "label": "Suit Number", "type": "text", "required": True},
                {"name": "defendant_name", "label": "Defendant Name", "type": "text", "required": True},
                {"name": "grounds", "label": "Grounds for Rejection", "type": "multiline", "required": True}
            ],
            "template_text": """IN THE {court_name}

SUIT NO. {suit_number}

APPLICATION u/O 7 R 11 CPC

Defendant: {defendant_name}

GROUNDS FOR REJECTION OF PLAINT:
{grounds}

[AI expands with legal grounds - cause of action, jurisdiction, limitation, etc.]

PRAYER:
Reject the plaint.

Defendant/Advocate
Date:""",
            "tags": ["Litigation", "Order 7 Rule 11", "Plaint Rejection"],
            "ai_enhanced": True
        },
        {
            "id": "temporary_injunction_order39",
            "name": "Application for Temporary Injunction (Order 39)",
            "category": "litigation",
            "description": "Application for temporary/interim injunction",
            "applicable_for": ["Lawyer", "Legal Professional"],
            "fields": [
                {"name": "court_name", "label": "Court Name", "type": "text", "required": True},
                {"name": "case_number", "label": "Case Number", "type": "text", "required": True},
                {"name": "applicant_name", "label": "Applicant Name", "type": "text", "required": True},
                {"name": "injunction_sought", "label": "Injunction Sought", "type": "multiline", "required": True},
                {"name": "urgent_need", "label": "Why Injunction is Urgent", "type": "multiline", "required": True}
            ],
            "template_text": """IN THE {court_name}

{case_number}

APPLICATION FOR TEMPORARY INJUNCTION u/O 39 R 1&2 CPC

Applicant: {applicant_name}

INJUNCTION SOUGHT:
{injunction_sought}

URGENCY:
{urgent_need}

[AI expands with prima facie case, balance of convenience, irreparable injury]

PRAYER:
Grant temporary injunction as prayed.

Applicant/Advocate
Date:""",
            "tags": ["Litigation", "Injunction", "Order 39", "Interim Relief"],
            "ai_enhanced": True
        },
        {
            "id": "affidavit_evidence",
            "name": "Affidavit of Evidence",
            "category": "litigation",
            "description": "Affidavit of evidence for plaintiff/defendant",
            "applicable_for": ["Lawyer", "Legal Professional"],
            "fields": [
                {"name": "court_name", "label": "Court Name", "type": "text", "required": True},
                {"name": "case_number", "label": "Case Number", "type": "text", "required": True},
                {"name": "deponent_name", "label": "Deponent Name", "type": "text", "required": True},
                {"name": "deponent_status", "label": "Deponent Status", "type": "dropdown", "required": True, "options": ["Plaintiff", "Defendant", "Witness"]},
                {"name": "evidence_facts", "label": "Facts to be Deposed", "type": "multiline", "required": True}
            ],
            "template_text": """IN THE {court_name}

{case_number}

AFFIDAVIT OF EVIDENCE

I, {deponent_name}, {deponent_status}, do hereby solemnly affirm and state:

1. I am the {deponent_status} in this case and am well acquainted with the facts.

2. EVIDENCE:
{evidence_facts}

[AI expands with proper affidavit format and verification]

VERIFICATION:
Verified that the contents are true to my knowledge.

{deponent_name}
Deponent
Date:
Place:""",
            "tags": ["Litigation", "Affidavit", "Evidence"],
            "ai_enhanced": True
        },
        {
            "id": "criminal_complaint_200",
            "name": "Criminal Complaint u/s 200 CrPC",
            "category": "litigation",
            "description": "Private criminal complaint before Magistrate",
            "applicable_for": ["Lawyer", "Individual", "Legal Professional"],
            "fields": [
                {"name": "magistrate_court", "label": "Magistrate Court Name", "type": "text", "required": True},
                {"name": "complainant_name", "label": "Complainant Name", "type": "text", "required": True},
                {"name": "accused_name", "label": "Accused Name", "type": "text", "required": True},
                {"name": "offence_details", "label": "Offence Details", "type": "multiline", "required": True},
                {"name": "sections_invoked", "label": "IPC Sections", "type": "text", "required": True, "placeholder": "e.g., 420, 468, 471 IPC"}
            ],
            "template_text": """BEFORE THE {magistrate_court}

CRIMINAL COMPLAINT u/s 200 CrPC

Complainant: {complainant_name}
Accused: {accused_name}

OFFENCE:
{offence_details}

SECTIONS: {sections_invoked}

[AI expands with ingredients of offence and evidence]

PRAYER:
Take cognizance and issue process against the accused.

Complainant/Advocate
Date:""",
            "tags": ["Litigation", "Criminal", "Complaint", "CrPC"],
            "ai_enhanced": True
        },
        {
            "id": "regular_bail_application",
            "name": "Bail Application (Regular Bail)",
            "category": "litigation",
            "description": "Regular bail application in criminal case",
            "applicable_for": ["Lawyer", "Legal Professional"],
            "fields": [
                {"name": "court_name", "label": "Court Name", "type": "text", "required": True},
                {"name": "applicant_name", "label": "Applicant/Accused Name", "type": "text", "required": True},
                {"name": "fir_number", "label": "FIR Number", "type": "text", "required": True},
                {"name": "police_station", "label": "Police Station", "type": "text", "required": True},
                {"name": "sections", "label": "Sections of Law", "type": "text", "required": True},
                {"name": "grounds_for_bail", "label": "Grounds for Bail", "type": "multiline", "required": True}
            ],
            "template_text": """IN THE {court_name}

BAIL APPLICATION

Applicant: {applicant_name}
FIR No: {fir_number}
Police Station: {police_station}
Sections: {sections}

GROUNDS FOR BAIL:
{grounds_for_bail}

[AI expands with bail jurisprudence, no flight risk, roots in society, etc.]

PRAYER:
Grant regular bail to the applicant.

Applicant/Advocate
Date:""",
            "tags": ["Litigation", "Criminal", "Bail", "CrPC"],
            "ai_enhanced": True
        },
        {
            "id": "anticipatory_bail_438",
            "name": "Anticipatory Bail Application (438 CrPC)",
            "category": "litigation",
            "description": "Application for anticipatory bail",
            "applicable_for": ["Lawyer", "Legal Professional"],
            "fields": [
                {"name": "court_name", "label": "Court Name (Sessions/High Court)", "type": "text", "required": True},
                {"name": "applicant_name", "label": "Applicant Name", "type": "text", "required": True},
                {"name": "apprehension_details", "label": "Apprehension of Arrest Details", "type": "multiline", "required": True},
                {"name": "grounds", "label": "Grounds for Anticipatory Bail", "type": "multiline", "required": True}
            ],
            "template_text": """IN THE {court_name}

ANTICIPATORY BAIL APPLICATION u/s 438 CrPC

Applicant: {applicant_name}

APPREHENSION:
{apprehension_details}

GROUNDS:
{grounds}

[AI expands with legal grounds, custodial interrogation not required, etc.]

PRAYER:
Grant anticipatory bail to the applicant.

Applicant/Advocate
Date:""",
            "tags": ["Litigation", "Anticipatory Bail", "438 CrPC", "Criminal"],
            "ai_enhanced": True
        },
        {
            "id": "compounding_138_ni_act",
            "name": "Compounding Application (138 NI Act)",
            "category": "litigation",
            "description": "Application for compounding of cheque bounce offence",
            "applicable_for": ["Lawyer", "Legal Professional"],
            "fields": [
                {"name": "court_name", "label": "Court Name", "type": "text", "required": True},
                {"name": "case_number", "label": "Case Number", "type": "text", "required": True},
                {"name": "complainant_name", "label": "Complainant Name", "type": "text", "required": True},
                {"name": "accused_name", "label": "Accused Name", "type": "text", "required": True},
                {"name": "settlement_amount", "label": "Settlement Amount (Rs.)", "type": "number", "required": True}
            ],
            "template_text": """IN THE {court_name}

{case_number}

COMPOUNDING APPLICATION u/s 147 NI Act

Complainant: {complainant_name}
Accused: {accused_name}

The parties have settled the matter for Rs. {settlement_amount}.

PRAYER:
Permit compounding and close the case.

Complainant & Accused/Advocates
Date:""",
            "tags": ["Litigation", "Compounding", "138 NI Act", "Cheque Bounce"],
            "ai_enhanced": True
        },
        {
            "id": "memo_of_appeal",
            "name": "Memo of Appeal (Civil/Criminal)",
            "category": "litigation",
            "description": "Memorandum of appeal against lower court order",
            "applicable_for": ["Lawyer", "Legal Professional"],
            "fields": [
                {"name": "appellate_court", "label": "Appellate Court Name", "type": "text", "required": True},
                {"name": "appellant_name", "label": "Appellant Name", "type": "text", "required": True},
                {"name": "respondent_name", "label": "Respondent Name", "type": "text", "required": True},
                {"name": "impugned_order", "label": "Impugned Order Details", "type": "multiline", "required": True},
                {"name": "grounds_of_appeal", "label": "Grounds of Appeal", "type": "multiline", "required": True}
            ],
            "template_text": """IN THE {appellate_court}

MEMORANDUM OF APPEAL

Appellant: {appellant_name}
Respondent: {respondent_name}

IMPUGNED ORDER:
{impugned_order}

GROUNDS OF APPEAL:
{grounds_of_appeal}

[AI expands with legal grounds and substantial questions of law]

PRAYER:
Set aside the impugned order and allow the appeal.

Appellant/Advocate
Date:""",
            "tags": ["Litigation", "Appeal", "Memo", "Appellate"],
            "ai_enhanced": True
        }
    ]
