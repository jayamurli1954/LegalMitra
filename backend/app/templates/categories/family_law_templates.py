"""Family & Personal Law Templates"""

def get_family_law_templates():
    """Returns all family law related templates"""
    return [
        {
            "id": "mutual_divorce_13b",
            "name": "Mutual Divorce Petition (Section 13B HMA)",
            "category": "family_law",
            "description": "Joint petition for mutual consent divorce",
            "applicable_for": ["Lawyer", "Legal Professional"],
            "fields": [
                {"name": "court_name", "label": "Family Court Name", "type": "text", "required": True},
                {"name": "husband_name", "label": "Husband Name", "type": "text", "required": True},
                {"name": "wife_name", "label": "Wife Name", "type": "text", "required": True},
                {"name": "marriage_date", "label": "Date of Marriage", "type": "date", "required": True},
                {"name": "separation_date", "label": "Date of Separation", "type": "date", "required": True},
                {"name": "settlement_terms", "label": "Settlement Terms (Alimony, Custody, etc.)", "type": "multiline", "required": True}
            ],
            "template_text": """IN THE {court_name}

JOINT PETITION FOR DIVORCE u/s 13B HINDU MARRIAGE ACT

Petitioner No.1: {husband_name} (Husband)
Petitioner No.2: {wife_name} (Wife)

Marriage Date: {marriage_date}
Separation Since: {separation_date}

The petitioners have been living separately and mutually consent to dissolve the marriage.

SETTLEMENT TERMS:
{settlement_terms}

[AI expands with legal format and joint affidavit]

PRAYER:
Grant decree of divorce by mutual consent.

Petitioners/Advocates
Date:""",
            "tags": ["Family Law", "Divorce", "Mutual Consent", "13B"],
            "ai_enhanced": True
        },
        {
            "id": "maintenance_125_crpc",
            "name": "Maintenance Application (Section 125 CrPC)",
            "category": "family_law",
            "description": "Application for maintenance under CrPC",
            "applicable_for": ["Lawyer", "Individual", "Legal Professional"],
            "fields": [
                {"name": "magistrate_court", "label": "Magistrate Court Name", "type": "text", "required": True},
                {"name": "applicant_name", "label": "Applicant Name (Wife/Child/Parent)", "type": "text", "required": True},
                {"name": "respondent_name", "label": "Respondent Name (Husband/Son)", "type": "text", "required": True},
                {"name": "monthly_maintenance", "label": "Monthly Maintenance Claimed (Rs.)", "type": "number", "required": True},
                {"name": "grounds", "label": "Grounds for Maintenance", "type": "multiline", "required": True}
            ],
            "template_text": """BEFORE THE {magistrate_court}

MAINTENANCE APPLICATION u/s 125 CrPC

Applicant: {applicant_name}
Respondent: {respondent_name}

CLAIM: Monthly maintenance of Rs. {monthly_maintenance}

GROUNDS:
{grounds}

[AI expands with inability to maintain self, respondent's income, etc.]

PRAYER:
Direct the respondent to pay monthly maintenance.

Applicant/Advocate
Date:""",
            "tags": ["Family Law", "Maintenance", "125 CrPC", "Alimony"],
            "ai_enhanced": True
        },
        {
            "id": "domestic_violence_pwdv",
            "name": "Domestic Violence Complaint (PWDV Act)",
            "category": "family_law",
            "description": "Complaint under Protection of Women from Domestic Violence Act",
            "applicable_for": ["Lawyer", "Women", "Legal Professional"],
            "fields": [
                {"name": "magistrate_court", "label": "Magistrate Court Name", "type": "text", "required": True},
                {"name": "aggrieved_person", "label": "Aggrieved Person Name", "type": "text", "required": True},
                {"name": "respondent_name", "label": "Respondent Name", "type": "text", "required": True},
                {"name": "violence_details", "label": "Details of Domestic Violence", "type": "multiline", "required": True},
                {"name": "relief_sought", "label": "Relief Sought", "type": "multiline", "required": True, "placeholder": "Protection order, Residence order, Maintenance, etc."}
            ],
            "template_text": """BEFORE THE {magistrate_court}

COMPLAINT UNDER PROTECTION OF WOMEN FROM DOMESTIC VIOLENCE ACT, 2005

Aggrieved Person: {aggrieved_person}
Respondent: {respondent_name}

VIOLENCE DETAILS:
{violence_details}

RELIEF SOUGHT:
{relief_sought}

[AI expands with legal provisions and reliefs available]

PRAYER:
Grant protection and other reliefs under PWDV Act.

Aggrieved Person/Advocate
Date:""",
            "tags": ["Family Law", "Domestic Violence", "PWDV Act", "Women Protection"],
            "ai_enhanced": True
        },
        {
            "id": "child_custody_application",
            "name": "Child Custody Application",
            "category": "family_law",
            "description": "Application for child custody in family court",
            "applicable_for": ["Lawyer", "Parent", "Legal Professional"],
            "fields": [
                {"name": "court_name", "label": "Family Court Name", "type": "text", "required": True},
                {"name": "applicant_name", "label": "Applicant/Parent Name", "type": "text", "required": True},
                {"name": "child_name", "label": "Child Name", "type": "text", "required": True},
                {"name": "child_age", "label": "Child Age", "type": "number", "required": True},
                {"name": "grounds_for_custody", "label": "Grounds for Custody", "type": "multiline", "required": True}
            ],
            "template_text": """IN THE {court_name}

APPLICATION FOR CHILD CUSTODY

Applicant/Parent: {applicant_name}
Child: {child_name}, Age: {child_age}

GROUNDS:
{grounds_for_custody}

[AI expands with welfare of child, best interests, etc.]

PRAYER:
Grant custody of the minor child to the applicant.

Applicant/Advocate
Date:""",
            "tags": ["Family Law", "Child Custody", "Guardianship"],
            "ai_enhanced": True
        },
        {
            "id": "restitution_conjugal_rights",
            "name": "Legal Notice for Restitution of Conjugal Rights",
            "category": "family_law",
            "description": "Notice demanding restitution of conjugal rights",
            "applicable_for": ["Lawyer", "Individual"],
            "fields": [
                {"name": "sender_name", "label": "Sender Name (Husband/Wife)", "type": "text", "required": True},
                {"name": "spouse_name", "label": "Spouse Name", "type": "text", "required": True},
                {"name": "marriage_date", "label": "Date of Marriage", "type": "date", "required": True},
                {"name": "desertion_details", "label": "Desertion Details", "type": "multiline", "required": True}
            ],
            "template_text": """LEGAL NOTICE

To: {spouse_name}

From: {sender_name}

Subject: Restitution of Conjugal Rights

We were married on {marriage_date}. Without reasonable excuse, you have withdrawn from my society.

DESERTION:
{desertion_details}

DEMAND:
Resume cohabitation within 15 days, failing which legal proceedings for restitution of conjugal rights will be initiated.

[AI expands with legal basis]

Advocate for {sender_name}
Date:""",
            "tags": ["Family Law", "Conjugal Rights", "Legal Notice", "Matrimonial"],
            "ai_enhanced": True
        },
        {
            "id": "will_hindu_simple",
            "name": "Last Will and Testament (Simple)",
            "category": "family_law",
            "description": "Simple will for property distribution",
            "applicable_for": ["Individual", "Lawyer"],
            "fields": [
                {"name": "testator_name", "label": "Testator Name (Person making will)", "type": "text", "required": True},
                {"name": "testator_address", "label": "Testator Address", "type": "multiline", "required": True},
                {"name": "beneficiaries", "label": "Beneficiaries and Bequests", "type": "multiline", "required": True, "placeholder": "List beneficiaries and what property/assets they inherit"},
                {"name": "executor_name", "label": "Executor Name", "type": "text", "required": True}
            ],
            "template_text": """LAST WILL AND TESTAMENT

I, {testator_name}, residing at {testator_address}, being of sound mind, do hereby make this my Last Will:

1. I revoke all previous wills.

2. BEQUESTS:
{beneficiaries}

3. EXECUTOR:
   I appoint {executor_name} as the Executor of this Will.

[AI expands with legal formalities and attestation clause]

SIGNED by the Testator:

{testator_name}
Date:

WITNESSES:
1. Name:_______ Signature:_______
2. Name:_______ Signature:_______""",
            "tags": ["Family Law", "Will", "Testament", "Estate Planning"],
            "ai_enhanced": True
        },
        {
            "id": "codicil_to_will",
            "name": "Codicil to Will",
            "category": "family_law",
            "description": "Codicil to amend existing will",
            "applicable_for": ["Individual", "Lawyer"],
            "fields": [
                {"name": "testator_name", "label": "Testator Name", "type": "text", "required": True},
                {"name": "original_will_date", "label": "Original Will Date", "type": "date", "required": True},
                {"name": "amendments", "label": "Amendments to be Made", "type": "multiline", "required": True}
            ],
            "template_text": """CODICIL TO WILL

I, {testator_name}, made my Will dated {original_will_date}.

I now make the following amendments:

{amendments}

In all other respects, the original Will remains valid.

[AI expands with proper codicil format]

{testator_name}
Date:

WITNESSES:
1. Name:_______ Signature:_______
2. Name:_______ Signature:_______""",
            "tags": ["Family Law", "Codicil", "Will Amendment"],
            "ai_enhanced": True
        },
        {
            "id": "succession_certificate",
            "name": "Succession Certificate Application",
            "category": "family_law",
            "description": "Application for succession certificate for inheriting assets",
            "applicable_for": ["Lawyer", "Legal Heir"],
            "fields": [
                {"name": "court_name", "label": "District Court Name", "type": "text", "required": True},
                {"name": "applicant_name", "label": "Applicant Name (Legal Heir)", "type": "text", "required": True},
                {"name": "deceased_name", "label": "Deceased Name", "type": "text", "required": True},
                {"name": "death_date", "label": "Date of Death", "type": "date", "required": True},
                {"name": "assets_details", "label": "Details of Assets/Debts", "type": "multiline", "required": True}
            ],
            "template_text": """IN THE {court_name}

PETITION FOR SUCCESSION CERTIFICATE

Applicant: {applicant_name}
Deceased: {deceased_name}
Date of Death: {death_date}

ASSETS:
{assets_details}

[AI expands with list of legal heirs and succession details]

PRAYER:
Grant Succession Certificate to the applicant.

Applicant/Advocate
Date:""",
            "tags": ["Family Law", "Succession Certificate", "Inheritance", "Legal Heir"],
            "ai_enhanced": True
        }
    ]
