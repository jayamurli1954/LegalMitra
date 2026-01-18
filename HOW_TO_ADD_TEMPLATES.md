# How to Add More Templates - Step-by-Step Guide

## Quick Start

**File to Edit**: `backend/app/templates/template_service.py`

**Location**: Lines 102-1000+ (the `_get_default_templates()` method)

---

## Step-by-Step Process

### **Step 1: Open the Template Service File**

```bash
# Navigate to the file
backend/app/templates/template_service.py
```

### **Step 2: Find the Template List**

Look for the `_get_default_templates()` method around line 102:

```python
def _get_default_templates(self) -> List[Dict]:
    """Get comprehensive CA/Corporate template library"""
    return [
        # Templates are here
        {...},  # Template 1
        {...},  # Template 2
        # Add new templates here!
    ]
```

### **Step 3: Add Your New Template**

Add a new dictionary to the list. Here's the template structure:

```python
{
    "id": "unique_template_id",              # Must be unique!
    "name": "Display Name for Template",      # User sees this
    "category": "gst",                        # Category (see list below)
    "description": "What this template does", # Brief description
    "applicable_for": ["CA", "Corporate"],    # Who can use it
    "fields": [                               # Input fields
        {
            "name": "field_name",             # Variable name
            "label": "Field Label",           # Label user sees
            "type": "text",                   # Field type
            "required": True,                 # Is it required?
            "placeholder": "Example value"    # Hint for user
        }
    ],
    "template_text": """
        Your template content here.
        Use {field_name} for variables.
    """,
    "tags": ["Tag1", "Tag2"],                 # Search tags
    "ai_enhanced": True                       # Use AI to improve?
}
```

### **Step 4: Restart Backend Server**

```bash
cd backend
python -m uvicorn app.main:app --port 8888 --reload
```

### **Step 5: Test Your Template**

1. Go to http://localhost:3005
2. Click "Document Templates"
3. Find your category
4. See your new template!

---

## Template Structure Explained

### **Required Fields**

| Field | Type | Purpose | Example |
|-------|------|---------|---------|
| `id` | String | Unique identifier | `"gst_appeal_letter"` |
| `name` | String | Display name | `"GST Appeal Letter"` |
| `category` | String | Category key | `"gst"` |
| `description` | String | What it does | `"Appeal against GST order"` |
| `applicable_for` | List | User types | `["CA", "Tax Professional"]` |
| `fields` | List | Input fields | See field structure below |
| `template_text` | String | Template content | Document text with {placeholders} |
| `tags` | List | Search keywords | `["GST", "Appeal", "Tax"]` |
| `ai_enhanced` | Boolean | Use AI? | `True` or `False` |

### **Field Structure**

Each field in the `fields` list:

```python
{
    "name": "taxpayer_name",           # Variable name (no spaces!)
    "label": "Taxpayer Name",          # Label shown to user
    "type": "text",                    # Field type (see types below)
    "required": True,                  # Is this field required?
    "placeholder": "ABC Company Ltd",  # Example/hint
    "help_text": "Enter legal name",   # Optional help text
    "options": ["Option A", "Option B"] # Only for dropdown type
}
```

### **Field Types**

| Type | Purpose | Example |
|------|---------|---------|
| `text` | Single line text | Name, PAN, GSTIN |
| `number` | Numeric input | Amount, Year |
| `date` | Date picker | Filing date, Deadline |
| `dropdown` | Select from options | State, Category, Type |
| `multiline` | Multi-line text | Address, Description |

### **Categories Available**

| Category Key | Display Name |
|--------------|--------------|
| `gst` | GST Templates |
| `income_tax` | Income Tax Templates |
| `corporate` | Corporate Templates |
| `sebi_regulatory` | SEBI & Regulatory |
| `contracts` | Business Contracts |
| `compliance` | Compliance & Certifications |
| `legal_notices` | Legal Notices |

---

## Example: Adding a New GST Template

### **Template: GST Notice Reply**

