"""
Document Processor Service
Handles extraction of text from various document formats
"""

import io
from typing import Optional

# PDF processing
try:
    import PyPDF2
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False

try:
    import pdfplumber
    PDF_PLUMBER_AVAILABLE = True
except ImportError:
    PDF_PLUMBER_AVAILABLE = False

# Word document processing
try:
    from docx import Document
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False

# Image processing and OCR
try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

try:
    import pytesseract
    TESSERACT_AVAILABLE = True
except ImportError:
    TESSERACT_AVAILABLE = False

# AI Vision APIs (for better image processing)
# Note: We now use the new google.genai package (not deprecated google.generativeai)
# The gemini_ocr utility handles the actual API calls using the new SDK

try:
    from openai import OpenAI
    OPENAI_VISION_AVAILABLE = True
except Exception:
    OPENAI_VISION_AVAILABLE = False

from app.core.config import get_settings
import base64
import logging


class DocumentProcessor:
    """Service for processing and extracting text from various document formats"""
    
    def __init__(self):
        self.settings = get_settings()
    
    async def process_pdf(self, file_content: bytes) -> str:
        """Extract text from PDF file"""
        logger = logging.getLogger(__name__)
        
        if not PDF_AVAILABLE and not PDF_PLUMBER_AVAILABLE:
            raise Exception("PDF processing libraries not available. Please install PyPDF2 or pdfplumber.")
        
        pdf_file = io.BytesIO(file_content)
        text_parts = []
        last_error = None
        
        # Try pdfplumber first (better text extraction)
        if PDF_PLUMBER_AVAILABLE:
            try:
                pdf_file.seek(0)  # Reset file pointer
                with pdfplumber.open(pdf_file) as pdf:
                    for page_num, page in enumerate(pdf.pages, 1):
                        try:
                            page_text = page.extract_text()
                            if page_text and page_text.strip():
                                text_parts.append(page_text)
                        except Exception as page_error:
                            logger.warning(f"Error extracting text from page {page_num} with pdfplumber: {page_error}")
                            continue
                
                if text_parts:
                    extracted_text = "\n\n".join(text_parts)
                    if extracted_text.strip():
                        return extracted_text
            except Exception as e:
                last_error = f"pdfplumber error: {str(e)}"
                logger.warning(f"pdfplumber failed: {last_error}")
        
        # Fallback to PyPDF2 if pdfplumber failed or returned no text
        if PDF_AVAILABLE and not text_parts:
            try:
                pdf_file.seek(0)  # Reset file pointer
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                for page_num, page in enumerate(pdf_reader.pages, 1):
                    try:
                        text = page.extract_text()
                        if text and text.strip():
                            text_parts.append(text)
                    except Exception as page_error:
                        logger.warning(f"Error extracting text from page {page_num} with PyPDF2: {page_error}")
                        continue
                
                if text_parts:
                    extracted_text = "\n\n".join(text_parts)
                    if extracted_text.strip():
                        return extracted_text
            except Exception as e:
                last_error = f"PyPDF2 error: {str(e)}"
                logger.warning(f"PyPDF2 failed: {last_error}")
        
        # If no text was extracted, raise an informative error
        error_msg = "Could not extract text from PDF. "
        if last_error:
            error_msg += f"Last error: {last_error}. "
        error_msg += "The PDF might be image-based (scanned) or encrypted. "
        error_msg += "For image-based PDFs, consider converting pages to images and using OCR."
        raise Exception(error_msg)
    
    async def process_word(self, file_content: bytes, file_extension: str) -> str:
        """Extract text from Word document"""
        if not DOCX_AVAILABLE:
            raise Exception("Word document processing not available. Please install python-docx.")
        
        try:
            docx_file = io.BytesIO(file_content)
            doc = Document(docx_file)
            
            text_parts = []
            for paragraph in doc.paragraphs:
                if paragraph.text.strip():
                    text_parts.append(paragraph.text)
            
            # Also extract text from tables
            for table in doc.tables:
                for row in table.rows:
                    row_text = " | ".join(cell.text for cell in row.cells)
                    if row_text.strip():
                        text_parts.append(row_text)
            
            return "\n".join(text_parts) if text_parts else "No text could be extracted from the document."
            
        except Exception as e:
            raise Exception(f"Error processing Word document: {str(e)}")
    
    async def process_image(self, file_content: bytes, filename: str) -> str:
        """Extract text from image using OCR or AI vision"""
        logger = logging.getLogger(__name__)
        gemini_error = None
        openai_error = None
        last_error = None
        
        # Try Gemini OCR utility first (recommended approach)
        try:
            from app.utils.gemini_ocr import extract_text_from_image, get_mime_type_from_filename
            
            logger.info("Attempting Gemini OCR (using gemini_ocr utility)...")
            mime_type = get_mime_type_from_filename(filename)
            extracted_text = extract_text_from_image(file_content, mime_type)
            logger.info(f"Gemini OCR successful: Extracted {len(extracted_text)} characters")
            return extracted_text
        except ImportError:
            logger.warning("Gemini OCR utility not available, trying fallback method")
        except Exception as e:
            gemini_error = str(e)
            last_error = f"Gemini OCR error: {str(e)}"
            logger.error(f"Gemini OCR failed: {last_error}")
            import traceback
            logger.error(f"Error trace: {traceback.format_exc()}")
        
        # Note: No fallback to old deprecated SDK needed - gemini_ocr utility uses the new google.genai SDK
        # If it fails, we'll proceed to OpenAI or Tesseract fallbacks
        
        # Try OpenAI Vision API (most accurate if available)
        if OPENAI_VISION_AVAILABLE and self.settings:
            try:
                if self.settings.OPENAI_API_KEY:
                    client = OpenAI(api_key=self.settings.OPENAI_API_KEY)
                    
                    # Convert image to base64
                    image_base64 = base64.b64encode(file_content).decode('utf-8')
                    
                    # Determine image MIME type from filename
                    image_mime = "image/jpeg"
                    if filename.lower().endswith('.png'):
                        image_mime = "image/png"
                    
                    response = client.chat.completions.create(
                        model="gpt-4o",  # or gpt-4-vision-preview
                        messages=[
                            {
                                "role": "user",
                                "content": [
                                    {"type": "text", "text": "Extract all text from this image. If this is a legal document, preserve the formatting and structure."},
                                    {
                                        "type": "image_url",
                                        "image_url": {
                                            "url": f"data:{image_mime};base64,{image_base64}"
                                        }
                                    }
                                ]
                            }
                        ],
                        max_tokens=4000
                    )
                    if response and response.choices and response.choices[0].message.content:
                        return response.choices[0].message.content
            except Exception as e:
                openai_error = str(e)  # Store OpenAI error separately
                if not gemini_error:  # Only overwrite if Gemini didn't fail first
                    last_error = f"OpenAI Vision API error: {str(e)}"
                logger.warning(f"OpenAI vision failed: {str(e)}")
        
        # Fallback to OCR using pytesseract
        if TESSERACT_AVAILABLE and PIL_AVAILABLE:
            try:
                image = Image.open(io.BytesIO(file_content))
                text = pytesseract.image_to_string(image)
                if text and text.strip():
                    return text
                else:
                    raise Exception("OCR returned empty text")
            except Exception as e:
                last_error = f"OCR error: {str(e)}"
                logger.warning(f"OCR failed: {str(e)}")
        
        # If all methods failed, provide helpful error message
        logger.error(f"All image processing methods failed.")
        if gemini_error:
            logger.error(f"Gemini error: {gemini_error}")
        if openai_error:
            logger.error(f"OpenAI error: {openai_error}")
        if last_error:
            logger.error(f"Last error: {last_error}")
        
        error_msg = "Could not extract text from image.\n\n"
        
        # Prioritize showing Gemini error if it exists (most likely to be the issue)
        if gemini_error:
            error_msg += "**Gemini Vision API Error:**\n\n"
            error_msg += f"Gemini Vision API was attempted but failed with the following error:\n\n"
            error_msg += f"`{gemini_error}`\n\n"
            
            # Provide specific guidance based on common errors
            gemini_lower = gemini_error.lower()
            if "invalid" in gemini_lower or "authentication" in gemini_lower or "api_key" in gemini_lower or "unauthorized" in gemini_lower:
                error_msg += "**This appears to be an authentication error.**\n"
                error_msg += "Please verify your GOOGLE_GEMINI_API_KEY in .env file is correct and not expired.\n\n"
            elif "quota" in gemini_lower or "limit" in gemini_lower or "exceeded" in gemini_lower:
                error_msg += "**This appears to be a quota/rate limit error.**\n"
                error_msg += "Check your Google Cloud Console for API usage limits and quotas.\n\n"
            elif "permission" in gemini_lower or "access" in gemini_lower or "forbidden" in gemini_lower:
                error_msg += "**This appears to be a permissions error.**\n"
                error_msg += "Ensure 'Generative Language API' is enabled in your Google Cloud Console.\n\n"
            elif "not found" in gemini_lower or "404" in gemini_lower or "model" in gemini_lower:
                error_msg += "**This appears to be a model availability error.**\n"
                error_msg += "The Gemini model may not be available. Check Google's API status.\n\n"
            else:
                error_msg += "**Troubleshooting steps:**\n"
                error_msg += "1. Verify your GOOGLE_GEMINI_API_KEY in .env file is correct\n"
                error_msg += "2. Check Google Cloud Console for API usage and quotas\n"
                error_msg += "3. Ensure Generative Language API is enabled in Google Cloud Console\n"
                error_msg += "4. Check your internet connection\n\n"
        else:
            # Check if google-genai package is installed
            try:
                from google import genai
                if not (self.settings and self.settings.GOOGLE_GEMINI_API_KEY):
                    error_msg += "google-genai package is installed but API key is not configured.\n"
                    error_msg += "Add GOOGLE_GEMINI_API_KEY to your .env file.\n\n"
                else:
                    error_msg += "google-genai package is available but OCR failed.\n"
                    error_msg += "Check server console logs for details.\n\n"
            except ImportError:
                error_msg += "google-genai package is not installed.\n"
                error_msg += "Install with: pip install google-genai\n\n"
        
        # Mention other fallback options
        if not gemini_error or (gemini_error and "quota" not in gemini_error.lower()):
            error_msg += "**Alternative options:**\n"
            error_msg += "1. Fix the Gemini API key/configuration (recommended)\n"
            error_msg += "2. Use OpenAI API key (OPENAI_API_KEY in .env) for GPT-4 Vision\n"
            error_msg += "3. Install Tesseract OCR (https://github.com/tesseract-ocr/tesseract/wiki)\n"
        
        raise Exception(error_msg)


# Singleton instance
document_processor = DocumentProcessor()

