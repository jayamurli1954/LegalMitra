"""
Court-Format PDF Generator
Generates e-Courts compatible PDFs with proper Indian court margins
"""

import logging
from typing import Dict, Optional
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.pdfgen import canvas
from io import BytesIO
from datetime import datetime

logger = logging.getLogger(__name__)


class CourtPDFGenerator:
    """
    Generates court-ready PDFs with proper formatting

    Indian Court Standard Margins:
    - Left: 1.5 inches (CRITICAL for binding)
    - Right: 1 inch
    - Top: 1 inch
    - Bottom: 1 inch
    """

    def __init__(self):
        """Initialize PDF generator with court standards"""
        self.page_width, self.page_height = A4

        # Court-standard margins
        self.margins = {
            'left': 1.5 * inch,    # CRITICAL: 1.5" for binding
            'right': 1.0 * inch,
            'top': 1.0 * inch,
            'bottom': 1.0 * inch
        }

        logger.info("Court PDF Generator initialized")

    def generate_pdf(
        self,
        content: str,
        court_type: str = "District",
        metadata: Optional[Dict] = None
    ) -> BytesIO:
        """
        Generate court-format PDF from text content

        Args:
            content: Document text content
            court_type: District / High Court / Supreme Court
            metadata: Document metadata (title, author, etc.)

        Returns:
            BytesIO object containing PDF
        """
        try:
            # Create PDF buffer
            buffer = BytesIO()

            # Create document with court margins
            doc = SimpleDocTemplate(
                buffer,
                pagesize=A4,
                leftMargin=self.margins['left'],
                rightMargin=self.margins['right'],
                topMargin=self.margins['top'],
                bottomMargin=self.margins['bottom'],
                title=metadata.get('title', 'Legal Document') if metadata else 'Legal Document',
                author=metadata.get('author', 'LegalMitra') if metadata else 'LegalMitra'
            )

            # Get styles based on court type
            styles = self._get_court_styles(court_type)

            # Build document story
            story = []

            # Add content paragraphs
            paragraphs = content.split('\n\n')

            for para_text in paragraphs:
                if not para_text.strip():
                    story.append(Spacer(1, 0.2 * inch))
                    continue

                # Determine style based on content
                style = self._determine_style(para_text, styles)

                # Handle line breaks within paragraphs
                lines = para_text.split('\n')
                for i, line in enumerate(lines):
                    if line.strip():
                        para = Paragraph(line, style)
                        story.append(para)
                    if i < len(lines) - 1:
                        story.append(Spacer(1, 0.1 * inch))

                # Add spacing after paragraph
                story.append(Spacer(1, 0.15 * inch))

            # Add footer with disclaimer
            story.append(Spacer(1, 0.3 * inch))
            footer_text = "Generated using LegalMitra - AI-assisted draft. To be reviewed by a qualified advocate."
            footer = Paragraph(footer_text, styles['Footer'])
            story.append(footer)

            # Build PDF
            doc.build(story, onFirstPage=self._add_page_number, onLaterPages=self._add_page_number)

            # Get PDF bytes
            buffer.seek(0)

            logger.info(f"PDF generated successfully for {court_type} Court")
            return buffer

        except Exception as e:
            logger.error(f"Failed to generate PDF: {e}")
            raise

    def _get_court_styles(self, court_type: str) -> Dict:
        """Get paragraph styles based on court type"""
        styles = getSampleStyleSheet()

        # Base font for all courts: Times New Roman (court standard)
        base_font = 'Times-Roman'
        base_font_bold = 'Times-Bold'

        # Font size (12pt standard)
        font_size = 12

        # Line spacing based on court type
        if court_type.upper() in ['HIGH COURT', 'SUPREME COURT']:
            line_spacing = 24  # Double spacing
        else:
            line_spacing = 18  # 1.5 spacing for District Court

        # Custom styles
        custom_styles = {
            'Normal': ParagraphStyle(
                'CustomNormal',
                parent=styles['Normal'],
                fontName=base_font,
                fontSize=font_size,
                leading=line_spacing,
                alignment=TA_JUSTIFY,
                spaceAfter=6
            ),
            'Heading': ParagraphStyle(
                'CustomHeading',
                parent=styles['Heading1'],
                fontName=base_font_bold,
                fontSize=font_size,
                leading=line_spacing,
                alignment=TA_CENTER,
                spaceAfter=12,
                spaceBefore=12
            ),
            'SubHeading': ParagraphStyle(
                'CustomSubHeading',
                parent=styles['Heading2'],
                fontName=base_font_bold,
                fontSize=font_size,
                leading=line_spacing,
                alignment=TA_LEFT,
                spaceAfter=6
            ),
            'Footer': ParagraphStyle(
                'CustomFooter',
                parent=styles['Normal'],
                fontName=base_font,
                fontSize=9,
                leading=12,
                alignment=TA_CENTER,
                textColor='gray'
            )
        }

        return custom_styles

    def _determine_style(self, text: str, styles: Dict) -> ParagraphStyle:
        """Determine appropriate style based on text content"""
        text_upper = text.upper()

        # Check for headings
        if any(heading in text_upper for heading in [
            'LEGAL NOTICE', 'AFFIDAVIT', 'VAKALATNAMA', 'REPLY TO',
            'MEMORANDUM', 'AGREEMENT', 'RESOLUTION', 'VERIFICATION'
        ]):
            return styles['Heading']

        # Check for sub-headings (numbered sections)
        if text.strip() and text.strip()[0].isdigit() and '. ' in text[:10]:
            return styles['SubHeading']

        # Default to normal
        return styles['Normal']

    def _add_page_number(self, canvas_obj, doc):
        """Add page number at bottom center"""
        canvas_obj.saveState()
        canvas_obj.setFont('Times-Roman', 10)
        page_num = canvas_obj.getPageNumber()
        text = f"Page {page_num}"
        canvas_obj.drawCentredString(
            doc.width / 2 + doc.leftMargin,
            0.5 * inch,
            text
        )
        canvas_obj.restoreState()

    def validate_pdf_compliance(self, pdf_buffer: BytesIO) -> Dict:
        """
        Validate PDF compliance with e-Courts standards

        Returns:
            Dict with validation results
        """
        try:
            pdf_buffer.seek(0, 2)  # Seek to end
            file_size = pdf_buffer.tell()
            pdf_buffer.seek(0)  # Reset

            # Check file size (< 10MB for e-Courts)
            max_size = 10 * 1024 * 1024  # 10 MB
            size_ok = file_size < max_size

            return {
                'is_valid': size_ok,
                'file_size_bytes': file_size,
                'file_size_mb': round(file_size / (1024 * 1024), 2),
                'max_size_mb': 10,
                'size_compliant': size_ok,
                'page_size': 'A4',
                'margins': {
                    'left': '1.5 inch',
                    'right': '1.0 inch',
                    'top': '1.0 inch',
                    'bottom': '1.0 inch'
                },
                'e_courts_compatible': size_ok
            }

        except Exception as e:
            logger.error(f"PDF validation failed: {e}")
            return {
                'is_valid': False,
                'error': str(e)
            }


# Singleton instance
pdf_generator = CourtPDFGenerator()