```python
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
        },
        {
            "name": "officer_name",
            "label": "Designated Officer Name",
            "type": "text",
            "required": False,
            "placeholder": "Name of GST Officer"
        }
    ],
    "template_text": """To,
{officer_name}
[Designation]
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
}
```

---

## Example: Adding an Income Tax Template

### **Template: TDS Return Filing Letter**

```python
{
    "id": "tds_return_filing_letter",
    "name": "TDS Return Filing Covering Letter",
    "category": "income_tax",
    "description": "Covering letter for TDS return filing (Form 24Q, 26Q, 27Q)",
    "applicable_for": ["CA", "Tax Professional", "Corporate"],
    "fields": [
        {
            "name": "company_name",
            "label": "Company/Deductor Name",
            "type": "text",
            "required": True
        },
        {
            "name": "tan",
            "label": "TAN",
            "type": "text",
            "required": True,
            "placeholder": "ABCD12345E"
        },
        {
            "name": "form_type",
            "label": "TDS Return Form",
            "type": "dropdown",
            "required": True,
            "options": [
                "Form 24Q (Salary TDS)",
                "Form 26Q (Non-Salary TDS)",
                "Form 27Q (TDS on NRI)",
                "Form 27EQ (TCS Return)"
            ]
        },
        {
            "name": "quarter",
            "label": "Quarter",
            "type": "dropdown",
            "required": True,
            "options": [
                "Q1 (Apr-Jun)",
                "Q2 (Jul-Sep)",
                "Q3 (Oct-Dec)",
                "Q4 (Jan-Mar)"
            ]
        },
        {
            "name": "financial_year",
            "label": "Financial Year",
            "type": "text",
            "required": True,
            "placeholder": "2024-25"
        },
        {
            "name": "total_tax_deducted",
            "label": "Total Tax Deducted (Rs.)",
            "type": "number",
            "required": True
        },
        {
            "name": "total_tax_deposited",
            "label": "Total Tax Deposited (Rs.)",
            "type": "number",
            "required": True
        }
    ],
    "template_text": """To,
The Assessing Officer,
Income Tax Department,
[Ward/Circle]

Date: [DATE]

Subject: Filing of {form_type} for {quarter} of FY {financial_year}

Ref: TAN - {tan}

Respected Sir/Madam,

We, {company_name} (TAN: {tan}), hereby submit the {form_type} for the quarter {quarter} of the Financial Year {financial_year}.

DETAILS OF TDS RETURN:
- Form Type: {form_type}
- Quarter: {quarter}
- Financial Year: {financial_year}
- Total Tax Deducted: Rs. {total_tax_deducted}
- Total Tax Deposited: Rs. {total_tax_deposited}
- Filing Date: [DATE]

The return has been filed electronically and the acknowledgment is enclosed herewith.

All taxes deducted have been deposited within the prescribed time limits and Form 16/16A have been issued to all deductees.

Kindly process the return and update the TDS credit in the respective deductees' Form 26AS.

Thanking you,

For {company_name}
TAN: {tan}

Authorized Signatory
Name:
Designation:
Place:

Enclosures:
1. TDS Return Acknowledgment
2. Challan Copies
3. Form 27A (if applicable)""",
    "tags": ["TDS", "Income Tax", "Return", "Form 24Q", "Form 26Q"],
    "ai_enhanced": True
}
```

---

## Where to Add Templates in the File

Open `backend/app/templates/template_service.py` and find:

```python
def _get_default_templates(self) -> List[Dict]:
    """Get comprehensive CA/Corporate template library"""
    return [
        # ==================== GST TEMPLATES ====================
        {...},  # Existing template 1
        {...},  # Existing template 2
        # ADD NEW GST TEMPLATES HERE 👇

        # ==================== INCOME TAX TEMPLATES ====================
        {...},  # Existing template 1
        {...},  # Existing template 2
        # ADD NEW INCOME TAX TEMPLATES HERE 👇

        # ... and so on for each category
    ]
```

