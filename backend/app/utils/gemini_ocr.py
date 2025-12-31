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
        # Use new API structure
        response = client.models.generate_content(
            model="gemini-1.5-flash",
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
        
        if response and response.text:
            return response.text.strip()
        else:
            raise Exception("Gemini API returned empty response")
            
    except Exception as e:
        # Provide helpful error message
        error_msg = str(e)
        if "authentication" in error_msg.lower() or "invalid" in error_msg.lower() or "api_key" in error_msg.lower():
            raise Exception(f"Gemini API authentication failed. Please verify GOOGLE_GEMINI_API_KEY is correct. Error: {error_msg}")
        elif "quota" in error_msg.lower() or "limit" in error_msg.lower():
            raise Exception(f"Gemini API quota exceeded. Check Google Cloud Console. Error: {error_msg}")
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

