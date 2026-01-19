"""Real Estate Templates"""

def get_real_estate_templates():
    """Returns all real estate related templates"""
    return [
        {
            "id": "sale_deed",
            "name": "Property Sale Deed",
            "category": "real_estate",
            "description": "Property sale deed/conveyance deed",
            "applicable_for": ["Legal", "Individual", "Real Estate"],
            "fields": [
                {"name": "seller_name", "label": "Seller Name", "type": "text", "required": True},
                {"name": "buyer_name", "label": "Buyer Name", "type": "text", "required": True},
                {"name": "property_description", "label": "Property Description", "type": "multiline", "required": True},
                {"name": "sale_consideration", "label": "Sale Consideration (Rs.)", "type": "number", "required": True},
                {"name": "property_address", "label": "Property Address", "type": "multiline", "required": True}
            ],
            "template_text": """SALE DEED\nSeller: {seller_name}\nBuyer: {buyer_name}\nProperty: {property_description}\nConsideration: Rs. {sale_consideration}\nAddress: {property_address}\n[AI expands with legal formalities]""",
            "tags": ["Real Estate", "Sale Deed", "Property"],
            "ai_enhanced": True
        },
        {
            "id": "gift_deed",
            "name": "Property Gift Deed",
            "category": "real_estate",
            "description": "Deed for gifting property",
            "applicable_for": ["Legal", "Individual"],
            "fields": [
                {"name": "donor_name", "label": "Donor Name", "type": "text", "required": True},
                {"name": "donee_name", "label": "Donee Name", "type": "text", "required": True},
                {"name": "relationship", "label": "Relationship", "type": "text", "required": True},
                {"name": "property_details", "label": "Property Details", "type": "multiline", "required": True}
            ],
            "template_text": """GIFT DEED\nDonor: {donor_name}\nDonee: {donee_name}\nRelationship: {relationship}\nProperty: {property_details}\n[AI expands]""",
            "tags": ["Real Estate", "Gift Deed"],
            "ai_enhanced": True
        },
        {
            "id": "power_of_attorney_property",
            "name": "Power of Attorney for Property",
            "category": "real_estate",
            "description": "POA for property matters",
            "applicable_for": ["Legal", "Individual"],
            "fields": [
                {"name": "principal_name", "label": "Principal Name", "type": "text", "required": True},
                {"name": "attorney_name", "label": "Attorney Name", "type": "text", "required": True},
                {"name": "property_details", "label": "Property Details", "type": "multiline", "required": True},
                {"name": "powers_granted", "label": "Powers Granted", "type": "multiline", "required": True}
            ],
            "template_text": """POWER OF ATTORNEY\nPrincipal: {principal_name}\nAttorney: {attorney_name}\nProperty: {property_details}\nPowers: {powers_granted}\n[AI expands]""",
            "tags": ["Real Estate", "POA", "Legal"],
            "ai_enhanced": True
        },
        {
            "id": "rent_agreement",
            "name": "Residential Rent Agreement",
            "category": "real_estate",
            "description": "Standard residential rental agreement",
            "applicable_for": ["Individual", "Property Owner"],
            "fields": [
                {"name": "landlord_name", "label": "Landlord Name", "type": "text", "required": True},
                {"name": "tenant_name", "label": "Tenant Name", "type": "text", "required": True},
                {"name": "property_address", "label": "Property Address", "type": "multiline", "required": True},
                {"name": "monthly_rent", "label": "Monthly Rent (Rs.)", "type": "number", "required": True},
                {"name": "security_deposit", "label": "Security Deposit (Rs.)", "type": "number", "required": True},
                {"name": "lease_period", "label": "Lease Period (months)", "type": "number", "required": True}
            ],
            "template_text": """RENT AGREEMENT\nLandlord: {landlord_name}\nTenant: {tenant_name}\nProperty: {property_address}\nRent: Rs. {monthly_rent}/month\nDeposit: Rs. {security_deposit}\nPeriod: {lease_period} months\n[AI expands with terms and conditions]""",
            "tags": ["Real Estate", "Rent", "Lease"],
            "ai_enhanced": True
        },
        {
            "id": "leave_license_agreement",
            "name": "Leave and License Agreement",
            "category": "real_estate",
            "description": "Leave and license agreement for property",
            "applicable_for": ["Individual", "Corporate"],
            "fields": [
                {"name": "licensor_name", "label": "Licensor Name", "type": "text", "required": True},
                {"name": "licensee_name", "label": "Licensee Name", "type": "text", "required": True},
                {"name": "premises_details", "label": "Premises Details", "type": "multiline", "required": True},
                {"name": "monthly_compensation", "label": "Monthly Compensation (Rs.)", "type": "number", "required": True},
                {"name": "tenure", "label": "Tenure (months)", "type": "number", "required": True}
            ],
            "template_text": """LEAVE AND LICENSE AGREEMENT\nLicensor: {licensor_name}\nLicensee: {licensee_name}\nPremises: {premises_details}\nCompensation: Rs. {monthly_compensation}/month\nTenure: {tenure} months\n[AI expands]""",
            "tags": ["Real Estate", "License", "Commercial"],
            "ai_enhanced": True
        },
        {
            "id": "builder_buyer_agreement",
            "name": "Builder-Buyer Agreement",
            "category": "real_estate",
            "description": "Agreement between builder and flat buyer",
            "applicable_for": ["Individual", "Builder", "Legal"],
            "fields": [
                {"name": "builder_name", "label": "Builder/Developer Name", "type": "text", "required": True},
                {"name": "buyer_name", "label": "Buyer Name", "type": "text", "required": True},
                {"name": "project_name", "label": "Project Name", "type": "text", "required": True},
                {"name": "unit_details", "label": "Unit/Flat Details", "type": "multiline", "required": True},
                {"name": "total_price", "label": "Total Price (Rs.)", "type": "number", "required": True},
                {"name": "possession_date", "label": "Expected Possession Date", "type": "date", "required": True}
            ],
            "template_text": """BUILDER-BUYER AGREEMENT\nBuilder: {builder_name}\nBuyer: {buyer_name}\nProject: {project_name}\nUnit: {unit_details}\nPrice: Rs. {total_price}\nPossession: {possession_date}\n[AI expands with RERA compliance]""",
            "tags": ["Real Estate", "Builder", "RERA"],
            "ai_enhanced": True
        },
        {
            "id": "property_mortgage_deed",
            "name": "Property Mortgage Deed",
            "category": "real_estate",
            "description": "Mortgage deed for property as security",
            "applicable_for": ["Banking", "Legal"],
            "fields": [
                {"name": "mortgagor_name", "label": "Mortgagor Name", "type": "text", "required": True},
                {"name": "mortgagee_name", "label": "Mortgagee Name", "type": "text", "required": True},
                {"name": "property_details", "label": "Property Details", "type": "multiline", "required": True},
                {"name": "loan_amount", "label": "Loan Amount (Rs.)", "type": "number", "required": True},
                {"name": "mortgage_purpose", "label": "Purpose of Mortgage", "type": "text", "required": True}
            ],
            "template_text": """MORTGAGE DEED\nMortgagor: {mortgagor_name}\nMortgagee: {mortgagee_name}\nProperty: {property_details}\nLoan: Rs. {loan_amount}\nPurpose: {mortgage_purpose}\n[AI expands]""",
            "tags": ["Real Estate", "Mortgage", "Loan"],
            "ai_enhanced": True
        },
        {
            "id": "khata_transfer_application",
            "name": "Khata Transfer Application",
            "category": "real_estate",
            "description": "Application for property khata transfer",
            "applicable_for": ["Individual", "Property Owner"],
            "fields": [
                {"name": "applicant_name", "label": "Applicant Name", "type": "text", "required": True},
                {"name": "property_number", "label": "Property/Khata Number", "type": "text", "required": True},
                {"name": "previous_owner", "label": "Previous Owner Name", "type": "text", "required": True},
                {"name": "property_address", "label": "Property Address", "type": "multiline", "required": True}
            ],
            "template_text": """KHATA TRANSFER APPLICATION\nApplicant: {applicant_name}\nKhata No: {property_number}\nPrevious Owner: {previous_owner}\nAddress: {property_address}\n[AI expands]""",
            "tags": ["Real Estate", "Khata", "Property Tax"],
            "ai_enhanced": True
        }
    ]
