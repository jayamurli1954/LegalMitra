"""
Document Review API endpoint for reviewing uploaded documents and images
Optimized for Render free tier (512MB memory limit)
"""

from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from fastapi.concurrency import run_in_threadpool
from pydantic import BaseModel
from typing import Optional
import logging
import os

logger = logging.getLogger(__name__)

# Free tier limits (Render 512MB)
MAX_FILE_SIZE = 300_000  # 300 KB for free tier
MAX_EXTRACTED_CHARS = 25_000  # 25k chars max for AI processing

# Lazy import to reduce startup memory
ai_service = None
document_processor = None

def get_ai_service():
    """Lazy load AI service"""
    global ai_service
    if ai_service is None:
        from app.services.ai_service import ai_service as _ai_service
        ai_service = _ai_service
    return ai_service

def get_document_processor():
    """Lazy load document processor"""
    global document_processor
    if document_processor is None:
        from app.services.document_processor import document_processor as _dp
        document_processor = _dp
    return document_processor

router = APIRouter()


def _truncate_text(text: str, max_chars: int = MAX_EXTRACTED_CHARS) -> str:
    """Truncate text to max_chars, preserving word boundaries"""
    if len(text) <= max_chars:
        return text
    # Truncate at word boundary
    truncated = text[:max_chars]
    last_space = truncated.rfind(' ')
    if last_space > max_chars * 0.9:  # If we can find a space near the end
        truncated = truncated[:last_space]
    return truncated + "\n\n[Document truncated for free tier - first 25,000 characters shown]"


def _process_document_sync(file_content: bytes, file_extension: str, filename: str) -> tuple[str, str]:
    """
    Synchronous document processing function for threadpool
    Returns: (extracted_text, document_type)
    """
    dp = get_document_processor()
    extracted_text = None
    document_type = 'unknown'
    
    try:
        if file_extension in ['png', 'jpeg', 'jpg']:
            # For images, use AI vision capabilities (async, but called from sync context)
            import asyncio
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
            extracted_text = loop.run_until_complete(
                dp.process_image(file_content, filename or 'image')
            )
            document_type = 'image'
        elif file_extension == 'pdf':
            import asyncio
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
            extracted_text = loop.run_until_complete(dp.process_pdf(file_content))
            document_type = 'pdf'
        elif file_extension in ['doc', 'docx']:
            import asyncio
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
            extracted_text = loop.run_until_complete(
                dp.process_word(file_content, file_extension)
            )
            document_type = 'word'
        elif file_extension == 'txt':
            extracted_text = file_content.decode('utf-8', errors='ignore')
            document_type = 'text'
    except Exception as e:
        logger.error(f"Document processing error: {e}")
        raise
    
    # FIX 2: Truncate extracted text to prevent memory issues
    if extracted_text:
        extracted_text = _truncate_text(extracted_text, MAX_EXTRACTED_CHARS)
    
    return extracted_text or "", document_type


class DocumentReviewResponse(BaseModel):
    """Response model for document review"""
    analysis: str
    document_type: str
    extracted_text: Optional[str] = None


