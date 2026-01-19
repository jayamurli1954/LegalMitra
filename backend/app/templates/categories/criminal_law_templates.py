"""Criminal Law Templates"""

def get_criminal_law_templates():
    """Returns all criminal law related templates"""
    return [
        {
            "id": "fir_draft_complaint",
            "name": "FIR Draft (Police Complaint)",
            "category": "criminal_law",
            "description": "Draft format for First Information Report to police",
            "applicable_for": ["Lawyer", "Individual", "Legal Professional"],
            "fields": [
                {
                    "name": "police_station",
                    "label": "Police Station Name",
                    "type": "text",
                    "required": True
                },
                {
                    "name": "complainant_name",
                    "label": "Complainant Name",
                    "type": "text",
                    "required": True
                },
                {
                    "name": "complainant_address",
                    "label": "Complainant Address",
                    "type": "multiline",
                    "required": True
                },
                {
                    "name": "accused_details",
                    "label": "Accused Details (if known)",
                    "type": "multiline",
                    "required": False,
                    "placeholder": "Name, address, description"
                },
                {
                    "name": "incident_date",
                    "label": "Date of Incident",
                    "type": "date",
                    "required": True
                },
                {
                    "name": "incident_time",
                    "label": "Time of Incident",
                    "type": "text",
                    "required": True,
                    "placeholder": "e.g., 10:30 PM"
                },
                {
                    "name": "incident_place",
                    "label": "Place of Incident",
                    "type": "multiline",
                    "required": True
                },
                {
                    "name": "incident_details",
                    "label": "Detailed Description of Incident",
                    "type": "multiline",
                    "required": True,
                    "placeholder": "Detailed narration of the incident, what happened, witnesses, etc."
                }
            ],
            "template_text": """To,
The Station House Officer (SHO)
{police_station}

Subject: First Information Report (FIR)

Respected Sir/Madam,

I, {complainant_name}, residing at {complainant_address}, hereby lodge a complaint regarding the following incident:

INCIDENT DETAILS:
Date of Incident: {incident_date}
Time of Incident: {incident_time}
Place of Incident: {incident_place}

ACCUSED DETAILS:
{accused_details}

DETAILED NARRATION:
{incident_details}

[AI expands with cognizable offense details, applicable sections IPC/BNS, witness information]

I request you to kindly register my complaint and take necessary legal action against the accused.

I am ready to cooperate with the investigation and provide any further information as required.

Complainant
Name: {complainant_name}
Signature:
Date:""",
            "tags": ["Criminal Law", "FIR", "Police Complaint", "Cognizable Offense"],
            "ai_enhanced": True
        },
        {
            "id": "private_criminal_complaint",
            "name": "Private Criminal Complaint Format",
            "category": "criminal_law",
            "description": "Private complaint before Magistrate under Section 200 CrPC",
            "applicable_for": ["Lawyer", "Legal Professional"],
            "fields": [
                {
                    "name": "magistrate_court",
                    "label": "Magistrate Court Name",
                    "type": "text",
                    "required": True
                },
                {
                    "name": "complainant_name",
                    "label": "Complainant Name",
                    "type": "text",
                    "required": True
                },
                {
                    "name": "accused_name",
                    "label": "Accused Name",
                    "type": "text",
                    "required": True
                },
                {
                    "name": "accused_address",
                    "label": "Accused Address",
                    "type": "multiline",
                    "required": True
                },
                {
                    "name": "offense_details",
                    "label": "Offense Details",
                    "type": "multiline",
                    "required": True,
                    "placeholder": "Detailed facts of the offense committed"
                },
                {
                    "name": "sections_invoked",
                    "label": "IPC/BNS Sections Invoked",
                    "type": "text",
                    "required": True,
                    "placeholder": "e.g., Section 420, 406 IPC"
                }
            ],
            "template_text": """BEFORE THE {magistrate_court}

CRIMINAL COMPLAINT u/s 200 CrPC

Complainant: {complainant_name}
         Vs.
Accused: {accused_name}
Address: {accused_address}

COMPLAINT

The Complainant most respectfully submits as under:

1. That the complainant is a law-abiding citizen and is filing this complaint against the accused for offenses punishable under {sections_invoked}.

2. FACTS OF THE CASE:
{offense_details}

3. That the acts of the accused constitute offenses punishable under {sections_invoked}.

[AI expands with detailed allegations, evidence, witnesses, and legal grounds]

PRAYER:
(a) Issue process against the accused
(b) Summon and try the accused for offenses under {sections_invoked}
(c) Grant any other relief as deemed fit

VERIFICATION:
I, {complainant_name}, verify that the contents of this complaint are true to my knowledge and belief.

Complainant/Advocate
Date:
Place:""",
            "tags": ["Criminal Law", "Private Complaint", "Section 200 CrPC", "Magistrate"],
            "ai_enhanced": True
        },
        {
            "id": "compromise_deed_criminal",
            "name": "Compromise Deed (Criminal Matters)",
            "category": "criminal_law",
            "description": "Compromise deed for compoundable criminal offenses",
            "applicable_for": ["Lawyer", "Legal Professional"],
            "fields": [
                {
                    "name": "complainant_name",
                    "label": "Complainant/Victim Name",
                    "type": "text",
                    "required": True
                },
                {
                    "name": "accused_name",
                    "label": "Accused Name",
                    "type": "text",
                    "required": True
                },
                {
                    "name": "case_number",
                    "label": "Case Number",
                    "type": "text",
                    "required": True,
                    "placeholder": "CC No. 123/2024"
                },
                {
                    "name": "court_name",
                    "label": "Court Name",
                    "type": "text",
                    "required": True
                },
                {
                    "name": "offense_details",
                    "label": "Brief Offense Details",
                    "type": "multiline",
                    "required": True
                },
                {
                    "name": "settlement_terms",
                    "label": "Settlement/Compromise Terms",
                    "type": "multiline",
                    "required": True,
                    "placeholder": "Amount paid, apology given, conditions agreed, etc."
                }
            ],
            "template_text": """COMPROMISE DEED

This Deed of Compromise is executed on this [DATE] between:

PARTY OF THE FIRST PART (Complainant):
{complainant_name}

PARTY OF THE SECOND PART (Accused):
{accused_name}

WHEREAS a criminal case bearing {case_number} is pending in {court_name} against the Accused.

WHEREAS the offense relates to: {offense_details}

WHEREAS both parties have mutually agreed to settle the dispute on the following terms:

SETTLEMENT TERMS:
{settlement_terms}

NOW THEREFORE, both parties agree as follows:

1. That the complainant has no objection to the compounding of the offense and withdrawal of the complaint.

2. That the dispute between the parties stands fully and finally settled.

3. That neither party shall make any claims against the other in future regarding this matter.

[AI expands with legal formalities, affidavit format, and court application]

PARTY OF THE FIRST PART          PARTY OF THE SECOND PART
(Complainant)                    (Accused)

Witnesses:
1. Name: _______ Signature: _______
2. Name: _______ Signature: _______

Date:
Place:""",
            "tags": ["Criminal Law", "Compromise", "Compounding", "Settlement", "Mutual Consent"],
            "ai_enhanced": True
        },
        {
            "id": "quashing_fir_482_crpc",
            "name": "Application for Quashing FIR (482 CrPC)",
            "category": "criminal_law",
            "description": "Application to High Court for quashing FIR under Section 482 CrPC",
            "applicable_for": ["Lawyer", "Legal Professional"],
            "fields": [
                {
                    "name": "high_court_name",
                    "label": "High Court Name",
                    "type": "text",
                    "required": True,
                    "placeholder": "e.g., Delhi High Court"
                },
                {
                    "name": "petitioner_name",
                    "label": "Petitioner Name (Accused)",
                    "type": "text",
                    "required": True
                },
                {
                    "name": "respondent_name",
                    "label": "Respondent Name (State/Complainant)",
                    "type": "text",
                    "required": True
                },
                {
                    "name": "fir_number",
                    "label": "FIR Number",
                    "type": "text",
                    "required": True,
                    "placeholder": "FIR No. 123/2024"
                },
                {
                    "name": "police_station",
                    "label": "Police Station",
                    "type": "text",
                    "required": True
                },
                {
                    "name": "sections_invoked",
                    "label": "Sections Invoked in FIR",
                    "type": "text",
                    "required": True
                },
                {
                    "name": "grounds_for_quashing",
                    "label": "Grounds for Quashing",
                    "type": "multiline",
                    "required": True,
                    "placeholder": "No cognizable offense, abuse of process, settlement reached, malicious prosecution, etc."
                }
            ],
            "template_text": """IN THE {high_court_name}

CRIMINAL MISCELLANEOUS PETITION u/s 482 CrPC

Petitioner: {petitioner_name}
    Vs.
Respondent: {respondent_name}

PETITION FOR QUASHING OF FIR

The Petitioner most humbly submits as under:

1. That the present petition is filed under Section 482 of the Code of Criminal Procedure, 1973 for quashing of {fir_number} registered at {police_station} under {sections_invoked}.

2. BRIEF FACTS:
[Facts leading to registration of FIR]

3. GROUNDS FOR QUASHING:
{grounds_for_quashing}

4. That the FIR does not disclose commission of any cognizable offense.

5. That continuation of criminal proceedings would be an abuse of the process of law.

[AI expands with legal precedents, inherent powers u/s 482, Supreme Court judgments]

PRAYER:
(a) Quash the {fir_number}
(b) Stay all proceedings during pendency
(c) Grant any other relief

This petition is filed within limitation and is supported by an affidavit.

Petitioner/Advocate
Date:
Place:""",
            "tags": ["Criminal Law", "Quashing", "482 CrPC", "High Court", "FIR"],
            "ai_enhanced": True
        },
        {
            "id": "protest_petition",
            "name": "Protest Petition",
            "category": "criminal_law",
            "description": "Protest petition when police files closure report",
            "applicable_for": ["Lawyer", "Legal Professional"],
            "fields": [
                {
                    "name": "magistrate_court",
                    "label": "Magistrate Court Name",
                    "type": "text",
                    "required": True
                },
                {
                    "name": "protestor_name",
                    "label": "Protestor/Complainant Name",
                    "type": "text",
                    "required": True
                },
                {
                    "name": "fir_number",
                    "label": "FIR Number",
                    "type": "text",
                    "required": True
                },
                {
                    "name": "closure_report_date",
                    "label": "Date of Closure Report",
                    "type": "date",
                    "required": True
                },
                {
                    "name": "grounds_for_protest",
                    "label": "Grounds for Protest",
                    "type": "multiline",
                    "required": True,
                    "placeholder": "Why closure report is wrong, evidence ignored, inadequate investigation, etc."
                }
            ],
            "template_text": """BEFORE THE {magistrate_court}

PROTEST PETITION AGAINST CLOSURE REPORT

FIR No: {fir_number}

Protestor: {protestor_name}

MOST RESPECTFULLY SUBMITTED:

1. That a closure report u/s 173(2) CrPC has been filed by the police on {closure_report_date} in the above FIR.

2. That the protestor is aggrieved by the said closure report on the following grounds:

GROUNDS FOR PROTEST:
{grounds_for_protest}

3. That the investigation has been conducted in a perfunctory and casual manner.

4. That there is sufficient evidence to proceed against the accused.

5. That the closure report is contrary to law and evidence on record.

[AI expands with legal provisions, investigation deficiencies, and evidence analysis]

PRAYER:
(a) Reject the closure report
(b) Direct further investigation u/s 156(3) CrPC
(c) Issue process against the accused
(d) Grant any other relief

VERIFICATION:
I, {protestor_name}, verify that the contents are true to my knowledge.

Protestor/Advocate
Date:
Place:""",
            "tags": ["Criminal Law", "Protest Petition", "Closure Report", "173 CrPC"],
            "ai_enhanced": True
        },
        {
            "id": "victim_compensation_application",
            "name": "Victim Compensation Application",
            "category": "criminal_law",
            "description": "Application for victim compensation under Section 357A CrPC",
            "applicable_for": ["Lawyer", "Victim", "Legal Professional"],
            "fields": [
                {
                    "name": "court_name",
                    "label": "Court Name/Legal Services Authority",
                    "type": "text",
                    "required": True,
                    "placeholder": "District Legal Services Authority/Court"
                },
                {
                    "name": "victim_name",
                    "label": "Victim/Applicant Name",
                    "type": "text",
                    "required": True
                },
                {
                    "name": "victim_address",
                    "label": "Victim Address",
                    "type": "multiline",
                    "required": True
                },
                {
                    "name": "crime_details",
                    "label": "Details of Crime Suffered",
                    "type": "multiline",
                    "required": True,
                    "placeholder": "Type of crime, injuries, losses suffered"
                },
                {
                    "name": "fir_case_number",
                    "label": "FIR/Case Number",
                    "type": "text",
                    "required": True
                },
                {
                    "name": "financial_loss",
                    "label": "Financial Loss/Medical Expenses (Rs.)",
                    "type": "number",
                    "required": True
                },
                {
                    "name": "compensation_claimed",
                    "label": "Compensation Amount Claimed (Rs.)",
                    "type": "number",
                    "required": True
                }
            ],
            "template_text": """BEFORE THE {court_name}

APPLICATION FOR VICTIM COMPENSATION u/s 357A CrPC

Applicant/Victim: {victim_name}
Address: {victim_address}

MOST RESPECTFULLY SUBMITTED:

1. That the applicant is a victim of crime in {fir_case_number}.

2. DETAILS OF CRIME:
{crime_details}

3. LOSSES SUFFERED:
Financial Loss/Medical Expenses: Rs. {financial_loss}
Physical/Mental trauma: [To be specified]

4. That the applicant is entitled to compensation from the State Victim Compensation Fund as per the Victim Compensation Scheme.

5. COMPENSATION CLAIMED: Rs. {compensation_claimed}

[AI expands with medical certificates, income proof, State compensation scheme rates]

PRAYER:
Grant victim compensation of Rs. {compensation_claimed} to the applicant from the Victim Compensation Fund.

DOCUMENTS ATTACHED:
1. Copy of FIR
2. Medical certificates
3. Income proof/Financial documents
4. Photographs of injuries (if any)

VERIFICATION:
I, {victim_name}, verify that the above statements are true to my knowledge.

Applicant/Advocate
Date:
Place:""",
            "tags": ["Criminal Law", "Victim Compensation", "357A CrPC", "Legal Services"],
            "ai_enhanced": True
        }
    ]
