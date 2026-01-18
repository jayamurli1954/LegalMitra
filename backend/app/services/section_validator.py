"""
Section Citation Validator - Prevents Legal Hallucinations
Validates that AI-cited sections actually exist in Indian Bare Acts
"""

import re
import json
import logging
from pathlib import Path
from typing import List, Dict, Tuple, Optional

logger = logging.getLogger(__name__)


class SectionValidator:
    """Validates legal section citations to prevent hallucinations"""

    def __init__(self):
        """Load bare acts registry"""
        self.bare_acts = self._load_bare_acts()
        logger.info("Section Validator initialized with bare acts registry")

    def _load_bare_acts(self) -> Dict:
        """Load bare acts from JSON file"""
        try:
            data_path = Path(__file__).parent.parent.parent / "data" / "bare_acts.json"
            with open(data_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load bare acts: {e}")
            return {}

    def extract_citations(self, text: str) -> List[Dict[str, str]]:
        """
        Extract all section citations from text

        Patterns matched:
        - Section 138 of the Negotiable Instruments Act
        - Section 302 IPC
        - IPC Section 420
        - Article 21
        - Section 80C of Income Tax Act

        Returns:
            List of dicts with 'section', 'act', 'full_match'
        """
        citations = []

        # Pattern 1: Section XXX of the YYY Act
        pattern1 = r'Section\s+(\d+[A-Z]?)\s+(?:of\s+(?:the\s+)?)?([A-Z][a-zA-Z\s,]+(?:Act|Code|Constitution))'
        for match in re.finditer(pattern1, text, re.IGNORECASE):
            section = match.group(1)
            act_name = match.group(2).strip()
            citations.append({
                'section': section,
                'act': self._normalize_act_name(act_name),
                'full_match': match.group(0),
                'position': match.start()
            })

        # Pattern 2: Section XXX IPC/CrPC/CPC/etc
        pattern2 = r'Section\s+(\d+[A-Z]?)\s+(IPC|CrPC|CPC|BNS|BNSS)'
        for match in re.finditer(pattern2, text, re.IGNORECASE):
            section = match.group(1)
            act_code = match.group(2).upper()
            citations.append({
                'section': section,
                'act': act_code,
                'full_match': match.group(0),
                'position': match.start()
            })

        # Pattern 3: Article XXX (Constitution)
        pattern3 = r'Article\s+(\d+[A-Z]?)'
        for match in re.finditer(pattern3, text, re.IGNORECASE):
            section = match.group(1)
            citations.append({
                'section': section,
                'act': 'CONSTITUTION',
                'full_match': match.group(0),
                'position': match.start()
            })

        # Pattern 4: Act Code Section XXX (e.g., "IPC Section 420")
        pattern4 = r'(IPC|CrPC|CPC|BNS|BNSS)\s+Section\s+(\d+[A-Z]?)'
        for match in re.finditer(pattern4, text, re.IGNORECASE):
            act_code = match.group(1).upper()
            section = match.group(2)
            citations.append({
                'section': section,
                'act': act_code,
                'full_match': match.group(0),
                'position': match.start()
            })

        # Remove duplicates based on section + act combination
        unique_citations = []
        seen = set()
        for citation in sorted(citations, key=lambda x: x['position']):
            key = (citation['section'], citation['act'])
            if key not in seen:
                seen.add(key)
                unique_citations.append(citation)

        return unique_citations

    def _normalize_act_name(self, act_name: str) -> str:
        """Normalize act name to match registry keys"""
        act_name_lower = act_name.lower()

        # Map common names to registry keys
        mappings = {
            'indian penal code': 'IPC',
            'penal code': 'IPC',
            'code of criminal procedure': 'CrPC',
            'criminal procedure code': 'CrPC',
            'code of civil procedure': 'CPC',
            'civil procedure code': 'CPC',
            'negotiable instruments act': 'NI_ACT',
            'ni act': 'NI_ACT',
            'goods and services tax act': 'GST_ACT',
            'central goods and services tax act': 'GST_ACT',
            'gst act': 'GST_ACT',
            'cgst act': 'GST_ACT',
            'digital personal data protection act': 'DPDP_ACT',
            'dpdp act': 'DPDP_ACT',
            'data protection act': 'DPDP_ACT',
            'companies act': 'COMPANIES_ACT',
            'income tax act': 'IT_ACT',
            'income-tax act': 'IT_ACT',
            'constitution of india': 'CONSTITUTION',
            'constitution': 'CONSTITUTION',
            'bharatiya nyaya sanhita': 'BNS',
            'bharatiya nagarik suraksha sanhita': 'BNSS'
        }

        for key, value in mappings.items():
            if key in act_name_lower:
                return value

        return act_name.upper().replace(' ', '_')

    def validate_citation(self, section: str, act: str) -> Tuple[bool, Optional[str]]:
        """
        Validate if a section exists in the specified act

        Returns:
            (is_valid, section_title)
        """
        if act not in self.bare_acts:
            return False, None

        sections = self.bare_acts[act].get('sections', {})

        if section in sections:
            return True, sections[section]

        return False, None

    def validate_text(self, text: str) -> Dict:
        """
        Validate all citations in text

        Returns:
            {
                'total_citations': int,
                'valid_citations': int,
                'invalid_citations': List[Dict],
                'is_valid': bool,
                'details': List[Dict]
            }
        """
        citations = self.extract_citations(text)

        if not citations:
            return {
                'total_citations': 0,
                'valid_citations': 0,
                'invalid_citations': [],
                'is_valid': True,
                'details': [],
                'message': 'No section citations found'
            }

        details = []
        invalid_citations = []
        valid_count = 0

        for citation in citations:
            is_valid, section_title = self.validate_citation(
                citation['section'],
                citation['act']
            )

            detail = {
                'citation': citation['full_match'],
                'section': citation['section'],
                'act': citation['act'],
                'is_valid': is_valid,
                'section_title': section_title
            }

            details.append(detail)

            if is_valid:
                valid_count += 1
            else:
                invalid_citations.append(detail)

        return {
            'total_citations': len(citations),
            'valid_citations': valid_count,
            'invalid_citations': invalid_citations,
            'is_valid': len(invalid_citations) == 0,
            'details': details,
            'accuracy_score': (valid_count / len(citations) * 100) if citations else 100
        }

    def check_foreign_law(self, text: str) -> Dict:
        """
        Check if text contains references to foreign laws

        Returns:
            {
                'has_foreign_law': bool,
                'foreign_references': List[str]
            }
        """
        foreign_patterns = [
            r'\bUS\s+Code\b',
            r'\bUK\s+Act\b',
            r'\bIRS\b',
            r'\bCFR\b',
            r'\bSupreme\s+Court\s+of\s+the\s+United\s+States\b',
            r'\bHouse\s+of\s+Lords\b',
            r'\bEuropean\s+Court\b',
            r'\bAmerican\s+law\b',
            r'\bBritish\s+law\b',
            r'\bFederal\s+Rules\b',
            r'\bUCC\b.*\bUniform\s+Commercial\s+Code\b'
        ]

        foreign_references = []
        for pattern in foreign_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                foreign_references.append(match.group(0))

        return {
            'has_foreign_law': len(foreign_references) > 0,
            'foreign_references': list(set(foreign_references))
        }

    def check_risky_language(self, text: str) -> Dict:
        """
        Check for risky legal language that violates Bar Council norms

        Returns:
            {
                'has_risky_language': bool,
                'risky_phrases': List[str]
            }
        """
        risky_patterns = [
            r'\bguarantee[ds]?\b',
            r'\bwill\s+definitely\b',
            r'\b100%\s+(?:chance|certain|sure)\b',
            r'\bcourt\s+will\s+(?:rule|decide|order)\b',
            r'\bsure\s+(?:win|outcome|victory)\b',
            r'\billegal\s+without\s+exception\b',
            r'\bpredicted?\s+outcome\b',
            r'\bcertain\s+(?:to\s+win|victory)\b'
        ]

        risky_phrases = []
        for pattern in risky_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                risky_phrases.append(match.group(0))

        return {
            'has_risky_language': len(risky_phrases) > 0,
            'risky_phrases': list(set(risky_phrases))
        }

    def get_act_info(self, act_code: str) -> Optional[Dict]:
        """Get full information about an act"""
        if act_code in self.bare_acts:
            return {
                'code': act_code,
                'full_name': self.bare_acts[act_code].get('full_name'),
                'total_sections': len(self.bare_acts[act_code].get('sections', {}))
            }
        return None

    def list_available_acts(self) -> List[Dict]:
        """List all available acts in the registry"""
        return [
            {
                'code': code,
                'full_name': data.get('full_name'),
                'total_sections': len(data.get('sections', {}))
            }
            for code, data in self.bare_acts.items()
        ]


# Singleton instance
section_validator = SectionValidator()