@router.post("/review-document", response_model=DocumentReviewResponse)
async def review_document(
    file: UploadFile = File(...),
    query: Optional[str] = Form(None)
):
    """
    Review an uploaded document or image
    
    Supports:
    - PDF files (.pdf)
    - Word documents (.doc, .docx)
    - Images (.png, .jpeg, .jpg) - uses OCR/AI vision
    - Text files (.txt)
    """
    try:
        # Validate file type
        file_extension = file.filename.split('.')[-1].lower() if file.filename else ''
        allowed_extensions = ['pdf', 'doc', 'docx', 'png', 'jpeg', 'jpg', 'txt']
        
        if file_extension not in allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type. Supported types: {', '.join(allowed_extensions)}"
            )
        
        # Read file content
        file_content = await file.read()
        
        # FIX 1: Hard size limit for free tier
        if len(file_content) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=413,
                detail=f"File too large for free tier. Maximum size: {MAX_FILE_SIZE // 1000}KB. Your file: {len(file_content) // 1000}KB. Please upload a smaller document."
            )
        
        # FIX 4: Offload heavy document processing to threadpool
        try:
            extracted_text, document_type = await run_in_threadpool(
                _process_document_sync,
                file_content,
                file_extension,
                file.filename or 'document'
            )
        except Exception as process_error:
            # If document processing fails, still try to proceed but inform user
            error_detail = str(process_error)
            extracted_text = None
            
            # Provide helpful error message about what went wrong
            if file_extension in ['png', 'jpeg', 'jpg']:
                # Image processing failed
                if 'tesseract' in error_detail.lower() or 'ocr' in error_detail.lower():
                    error_message = (
                        "**Image Processing Failed:**\n\n"
                        "The uploaded image could not be processed because OCR (Optical Character Recognition) is not available.\n\n"
                        "**To enable image processing, you need one of the following:**\n"
                        "1. **Google Gemini API Key** (recommended) - Add `GOOGLE_GEMINI_API_KEY` to your `.env` file\n"
                        "2. **OpenAI API Key** - Add `OPENAI_API_KEY` to your `.env` file (for GPT-4 Vision)\n"
                        "3. **Tesseract OCR** - Install Tesseract OCR and configure it (https://github.com/tesseract-ocr/tesseract/wiki)\n\n"
                        f"**Technical Error:** {error_detail}"
                    )
                else:
                    # Check if the error mentions Gemini specifically
                    if 'gemini' in error_detail.lower() or 'vision' in error_detail.lower():
                        error_message = (
                            f"**Gemini Vision API Error:**\n\n"
                            f"Gemini Vision API was attempted but failed with the following error:\n\n"
                            f"{error_detail}\n\n"
                            "**Possible causes:**\n"
                            "1. Invalid or expired Gemini API key\n"
                            "2. API quota exceeded (check Google Cloud Console)\n"
                            "3. Network connectivity issue\n"
                            "4. Model not available or API endpoint changed\n\n"
                            "**To fix:**\n"
                            "- Verify your GOOGLE_GEMINI_API_KEY in .env file is correct\n"
                            "- Check Google Cloud Console for API usage and quotas\n"
                            "- Ensure Generative Language API is enabled in Google Cloud Console\n"
                            "- Check server console logs for detailed error information"
                        )
                    else:
                        error_message = (
                            f"**Image Processing Error:**\n\n"
                            f"The image could not be processed. Error: {error_detail}\n\n"
                            "Please ensure you have a valid API key configured for image processing (Gemini or OpenAI)."
                        )
            else:
                error_message = (
                    f"**Document Processing Error:**\n\n"
                    f"The document could not be processed. Error: {error_detail}\n\n"
                    "Please check if the file format is supported and try again."
                )
        
        # Create query for AI analysis - FIX 8: Limit to case context summary only
        user_query = query.strip() if query and query.strip() else "Please provide a concise case context summary (2-3 KB) of this document focusing on key facts, parties, and legal issues."
        
        # Combine extracted text with user query (already truncated)
        if extracted_text and extracted_text.strip():
            # FIX 2: Text is already truncated in _process_document_sync
            analysis_query = f"{user_query}\n\nDocument Content (first 25,000 chars):\n{extracted_text}"
        else:
            # If no text was extracted, provide detailed error message
            if 'error_message' in locals():
                # Return the error message directly instead of asking AI to explain it
                analysis = error_message
            else:
                # Fallback if error_message wasn't set
                analysis = (
                    "**Document Processing Failed:**\n\n"
                    "The document content could not be extracted. This may be due to:\n"
                    "- Unsupported file format\n"
                    "- Corrupted file\n"
                    "- Image-based document without OCR capability\n\n"
                    "Please try uploading a different file format or ensure OCR/vision APIs are configured."
                )
            
            # Return early with error message instead of asking AI
            return DocumentReviewResponse(
                analysis=analysis,
                document_type=document_type,
                extracted_text=None
            )
        
        # Note: Documents are processed temporarily and not saved to storage
        # This ensures privacy and prevents storage buildup
        
        # FIX 3: Get AI analysis with defensive error handling
        try:
            ai = get_ai_service()
            # FIX 8: Add prompt instruction to limit response length
            limited_query = f"{analysis_query}\n\nIMPORTANT: Keep your response concise. Maximum 800 words. Use numbered points. Do not exceed this limit."
            analysis = await ai.process_legal_query(
                query=limited_query,
                query_type="research"
            )
        except Exception as ai_error:
            # Provide helpful error message for AI service failures
            error_msg = str(ai_error)
            
            # Detect which API actually failed from the error URL
            actual_api = "Unknown"
            if "api.x.ai" in error_msg:
                actual_api = "Grok (x.ai)"
            elif "generativelanguage.googleapis.com" in error_msg or "gemini" in error_msg.lower():
                actual_api = "Gemini (Google)"
            elif "api.openai.com" in error_msg:
                actual_api = "OpenAI"
            elif "api.anthropic.com" in error_msg:
                actual_api = "Anthropic"
            
            # Check what provider is configured (may differ if server not restarted)
            from app.core.config import get_settings
            get_settings.cache_clear()  # Clear cache to get fresh settings
            settings = get_settings()
            configured_provider = settings.AI_PROVIDER.lower().strip()
            
            # Build user-friendly error message
            if "403" in error_msg or "Forbidden" in error_msg:
                if "api.x.ai" in error_msg:
                    analysis = (
                        "**AI Analysis Failed - Grok API Error:**\n\n"
                        "The document was successfully processed, but the AI analysis failed because the server is still using the Grok API, which returned a 403 Forbidden error.\n\n"
                        "**Error:** 403 Forbidden from https://api.x.ai/v1/chat/completions\n\n"
                        "**This usually means:**\n"
                        "1. Your GROK_API_KEY in .env file is invalid or expired\n"
                        "2. The API key doesn't have the necessary permissions\n"
                        "3. Your API subscription/quota has been exceeded\n\n"
                        "**IMPORTANT - Server Needs Restart:**\n"
                        "The .env file has been updated to use Gemini, but the server must be restarted for changes to take effect.\n\n"
                        "**To fix immediately:**\n"
                        "1. Stop the server (Ctrl+C)\n"
                        "2. Restart: python -m uvicorn app.main:app --host 0.0.0.0 --port 8888 --reload\n"
                        "3. The server will then use Gemini API instead of Grok\n\n"
                        f"**Current AI_PROVIDER in .env:** {configured_provider}\n\n"
                        f"**Extracted Document Text (first 1000 chars):**\n{extracted_text[:1000] if extracted_text else 'No text extracted'}"
                    )
                else:
                    analysis = (
                        f"**AI Analysis Failed - {actual_api} API Error:**\n\n"
                        f"The document was successfully processed, but the AI analysis failed due to an authentication error.\n\n"
                        f"**Error:** {error_msg}\n\n"
                        f"**To fix:**\n"
                        f"- Verify your API key in the .env file is correct\n"
                        f"- Check your {actual_api} account for status and quotas\n"
                        f"- If you recently changed AI_PROVIDER, make sure to restart the server\n"
                        f"- Consider switching to a different AI provider by changing AI_PROVIDER in .env\n\n"
                        f"**Current AI_PROVIDER:** {configured_provider}\n\n"
                        f"**Extracted Document Text (first 1000 chars):**\n{extracted_text[:1000] if extracted_text else 'No text extracted'}"
                    )
            elif "401" in error_msg or "Unauthorized" in error_msg:
                analysis = (
                    "**AI Analysis Failed:**\n\n"
                    "The document was successfully processed, but the AI analysis failed due to an authentication error.\n\n"
                    f"**Error:** {error_msg}\n\n"
                    "**To fix:**\n"
                    "- Verify your API key in the .env file is correct and not expired\n"
                    "- Check your API account dashboard for authentication status\n"
                    f"- Current AI Provider: {configured_provider.upper()}\n"
                    f"- Actual API that failed: {actual_api}\n\n"
                    f"**Extracted Document Text (first 1000 chars):**\n{extracted_text[:1000] if extracted_text else 'No text extracted'}"
                )
            else:
                analysis = (
                    "**AI Analysis Failed:**\n\n"
                    "The document was successfully processed and text extracted, but the AI analysis encountered an error.\n\n"
                    f"**Error:** {error_msg}\n\n"
                    f"**Current AI Provider:** {configured_provider.upper()}\n"
                    f"**Actual API that failed:** {actual_api}\n\n"
                    "**Possible solutions:**\n"
                    "- Check your API key configuration in .env file\n"
                    "- Verify your API account status and quotas\n"
                    "- If you recently changed AI_PROVIDER, make sure to restart the server\n"
                    "- Try switching to a different AI provider (Gemini, OpenAI, Anthropic)\n"
                    "- Check server logs for detailed error information\n\n"
                    f"**Extracted Document Text (first 1000 chars):**\n{extracted_text[:1000] if extracted_text else 'No text extracted'}"
                )
        
        return DocumentReviewResponse(
            analysis=analysis,
            document_type=document_type,
            extracted_text=extracted_text[:1000] if extracted_text else None  # Return first 1000 chars as preview
        )
        
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        error_detail = str(e)
        traceback_str = traceback.format_exc()
        print(f"Document review error: {error_detail}")
        print(f"Traceback: {traceback_str}")
        raise HTTPException(
            status_code=500, 
            detail=f"Error processing document: {error_detail}"
        )

