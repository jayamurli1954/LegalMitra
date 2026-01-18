"""
Template API - Document template management for LegalMitra
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Optional, Any
from app.templates.template_service import template_service, Template

router = APIRouter()


class TemplateListResponse(BaseModel):
    categories: Dict[str, Any]
    total_templates: int


class TemplateFillRequest(BaseModel):
    template_id: str
    field_values: Dict[str, Any]
    ai_enhance: bool = True


class TemplateFillResponse(BaseModel):
    template_id: str
    template_name: str
    filled_document: str


@router.get("/templates/categories", response_model=Dict[str, Any])
async def get_categories():
    """Get all template categories"""
    try:
        categories = template_service.get_all_categories()
        return categories
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/templates/summary")
async def get_templates_summary():
    """Get summary of all templates"""
    try:
        categories = template_service.get_all_categories()
        all_templates = template_service.catalog.get("templates", [])

        # Count templates by category
        category_counts = {}
        for template in all_templates:
            cat = template.get("category", "unknown")
            category_counts[cat] = category_counts.get(cat, 0) + 1

        return {
            "total_templates": len(all_templates),
            "total_categories": len(categories),
            "categories": categories,
            "templates_per_category": category_counts
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/templates/category/{category}")
async def get_templates_by_category(category: str):
    """Get templates for a specific category"""
    try:
        templates = template_service.get_templates_by_category(category)
        # Convert Pydantic models to dicts for JSON serialization (Pydantic v2 uses model_dump)
        templates_dict = []
        for t in templates:
            if hasattr(t, 'model_dump'):
                templates_dict.append(t.model_dump())
            elif hasattr(t, 'dict'):
                templates_dict.append(t.dict())
            else:
                templates_dict.append(t)
        return {
            "category": category,
            "count": len(templates),
            "templates": templates_dict
        }
    except Exception as e:
        import traceback
        print(f"Error in get_templates_by_category: {e}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/templates/{template_id}")
async def get_template(template_id: str):
    """Get specific template details"""
    try:
        template = template_service.get_template_by_id(template_id)
        if not template:
            raise HTTPException(status_code=404, detail="Template not found")
        # Convert Pydantic model to dict for JSON serialization (Pydantic v2 uses model_dump)
        if hasattr(template, 'model_dump'):
            return template.model_dump()
        elif hasattr(template, 'dict'):
            return template.dict()
        else:
            return template
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        print(f"Error in get_template: {e}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/templates/search/{query}")
async def search_templates(query: str, user_type: Optional[str] = None):
    """Search templates by keyword"""
    try:
        results = template_service.search_templates(query, user_type)
        return {
            "query": query,
            "user_type": user_type,
            "count": len(results),
            "results": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/templates/fill", response_model=TemplateFillResponse)
async def fill_template(request: TemplateFillRequest):
    """Fill a template with provided values and optionally enhance with AI"""
    try:
        filled_document = await template_service.fill_template(
            template_id=request.template_id,
            field_values=request.field_values,
            ai_enhance=request.ai_enhance
        )

        template = template_service.get_template_by_id(request.template_id)

        return TemplateFillResponse(
            template_id=request.template_id,
            template_name=template.name,
            filled_document=filled_document
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/templates/user-type/{user_type}")
async def get_templates_for_user_type(user_type: str):
    """Get templates applicable for specific user type (CA, Corporate, Lawyer, etc.)"""
    try:
        all_templates = template_service.catalog.get("templates", [])
        filtered_templates = [
            Template(**t) for t in all_templates
            if user_type in t.get("applicable_for", [])
        ]

        return {
            "user_type": user_type,
            "count": len(filtered_templates),
            "templates": filtered_templates
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
