"""
Gemini OCR Utility
Extracts text from images using Google Gemini Vision API (new google.genai SDK)
"""
import os
import base64
from typing import Optional
from app.core.config import get_settings

# Try to import new google.genai package
try:
    from google import genai
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False
    genai = None


def extract_text_from_image(image_bytes: bytes, mime_type: str = "image/png") -> str:
    """
    Extract text from image using Google Gemini Vision API (new SDK)
    
    Args:
        image_bytes: Image file bytes
        mime_type: MIME type of the image (e.g., "image/png", "image/jpeg")
    
    Returns:
        Extracted text from the image
    
    Raises:
        Exception: If API key is not configured or API call fails
    """
    if not GENAI_AVAILABLE:
        raise Exception(
            "google.genai package is not installed. "
            "Install with: pip uninstall google-generativeai && pip install google-genai"
        )
    
    settings = get_settings()
    
    if not settings.GOOGLE_GEMINI_API_KEY:
        raise Exception("GOOGLE_GEMINI_API_KEY is not configured in .env file")
    
    # Create client with API key
    client = genai.Client(api_key=settings.GOOGLE_GEMINI_API_KEY)
    
    # Encode image bytes to base64 for inline_data
    image_base64 = base64.b64encode(image_bytes).decode('utf-8')
    
    # Create prompt for legal document OCR
    prompt_text = (
        "Extract all readable text from this legal document image. "
        "Preserve the structure, formatting, and layout. "
        "If there are tables, preserve the table structure. "
        "If the document contains both Hindi and English text, extract both. "
        "Return only the extracted text without any additional commentary."
    )
    
    try:
        # Use new API structure with available model (gemini-2.5-flash or gemini-2.0-flash)
        # Try gemini-2.5-flash first (latest), fallback to gemini-2.0-flash
        model_name = "gemini-2.5-flash"
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=[
                    {
                        "role": "user",
                        "parts": [
                            {
                                "inline_data": {
                                    "mime_type": mime_type,
                                    "data": image_base64
                                }
                            },
                            {
                                "text": prompt_text
                            }
                        ]
                    }
                ]
            )
        except Exception as e:
            # Fallback to gemini-2.0-flash if 2.5 is not available
            if "404" in str(e) or "not found" in str(e).lower():
                model_name = "gemini-2.0-flash"
                response = client.models.generate_content(
                    model=model_name,
                    contents=[
                        {
                            "role": "user",
                            "parts": [
                                {
                                    "inline_data": {
                                        "mime_type": mime_type,
                                        "data": image_base64
                                    }
                                },
                                {
                                    "text": prompt_text
                                }
                            ]
                        }
                    ]
                )
            else:
                raise
        
        if response and response.text:
            return response.text.strip()
        else:
            raise Exception("Gemini API returned empty response")
            
    except Exception as e:
        # Provide helpful error message
        error_msg = str(e)
        error_str_lower = error_msg.lower()
        
        # Check for leaked API key error (most critical)
        if "leaked" in error_str_lower or "permission_denied" in error_str_lower or "403" in error_msg:
            if "leaked" in error_str_lower:
                raise Exception(
                    "⚠️ **SECURITY ALERT: Your Gemini API key has been reported as leaked.**\n\n"
                    "**This means your API key was exposed (possibly in a public repository, screenshot, or shared file).**\n\n"
                    "**IMMEDIATE ACTION REQUIRED:**\n"
                    "1. **Revoke the current API key** in Google AI Studio: https://makersuite.google.com/app/apikey\n"
                    "2. **Generate a new API key** from the same page\n"
                    "3. **Update your .env file** with the new key: GOOGLE_GEMINI_API_KEY=your_new_key\n"
                    "4. **Restart your server** for changes to take effect\n\n"
                    "**Alternative:** If you have OPENAI_API_KEY configured, the system will automatically use OpenAI Vision API as a fallback for OCR.\n\n"
                    f"**Original Error:** {error_msg}"
                )
            else:
                raise Exception(f"Gemini API permission denied (403). Please verify GOOGLE_GEMINI_API_KEY is correct and has proper permissions. Error: {error_msg}")
        elif "authentication" in error_str_lower or "invalid" in error_str_lower or "api_key" in error_str_lower or "unauthorized" in error_str_lower:
            raise Exception(f"Gemini API authentication failed. Please verify GOOGLE_GEMINI_API_KEY is correct in your .env file. Error: {error_msg}")
        elif "quota" in error_str_lower or "limit" in error_str_lower:
            raise Exception(f"Gemini API quota exceeded. Check Google Cloud Console for usage limits. Error: {error_msg}")
        else:
            raise Exception(f"Gemini API error: {error_msg}")


def get_mime_type_from_filename(filename: str) -> str:
    """
    Get MIME type from filename extension
    
    Args:
        filename: Name of the file
    
    Returns:
        MIME type string
    """
    filename_lower = filename.lower()
    if filename_lower.endswith('.png'):
        return "image/png"
    elif filename_lower.endswith('.jpg') or filename_lower.endswith('.jpeg'):
        return "image/jpeg"
    elif filename_lower.endswith('.gif'):
        return "image/gif"
    elif filename_lower.endswith('.webp'):
        return "image/webp"
    else:
        return "image/png"  # Default

