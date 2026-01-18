"""
Legal Templates V2 API - JSON-Driven Document Templates & Section Validation
Phase 1: Template Library + Section Validator + Audit Logging
Phase 2: PDF Generator + Marketplace UI
"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from io import BytesIO

from app.services.template_service import template_service
from app.services.section_validator import section_validator
from app.services.audit_logger import audit_logger
from app.services.pdf_generator import pdf_generator

router = APIRouter()


class TemplateRenderRequest(BaseModel):
    """Request to render a template"""
    template_id: str
    fields: Dict[str, Any]
    format: str = "text"  # text, html, markdown


class TemplateRenderResponse(BaseModel):
    """Response from template rendering"""
    template_id: str
    rendered_document: str
    validation: Optional[Dict] = None
    document_hash: str


class ValidationRequest(BaseModel):
    """Request to validate section citations"""
    text: str


class ValidationResponse(BaseModel):
    """Response from section validation"""
    is_valid: bool
    total_citations: int
    valid_citations: int
    invalid_citations: List[Dict]
    accuracy_score: float
    details: List[Dict]
    foreign_law_check: Dict
    risky_language_check: Dict


@router.get("/v2/templates")
async def list_templates_v2(
    category: Optional[str] = None,
    court: Optional[str] = None,
    act: Optional[str] = None,
    language: str = "en"
):
    """
    List available templates with optional filtering

    Query Parameters:
    - category: Filter by category (legal_notice, corporate, tax_compliance, pleadings)
    - court: Filter by court type (District, High Court, Supreme Court)
    - act: Filter by applicable act (IPC, CrPC, NI_ACT, GST_ACT, etc.)
    - language: Filter by language (default: en)
    """
    try:
        templates = template_service.list_templates(
            category=category,
            court=court,
            act=act,
            language=language
        )

        return {
            "total": len(templates),
            "filters": {
                "category": category,
                "court": court,
                "act": act,
                "language": language
            },
            "templates": templates
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/v2/templates/categories")
async def get_template_categories_v2():
    """Get all available template categories"""
    try:
        categories = template_service.get_categories()

        return {
            "total_categories": len(categories),
            "categories": categories
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/v2/templates/{template_id}")
async def get_template_v2(template_id: str):
    """Get full template details including fields"""
    try:
        template = template_service.get_template(template_id)

        if not template:
            raise HTTPException(status_code=404, detail="Template not found")

        return template

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/v2/templates/{template_id}/fields")
async def get_template_fields_v2(template_id: str):
    """Get required fields for a template"""
    try:
        fields = template_service.get_template_fields(template_id)

        if fields is None:
            raise HTTPException(status_code=404, detail="Template not found")

        return {
            "template_id": template_id,
            "fields": fields
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/v2/templates/render", response_model=TemplateRenderResponse)
async def render_template_v2(request: TemplateRenderRequest):
    """
    Render a template with user-provided fields

    Features:
    - Validates required fields
    - Replaces placeholders with actual values
    - Adds appropriate disclaimers
    - Validates section citations
    - Returns document hash for audit trail
    """
    try:
        # Validate fields
        validation = template_service.validate_fields(
            request.template_id,
            request.fields
        )

        if not validation['is_valid']:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "Invalid fields",
                    "missing_fields": validation.get('missing_fields', []),
                    "invalid_fields": validation.get('invalid_fields', [])
                }
            )

        # Render template
        rendered_doc = template_service.render_template(
            request.template_id,
            request.fields,
            request.format
        )

        if not rendered_doc:
            raise HTTPException(status_code=500, detail="Failed to render template")

        # Validate citations in rendered document
        citation_validation = section_validator.validate_text(rendered_doc)

        # Check for foreign law and risky language
        foreign_law_check = section_validator.check_foreign_law(rendered_doc)
        risky_language_check = section_validator.check_risky_language(rendered_doc)

        # Create document hash
        doc_hash = audit_logger.hash_text(rendered_doc)

        # Log template usage
        await audit_logger.log_template_usage(
            template_id=request.template_id,
            template_name=template_service.get_template(request.template_id).get('name'),
            category=template_service.get_template(request.template_id).get('category'),
            fields=request.fields,
            generated_doc_hash=doc_hash
        )

        # Log validation
        if citation_validation['total_citations'] > 0:
            await audit_logger.log_validation(
                source_type="template",
                source_id=request.template_id,
                validation_results={
                    **citation_validation,
                    'has_foreign_law': foreign_law_check['has_foreign_law'],
                    'has_risky_language': risky_language_check['has_risky_language']
                }
            )

        return TemplateRenderResponse(
            template_id=request.template_id,
            rendered_document=rendered_doc,
            validation={
                "citations": citation_validation,
                "foreign_law": foreign_law_check,
                "risky_language": risky_language_check
            },
            document_hash=doc_hash
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/validate/citations", response_model=ValidationResponse)
async def validate_citations(request: ValidationRequest):
    """
    Validate section citations in legal text

    Features:
    - Extracts all section citations
    - Validates against Indian Bare Acts registry
    - Checks for foreign law references
    - Checks for risky legal language
    - Returns accuracy score
    """
    try:
        # Validate citations
        validation = section_validator.validate_text(request.text)

        # Check for foreign law
        foreign_law_check = section_validator.check_foreign_law(request.text)

        # Check for risky language
        risky_language_check = section_validator.check_risky_language(request.text)

        # Log validation
        await audit_logger.log_validation(
            source_type="user_text",
            source_id="",
            validation_results={
                **validation,
                'has_foreign_law': foreign_law_check['has_foreign_law'],
                'has_risky_language': risky_language_check['has_risky_language']
            }
        )

        return ValidationResponse(
            is_valid=validation['is_valid'],
            total_citations=validation['total_citations'],
            valid_citations=validation['valid_citations'],
            invalid_citations=validation['invalid_citations'],
            accuracy_score=validation['accuracy_score'],
            details=validation['details'],
            foreign_law_check=foreign_law_check,
            risky_language_check=risky_language_check
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/bare-acts")
async def list_bare_acts():
    """List all available bare acts in the registry"""
    try:
        acts = section_validator.list_available_acts()

        return {
            "total_acts": len(acts),
            "acts": acts
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/bare-acts/{act_code}")
async def get_act_info(act_code: str):
    """Get information about a specific act"""
    try:
        act_info = section_validator.get_act_info(act_code.upper())

        if not act_info:
            raise HTTPException(status_code=404, detail="Act not found")

        return act_info

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/v2/templates/render-pdf")
async def render_template_as_pdf(request: TemplateRenderRequest, court_type: str = "District"):
    """
    Render template and generate court-format PDF

    Features:
    - Proper court margins (1.5" left for binding)
    - A4 page size
    - Times New Roman font
    - Page numbers
    - e-Courts compatible
    - Download as PDF file

    Query Parameters:
    - court_type: District / High Court / Supreme Court (affects line spacing)
    """
    try:
        # First render the template
        validation = template_service.validate_fields(
            request.template_id,
            request.fields
        )

        if not validation['is_valid']:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "Invalid fields",
                    "missing_fields": validation.get('missing_fields', []),
                    "invalid_fields": validation.get('invalid_fields', [])
                }
            )

        # Render template
        rendered_doc = template_service.render_template(
            request.template_id,
            request.fields,
            "text"  # Force text format for PDF
        )

        if not rendered_doc:
            raise HTTPException(status_code=500, detail="Failed to render template")

        # Get template metadata
        template = template_service.get_template(request.template_id)

        # Generate PDF
        pdf_metadata = {
            'title': template.get('name', 'Legal Document'),
            'author': 'LegalMitra',
            'subject': template.get('description', '')
        }

        pdf_buffer = pdf_generator.generate_pdf(
            content=rendered_doc,
            court_type=court_type,
            metadata=pdf_metadata
        )

        # Validate PDF compliance
        compliance = pdf_generator.validate_pdf_compliance(pdf_buffer)

        # Reset buffer position for reading
        pdf_buffer.seek(0)

        # Generate filename
        template_name = template.get('name', 'document').replace(' ', '_')
        from datetime import datetime
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{template_name}_{timestamp}.pdf"

        # Log PDF generation
        await audit_logger.log_template_usage(
            template_id=request.template_id,
            template_name=template.get('name'),
            category=template.get('category'),
            fields=request.fields,
            generated_doc_hash=audit_logger.hash_text(rendered_doc),
            context={'output_format': 'pdf', 'court_type': court_type}
        )

        # Return PDF as downloadable file
        return StreamingResponse(
            pdf_buffer,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename={filename}",
                "X-PDF-Compliance": "e-Courts Compatible" if compliance['e_courts_compatible'] else "Not Compatible",
                "X-File-Size-MB": str(compliance.get('file_size_mb', 0))
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
