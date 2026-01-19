"""
Template Service - JSON-Driven Legal Document Templates
Ready-made editable templates for Indian legal workflows
Also loads templates from Python code for backward compatibility
"""

import json
import logging
import re
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
import sys

logger = logging.getLogger(__name__)

# Import Python template functions
try:
    from app.templates.categories.gst_templates import get_gst_templates
    from app.templates.categories.income_tax_templates import get_income_tax_templates
    from app.templates.categories.corporate_templates import get_corporate_templates
    from app.templates.categories.contract_templates import get_contract_templates
    from app.templates.categories.compliance_templates import get_compliance_templates
    from app.templates.categories.legal_notice_templates import get_legal_notice_templates
    from app.templates.categories.banking_templates import get_banking_templates
    from app.templates.categories.real_estate_templates import get_real_estate_templates
    from app.templates.categories.litigation_templates import get_litigation_templates
    from app.templates.categories.family_law_templates import get_family_law_templates
    from app.templates.categories.criminal_law_templates import get_criminal_law_templates
    PYTHON_TEMPLATES_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Python templates not available: {e}")
    PYTHON_TEMPLATES_AVAILABLE = False


class TemplateService:
    """Manages legal document templates"""

    def __init__(self):
        """Initialize template service"""
        self.templates_dir = Path(__file__).parent.parent.parent / "data" / "templates"
        self.templates_cache = {}
        self._load_templates()
        logger.info("Template Service initialized")

    def _load_templates(self):
        """Load all templates from Python code first, then JSON files (Python templates take priority)"""
        json_count = 0
        python_count = 0
        
        # First, load from Python code (authoritative source - 112 templates)
        if PYTHON_TEMPLATES_AVAILABLE:
            try:
                python_templates = []
                python_templates.extend(get_gst_templates())
                python_templates.extend(get_income_tax_templates())
                python_templates.extend(get_corporate_templates())
                python_templates.extend(get_contract_templates())
                python_templates.extend(get_compliance_templates())
                python_templates.extend(get_legal_notice_templates())
                python_templates.extend(get_banking_templates())
                python_templates.extend(get_real_estate_templates())
                python_templates.extend(get_litigation_templates())
                python_templates.extend(get_family_law_templates())
                python_templates.extend(get_criminal_law_templates())

                for template in python_templates:
                    template_id = template.get('id')
                    if template_id:
                        # Convert Python format to JSON format
                        template_data = {
                            'template_id': template_id,
                            'name': template.get('name'),
                            'category': template.get('category'),
                            'description': template.get('description'),
                            'fields': template.get('fields', []),
                            'template_text': template.get('template_text', ''),
                            'tags': template.get('tags', []),
                            'is_premium': template.get('is_premium', False),
                            'court': template.get('court', []),
                            'act': template.get('act', []),
                            'language': template.get('language', 'en'),
                            'applicable_for': template.get('applicable_for', [])
                        }
                        self.templates_cache[template_id] = template_data
                        python_count += 1

            except Exception as e:
                logger.error(f"Failed to load Python templates: {e}")

        # Note: JSON templates are NOT loaded to avoid duplicates
        # Python code is the authoritative source with exactly 112 templates
        # JSON files are legacy/backup only

        logger.info(f"✅ Loaded {python_count} templates from Python code (authoritative source)")

    def get_template(self, template_id: str) -> Optional[Dict]:
        """Get template by ID"""
        return self.templates_cache.get(template_id)

    def list_templates(
        self,
        category: Optional[str] = None,
        court: Optional[str] = None,
        act: Optional[str] = None,
        language: str = "en"
    ) -> List[Dict]:
        """
        List available templates with optional filtering

        Args:
            category: Filter by category (legal_notice, corporate, tax, etc.)
            court: Filter by court type (District, High Court, Supreme Court)
            act: Filter by applicable act (IPC, CrPC, NI Act, etc.)
            language: Filter by language (default: en)

        Returns:
            List of template summaries
        """
        templates = []

        for template_id, template_data in self.templates_cache.items():
            # Apply filters
            if category and template_data.get('category') != category:
                continue

            if court and court not in template_data.get('court', []):
                continue

            if act and act not in template_data.get('act', []):
                continue

            if language and template_data.get('language') != language:
                continue

            # Add summary
            templates.append({
                'template_id': template_id,
                'name': template_data.get('name'),
                'category': template_data.get('category'),
                'description': template_data.get('description'),
                'court': template_data.get('court', []),
                'act': template_data.get('act', []),
                'language': template_data.get('language', 'en'),
                'tags': template_data.get('tags', []),
                'is_premium': template_data.get('is_premium', False)
            })

        return templates

    def render_template(
        self,
        template_id: str,
        fields: Dict[str, Any],
        format: str = "text"
    ) -> Optional[str]:
        """
        Render template with user-provided fields

        Args:
            template_id: Template identifier
            fields: Dictionary of field values
            format: Output format (text, html, markdown)

        Returns:
            Rendered document text
        """
        template = self.get_template(template_id)
        if not template:
            logger.error(f"Template not found: {template_id}")
            return None

        # Validate required fields
        required_fields = [
            field['id'] for field in template.get('fields', [])
            if field.get('required', False)
        ]

        missing_fields = [f for f in required_fields if f not in fields]
        if missing_fields:
            logger.error(f"Missing required fields: {missing_fields}")
            return None

        # Add default values
        enriched_fields = self._add_default_fields(fields)

        # Render body
        body_paragraphs = template.get('body', [])
        rendered_paragraphs = []

        for paragraph in body_paragraphs:
            # Get text (support for both string and dict format)
            if isinstance(paragraph, str):
                text = paragraph
            elif isinstance(paragraph, dict):
                # Check conditional rendering for dict format
                if 'condition' in paragraph:
                    if not self._evaluate_condition(paragraph['condition'], enriched_fields):
                        continue
                text = paragraph.get('text', '')
            else:
                continue

            # Replace placeholders
            rendered_text = self._replace_placeholders(text, enriched_fields)
            rendered_paragraphs.append(rendered_text)

        # Join paragraphs
        if format == "html":
            rendered_body = "\n".join([f"<p>{p}</p>" for p in rendered_paragraphs])
        else:
            rendered_body = "\n\n".join(rendered_paragraphs)

        # Add disclaimer if required
        if template.get('disclaimer', True):
            disclaimer = self._get_disclaimer(template.get('category'))
            rendered_body += f"\n\n{disclaimer}"

        return rendered_body

    def _replace_placeholders(self, text: str, fields: Dict[str, Any]) -> str:
        """Replace {{placeholder}} with actual values"""
        def replacer(match):
            field_name = match.group(1)
            value = fields.get(field_name, f"[{field_name}]")
            return str(value)

        return re.sub(r'\{\{(.*?)\}\}', replacer, text)

    def _evaluate_condition(self, condition: str, fields: Dict[str, Any]) -> bool:
        """Evaluate conditional rendering"""
        try:
            # Simple condition evaluation (e.g., "field_name == 'value'")
            # For safety, only support simple equality checks
            if '==' in condition:
                field, value = condition.split('==')
                field = field.strip()
                value = value.strip().strip('"').strip("'")
                return str(fields.get(field, '')).lower() == value.lower()
            elif 'exists' in condition:
                field = condition.replace('exists', '').strip()
                return field in fields and fields[field]
            return True
        except:
            return True

    def _add_default_fields(self, fields: Dict[str, Any]) -> Dict[str, Any]:
        """Add auto-generated default fields"""
        enriched = fields.copy()

        # Add current date if not provided
        if 'date' not in enriched:
            enriched['date'] = datetime.now().strftime('%d-%m-%Y')

        # Add formatted date variations
        if 'date' in enriched and not isinstance(enriched['date'], str):
            enriched['date'] = enriched['date'].strftime('%d-%m-%Y')

        return enriched

    def _get_disclaimer(self, category: str) -> str:
        """Get appropriate disclaimer based on category"""
        disclaimers = {
            'legal_notice': (
                "⚠️ **Legal Notice Disclaimer**: This is a template notice generated using LegalMitra. "
                "It must be reviewed and finalized by a qualified advocate before sending. "
                "This does not constitute legal advice."
            ),
            'corporate': (
                "⚠️ **Corporate Document Disclaimer**: This is a template document generated using LegalMitra. "
                "It must be reviewed by legal counsel before execution. "
                "Consult a qualified company secretary or advocate for compliance verification."
            ),
            'tax_compliance': (
                "⚠️ **Tax Compliance Disclaimer**: This is a template for tax compliance matters. "
                "Tax laws are complex and fact-specific. This must be reviewed by a qualified "
                "Chartered Accountant or tax advocate before submission."
            ),
            'pleadings': (
                "⚠️ **Court Pleading Disclaimer**: This is a template pleading generated using LegalMitra. "
                "It must be reviewed, verified, and signed by a qualified advocate before filing. "
                "Facts, citations, and legal arguments must be verified."
            ),
            'default': (
                "⚠️ **General Disclaimer**: This document is AI-assisted and generated using LegalMitra. "
                "It must be reviewed by a qualified legal professional before use. "
                "This does not constitute legal advice."
            )
        }

        return disclaimers.get(category, disclaimers['default'])

    def get_template_fields(self, template_id: str) -> Optional[List[Dict]]:
        """Get required fields for a template"""
        template = self.get_template(template_id)
        if not template:
            return None

        return template.get('fields', [])

    def validate_fields(self, template_id: str, fields: Dict[str, Any]) -> Dict:
        """
        Validate user-provided fields against template requirements

        Returns:
            {
                'is_valid': bool,
                'missing_fields': List[str],
                'invalid_fields': List[Dict]
            }
        """
        template = self.get_template(template_id)
        if not template:
            return {
                'is_valid': False,
                'error': 'Template not found'
            }

        template_fields = template.get('fields', [])
        missing_fields = []
        invalid_fields = []

        for field_def in template_fields:
            field_id = field_def['id']
            field_value = fields.get(field_id)

            # Check required
            if field_def.get('required', False) and not field_value:
                missing_fields.append(field_id)
                continue

            # Check type
            field_type = field_def.get('type', 'text')
            if field_value and not self._validate_field_type(field_value, field_type):
                invalid_fields.append({
                    'field': field_id,
                    'expected_type': field_type,
                    'error': f"Invalid {field_type} format"
                })

        return {
            'is_valid': len(missing_fields) == 0 and len(invalid_fields) == 0,
            'missing_fields': missing_fields,
            'invalid_fields': invalid_fields
        }

    def _validate_field_type(self, value: Any, field_type: str) -> bool:
        """Validate field value against expected type"""
        if field_type == 'email':
            return re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', str(value)) is not None
        elif field_type == 'phone':
            return re.match(r'^[0-9]{10}$', str(value).replace('+91', '').replace('-', '').replace(' ', '')) is not None
        elif field_type == 'number':
            try:
                float(value)
                return True
            except:
                return False
        elif field_type == 'date':
            # Accept various date formats
            return isinstance(value, (str, datetime))
        else:
            return True

    def get_categories(self) -> List[Dict]:
        """Get all template categories"""
        categories = {}

        for template in self.templates_cache.values():
            category = template.get('category', 'Uncategorized')
            if category not in categories:
                categories[category] = {
                    'name': category,
                    'count': 0,
                    'templates': []
                }

            categories[category]['count'] += 1
            categories[category]['templates'].append(template.get('template_id'))

        return list(categories.values())


# Singleton instance
template_service = TemplateService()