---

## Tips for Writing Good Templates

### **1. Use Clear Field Names**
```python
# Good
"name": "taxpayer_pan_number"

# Bad
"name": "pan"  # Too vague
```

### **2. Provide Helpful Placeholders**
```python
# Good
"placeholder": "29AAAAA0000A1Z5"  # Shows format

# Bad
"placeholder": "Enter GSTIN"  # Doesn't help
```

### **3. Use AI Enhancement Wisely**
```python
template_text = """
... standard text ...

[AI will expand this section based on {field_name}]

... more text ...
"""
```

### **4. Add Comprehensive Tags**
```python
# Good
"tags": ["GST", "Appeal", "Tax", "Litigation", "Department"]

# Bad
"tags": ["GST"]  # Too few, hard to search
```

### **5. Structure Template Text Well**
```python
template_text = """
HEADING IN CAPS
Proper spacing

1. Numbered points
2. Are easier to read

Clear sections:
- Point 1
- Point 2

{field_placeholders} should be clear
"""
```

---

## Common Template Patterns

### **Pattern 1: Application Letter**
```
To: [Authority]
Subject: Application for [Purpose]

Content with {fields}

Prayer/Request section

Signature block
Enclosures
```

### **Pattern 2: Reply to Notice**
```
To: [Officer]
Ref: [Notice Number]

Reply to each point
Legal arguments
Case laws if applicable

Prayer for relief

Signature
Enclosures
```

### **Pattern 3: Certificate/Report**
```
CERTIFICATE/REPORT HEADING

Details in structured format:
1. Item 1: {field1}
2. Item 2: {field2}

Certification statement

Authorized signatory details
Date, Place, Seal
```

---

## Testing Your New Template

### **Step 1: Add Template to Code**
Edit `template_service.py` and add your template dict.

### **Step 2: Restart Backend**
```bash
cd backend
python -m uvicorn app.main:app --port 8888 --reload
```

### **Step 3: Check API**
```bash
curl http://localhost:8888/api/v1/templates/summary
# Should show increased count

curl http://localhost:8888/api/v1/templates/category/gst
# Should show your new template in the list
```

### **Step 4: Test in UI**
1. Open http://localhost:3005
2. Click "Document Templates"
3. Select your category
4. Find your new template
5. Fill in fields
6. Click "Generate"
7. Verify output looks correct

---

## Bulk Adding Templates

Want to add 10-20 templates at once? I can help!

### **Option 1: I Create Them for You**
Tell me:
- Category (GST, Income Tax, etc.)
- Template types you need
- I'll write the complete code

### **Option 2: Use Template Generator Script**
I can create a Python script that generates template dictionaries from simpler input.

### **Option 3: Import from JSON**
Create templates in JSON format and import them.

---

## Need Help?

### **I Can Create Templates For**:
- ✅ GST (Returns, Refunds, Appeals, Notices)
- ✅ Income Tax (Audits, TDS, Returns, Appeals)
- ✅ Corporate (Board Resolutions, ROC Filings, Agreements)
- ✅ Contracts (Employment, Service, Partnership, NDA)
- ✅ Compliance (PF, ESI, Labor, Environmental)
- ✅ Legal Notices (Demand, Cease & Desist, Termination)
- ✅ Banking (Loan Apps, Guarantees, Credit Facilities)
- ✅ Real Estate (Sale Deed, Lease, Conveyance)
- ✅ And more!

**Just tell me**:
1. Which category?
2. What specific templates?
3. How many do you want?

I'll write the complete code ready to paste!

---

## Summary

✅ **File to Edit**: `backend/app/templates/template_service.py`
✅ **Add templates**: To the `_get_default_templates()` method
✅ **Restart backend**: To see changes
✅ **Test**: UI and API both work automatically
✅ **Get Help**: Tell me what templates you need!

---

**Ready to expand your library? Tell me what templates you want and I'll create them!**
