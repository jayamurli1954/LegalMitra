"""
Case-Law Citation Extractor - Phase 3
Extracts and validates case-law citations from legal text
"""

import re
from typing import Dict, List, Tuple


class CaseLawExtractor:
    """
    Extracts case-law citations in standard Indian formats:
    - Party v. Party (Year)
    - Party vs Party, Citation
    - AIR 1950 SC 27
    - (2020) 1 SCC 123
    """

    def __init__(self):
        # Indian case citation patterns
        self.CITATION_PATTERNS = [
            # AIR citations: AIR 1950 SC 27
            r'AIR\s+(\d{4})\s+(SC|[A-Z]{2,4})\s+\d+',

            # SCC citations: (2020) 1 SCC 123
            r'\((\d{4})\)\s+\d+\s+SCC\s+\d+',

            # Party names: ABC v. XYZ (Year)
            r'([A-Z][a-zA-Z\s&]+)\s+v\.?\s+([A-Z][a-zA-Z\s&]+)\s*\((\d{4})\)',

            # Party names with vs: ABC vs XYZ, Citation
            r'([A-Z][a-zA-Z\s&]+)\s+vs\.?\s+([A-Z][a-zA-Z\s&]+)',

            # High Court citations
            r'\d+\s+([A-Z]{2,4}HC)\s+\d+',

            # Law Reports
            r'(\d{4})\s+\d+\s+(SCC|SCR|Cri\.?LJ|AIR)\s+\d+'
        ]

        # Court abbreviations
        self.COURT_ABBREV = {
            'SC': 'Supreme Court of India',
            'SCC': 'Supreme Court Cases',
            'SCR': 'Supreme Court Reports',
            'AIR': 'All India Reporter',
            'HC': 'High Court',
            'DelhiHC': 'Delhi High Court',
            'BomHC': 'Bombay High Court',
            'CalHC': 'Calcutta High Court',
            'MadHC': 'Madras High Court',
            'KarHC': 'Karnataka High Court',
            'APHC': 'Andhra Pradesh High Court',
            'MPHC': 'Madhya Pradesh High Court',
            'RajHC': 'Rajasthan High Court',
            'KERHC': 'Kerala High Court',
            'GUJHC': 'Gujarat High Court'
        }

        # Famous landmark cases for validation
        self.LANDMARK_CASES = [
            'Kesavananda Bharati v. State of Kerala',
            'Maneka Gandhi v. Union of India',
            'Vishaka v. State of Rajasthan',
            'K.S. Puttaswamy v. Union of India',
            'Indra Sawhney v. Union of India',
            'Minerva Mills v. Union of India',
            'A.K. Gopalan v. State of Madras',
            'Golak Nath v. State of Punjab',
            'Rustom Cavasjee Cooper v. Union of India',
            'Shayara Bano v. Union of India',
            'Navtej Singh Johar v. Union of India',
            'Joseph Shine v. Union of India',
            'Common Cause v. Union of India'
        ]

    def extract_citations(self, text: str) -> List[Dict]:
        """
        Extract all case-law citations from text

        Args:
            text: Legal text to extract citations from

        Returns:
            List of citation dictionaries
        """
        citations = []
        seen = set()  # Avoid duplicates

        for pattern in self.CITATION_PATTERNS:
            matches = re.finditer(pattern, text, re.IGNORECASE)

            for match in matches:
                citation_text = match.group(0)

                # Skip if already seen
                if citation_text in seen:
                    continue
                seen.add(citation_text)

                # Parse citation details
                citation_info = self._parse_citation(citation_text, match)
                if citation_info:
                    citations.append(citation_info)

        # Also check for landmark cases
        for landmark in self.LANDMARK_CASES:
            if landmark.lower() in text.lower():
                # Find the full reference in text
                idx = text.lower().find(landmark.lower())
                # Extract surrounding context (up to 100 chars)
                start = max(0, idx - 20)
                end = min(len(text), idx + len(landmark) + 50)
                context = text[start:end]

                if landmark not in seen:
                    citations.append({
                        'citation': landmark,
                        'type': 'landmark_case',
                        'court': 'Supreme Court',
                        'year': self._extract_year_from_context(context),
                        'is_landmark': True,
                        'context': context.strip()
                    })
                    seen.add(landmark)

        return citations

    def _parse_citation(self, citation_text: str, match: re.Match) -> Dict:
        """Parse citation details from matched text"""

        # AIR citation
        if 'AIR' in citation_text:
            parts = citation_text.split()
            return {
                'citation': citation_text,
                'type': 'AIR',
                'year': parts[1] if len(parts) > 1 else None,
                'court': self.COURT_ABBREV.get(parts[2], parts[2]) if len(parts) > 2 else 'Unknown',
                'reporter': 'All India Reporter',
                'is_landmark': False
            }

        # SCC citation
        if 'SCC' in citation_text:
            year_match = re.search(r'\((\d{4})\)', citation_text)
            return {
                'citation': citation_text,
                'type': 'SCC',
                'year': year_match.group(1) if year_match else None,
                'court': 'Supreme Court',
                'reporter': 'Supreme Court Cases',
                'is_landmark': False
            }

        # Party names
        if ' v. ' in citation_text or ' vs ' in citation_text:
            year_match = re.search(r'\((\d{4})\)', citation_text)
            return {
                'citation': citation_text,
                'type': 'party_names',
                'year': year_match.group(1) if year_match else None,
                'court': 'Unknown',
                'is_landmark': self._check_if_landmark(citation_text)
            }

        # High Court citation
        if 'HC' in citation_text:
            return {
                'citation': citation_text,
                'type': 'high_court',
                'court': 'High Court',
                'is_landmark': False
            }

        return None

    def _check_if_landmark(self, citation_text: str) -> bool:
        """Check if citation matches a landmark case"""
        for landmark in self.LANDMARK_CASES:
            if landmark.lower() in citation_text.lower():
                return True
        return False

    def _extract_year_from_context(self, context: str) -> str:
        """Extract year from surrounding context"""
        year_match = re.search(r'\((\d{4})\)|(\d{4})', context)
        if year_match:
            return year_match.group(1) or year_match.group(2)
        return None

    def validate_citations(self, citations: List[Dict]) -> Dict:
        """
        Validate extracted citations

        Args:
            citations: List of extracted citations

        Returns:
            Validation summary
        """
        total = len(citations)
        valid = 0
        invalid = []

        for citation in citations:
            # Basic validation rules
            is_valid = True
            issues = []

            # Check year is reasonable (1950-2030)
            year = citation.get('year')
            if year:
                try:
                    year_int = int(year)
                    if year_int < 1950 or year_int > 2030:
                        is_valid = False
                        issues.append(f"Year {year} is out of reasonable range")
                except (ValueError, TypeError):
                    is_valid = False
                    issues.append("Invalid year format")

            # Check court is known
            court = citation.get('court', '')
            if court == 'Unknown' and not citation.get('is_landmark', False):
                issues.append("Court not identified")

            # Count as valid if no critical issues
            if is_valid:
                valid += 1
            else:
                invalid.append({
                    'citation': citation['citation'],
                    'issues': issues
                })

        return {
            'total_citations': total,
            'valid_citations': valid,
            'invalid_citations': invalid,
            'accuracy_score': round(valid / total * 100, 2) if total > 0 else 0,
            'has_landmark_cases': any(c.get('is_landmark', False) for c in citations),
            'courts_cited': list(set(c.get('court', 'Unknown') for c in citations))
        }

    def extract_and_validate(self, text: str) -> Dict:
        """
        Extract and validate case-law citations in one go

        Args:
            text: Legal text

        Returns:
            Combined extraction and validation results
        """
        citations = self.extract_citations(text)
        validation = self.validate_citations(citations)

        return {
            'citations': citations,
            'validation': validation,
            'summary': {
                'has_citations': len(citations) > 0,
                'citation_count': len(citations),
                'landmark_count': sum(1 for c in citations if c.get('is_landmark', False)),
                'supreme_court_count': sum(1 for c in citations if 'Supreme Court' in c.get('court', '')),
                'high_court_count': sum(1 for c in citations if 'High Court' in c.get('court', ''))
            }
        }


# Global instance
caselaw_extractor = CaseLawExtractor()


# Standalone extraction function
def extract_case_citations(text: str) -> Dict:
    """
    Convenience function to extract case citations

    Args:
        text: Legal text

    Returns:
        Extracted and validated citations
    """
    return caselaw_extractor.extract_and_validate(text)
