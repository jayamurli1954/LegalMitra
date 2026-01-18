"""
Legal Accuracy Scoring Engine - Phase 3
Quantifies legal reliability of AI-generated responses before showing to users
"""

from typing import Dict, List, Tuple
import re


class LegalAccuracyScorer:
    """
    Scores legal responses on multiple dimensions:
    - Correct statute cited (30 points)
    - Correct section numbers (30 points)
    - No foreign law (15 points)
    - No guarantee language (15 points)
    - Disclaimer present (10 points)

    Score >= 85: Show normally
    Score 70-84: Show with warning
    Score < 70: Block/regenerate
    """

    def __init__(self, section_validator=None):
        self.section_validator = section_validator

        # Guarantee language patterns (Bar Council unsafe)
        self.GUARANTEE_PATTERNS = [
            r'\bguarantee\b',
            r'\bwill\s+(?:definitely|certainly|surely)\b',
            r'\b100%\s+(?:chance|sure|certain)\b',
            r'\bcourt\s+will\s+(?:rule|decide|grant)\b',
            r'\billegal\s+without\s+exception\b',
            r'\byou\s+will\s+(?:win|lose)\b',
            r'\bassured\s+(?:success|victory|outcome)\b',
            r'\bno\s+doubt\s+about\s+(?:winning|success)\b',
            r'\bcan\s+never\s+fail\b'
        ]

        # Foreign law indicators
        self.FOREIGN_LAW_TERMS = [
            "US Code", "USC", "United States Code",
            "UK Act", "British law", "English law",
            "IRS", "Internal Revenue Service",
            "CFR", "Code of Federal Regulations",
            "Supreme Court of the United States", "SCOTUS",
            "House of Lords", "Court of Appeal (UK)",
            "European Union law", "EU Regulation",
            "Canadian law", "Australian law"
        ]

        # Indian law indicators
        self.INDIAN_LAW_TERMS = [
            "Indian Penal Code", "IPC",
            "Code of Criminal Procedure", "CrPC",
            "Code of Civil Procedure", "CPC",
            "Constitution of India",
            "Supreme Court of India",
            "High Court",
            "District Court",
            "Negotiable Instruments Act",
            "GST Act", "CGST", "SGST",
            "Companies Act",
            "Income Tax Act",
            "Consumer Protection Act",
            "Bharatiya Nyaya Sanhita", "BNS"
        ]

        # Disclaimer patterns
        self.DISCLAIMER_PATTERNS = [
            r'legal advice',
            r'consult.*(?:advocate|lawyer)',
            r'not.*(?:legal advice|final opinion)',
            r'review.*qualified\s+advocate',
            r'general.*explanation',
            r'educational.*purpose'
        ]

    def score_response(self, response_text: str, expected_act: str = None) -> Dict:
        """
        Score a legal response on multiple dimensions

        Args:
            response_text: The AI-generated legal response
            expected_act: Optional - the Act that should be cited (e.g., "IPC", "GST_ACT")

        Returns:
            Dict with score, breakdown, and enforcement action
        """
        score = 100
        breakdown = {}
        warnings = []
        errors = []

        # Dimension 1: Correct statute cited (30 points)
        statute_score, statute_details = self._score_statute_citation(response_text, expected_act)
        score += statute_score
        breakdown['statute_citation'] = {
            'score': statute_score,
            'max': 30,
            'details': statute_details
        }
        if statute_score < 0:
            errors.extend(statute_details.get('errors', []))

        # Dimension 2: Correct section numbers (30 points)
        section_score, section_details = self._score_section_validity(response_text)
        score += section_score
        breakdown['section_validity'] = {
            'score': section_score,
            'max': 30,
            'details': section_details
        }
        if section_score < 0:
            errors.extend(section_details.get('errors', []))

        # Dimension 3: No foreign law (15 points)
        foreign_law_score, foreign_law_details = self._score_foreign_law_absence(response_text)
        score += foreign_law_score
        breakdown['no_foreign_law'] = {
            'score': foreign_law_score,
            'max': 15,
            'details': foreign_law_details
        }
        if foreign_law_score < 0:
            warnings.extend(foreign_law_details.get('warnings', []))

        # Dimension 4: No guarantee language (15 points)
        guarantee_score, guarantee_details = self._score_guarantee_absence(response_text)
        score += guarantee_score
        breakdown['no_guarantee_language'] = {
            'score': guarantee_score,
            'max': 15,
            'details': guarantee_details
        }
        if guarantee_score < 0:
            warnings.extend(guarantee_details.get('warnings', []))

        # Dimension 5: Disclaimer present (10 points)
        disclaimer_score, disclaimer_details = self._score_disclaimer_presence(response_text)
        score += disclaimer_score
        breakdown['disclaimer_present'] = {
            'score': disclaimer_score,
            'max': 10,
            'details': disclaimer_details
        }
        if disclaimer_score < 0:
            warnings.append("Missing legal disclaimer")

        # Determine enforcement action
        if score >= 85:
            action = "SHOW_NORMAL"
            action_message = "Response meets high quality standards"
        elif score >= 70:
            action = "SHOW_WITH_WARNING"
            action_message = "Response has minor quality issues, show with warning"
        else:
            action = "BLOCK_OR_REGENERATE"
            action_message = "Response quality below acceptable threshold"

        return {
            'total_score': score,
            'max_score': 100,
            'percentage': score,
            'grade': self._score_to_grade(score),
            'action': action,
            'action_message': action_message,
            'breakdown': breakdown,
            'warnings': warnings,
            'errors': errors,
            'is_safe_to_show': score >= 70
        }

    def _score_statute_citation(self, text: str, expected_act: str = None) -> Tuple[int, Dict]:
        """Score correctness of statute citations"""
        details = {'indian_laws_cited': [], 'missing_citations': False, 'errors': []}

        # Check if any Indian law is cited
        cited_count = 0
        for term in self.INDIAN_LAW_TERMS:
            if term.lower() in text.lower():
                cited_count += 1
                details['indian_laws_cited'].append(term)

        if cited_count == 0:
            details['missing_citations'] = True
            details['errors'].append("No Indian statute cited")
            return (-30, details)  # Full penalty

        # If specific Act expected, check if it's cited
        if expected_act:
            act_patterns = {
                'IPC': r'\b(?:IPC|Indian Penal Code)\b',
                'BNS': r'\b(?:BNS|Bharatiya Nyaya Sanhita)\b',
                'CrPC': r'\b(?:CrPC|Code of Criminal Procedure)\b',
                'CPC': r'\b(?:CPC|Code of Civil Procedure)\b',
                'NI_ACT': r'\b(?:Negotiable Instruments Act|NI Act)\b',
                'GST_ACT': r'\b(?:GST Act|CGST|SGST)\b',
                'COMPANIES_ACT': r'\b(?:Companies Act)\b',
                'IT_ACT': r'\b(?:Income Tax Act)\b',
                'CONSUMER_ACT': r'\b(?:Consumer Protection Act)\b'
            }

            if expected_act in act_patterns:
                if not re.search(act_patterns[expected_act], text, re.IGNORECASE):
                    details['errors'].append(f"Expected {expected_act} not cited")
                    return (-15, details)  # Partial penalty

        return (0, details)  # No penalty, correct citation

    def _score_section_validity(self, text: str) -> Tuple[int, Dict]:
        """Score validity of section numbers"""
        details = {'total_citations': 0, 'valid_citations': 0, 'invalid_citations': [], 'errors': []}

        if not self.section_validator:
            # Can't validate without validator
            return (0, details)

        # Use existing section validator
        validation = self.section_validator.validate_text(text)

        details['total_citations'] = validation['total_citations']
        details['valid_citations'] = validation['valid_citations']
        details['invalid_citations'] = validation['invalid_citations']

        if validation['total_citations'] == 0:
            # No sections cited - neutral (0 points)
            return (0, details)

        # Calculate accuracy
        accuracy = validation['accuracy_score'] / 100.0  # Convert percentage to 0-1

        if accuracy == 1.0:
            return (0, details)  # Perfect, no penalty
        elif accuracy >= 0.8:
            return (-10, details)  # Minor errors
        elif accuracy >= 0.5:
            details['errors'].append(f"{len(details['invalid_citations'])} invalid section citations")
            return (-20, details)  # Major errors
        else:
            details['errors'].append(f"Majority of citations invalid ({len(details['invalid_citations'])} errors)")
            return (-30, details)  # Critical errors

    def _score_foreign_law_absence(self, text: str) -> Tuple[int, Dict]:
        """Score absence of foreign law references"""
        details = {'has_foreign_law': False, 'foreign_terms_found': [], 'warnings': []}

        for term in self.FOREIGN_LAW_TERMS:
            if term in text:
                details['has_foreign_law'] = True
                details['foreign_terms_found'].append(term)

        if details['has_foreign_law']:
            details['warnings'].append(f"Foreign law references detected: {', '.join(details['foreign_terms_found'])}")
            return (-15, details)  # Full penalty

        return (0, details)  # No penalty

    def _score_guarantee_absence(self, text: str) -> Tuple[int, Dict]:
        """Score absence of guarantee/outcome prediction language"""
        details = {'has_guarantees': False, 'guarantee_phrases': [], 'warnings': []}

        for pattern in self.GUARANTEE_PATTERNS:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                details['has_guarantees'] = True
                details['guarantee_phrases'].extend(matches)

        if details['has_guarantees']:
            unique_phrases = list(set(details['guarantee_phrases']))
            details['warnings'].append(f"Risky guarantee language: {', '.join(unique_phrases[:3])}")

            # Progressive penalty based on count
            count = len(unique_phrases)
            if count == 1:
                return (-5, details)  # Minor
            elif count <= 3:
                return (-10, details)  # Moderate
            else:
                return (-15, details)  # Severe

        return (0, details)  # No penalty

    def _score_disclaimer_presence(self, text: str) -> Tuple[int, Dict]:
        """Score presence of legal disclaimer"""
        details = {'has_disclaimer': False, 'disclaimer_phrases': []}

        for pattern in self.DISCLAIMER_PATTERNS:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                details['has_disclaimer'] = True
                details['disclaimer_phrases'].extend(matches)

        if not details['has_disclaimer']:
            return (-10, details)  # Full penalty

        return (0, details)  # No penalty

    def _score_to_grade(self, score: int) -> str:
        """Convert numerical score to letter grade"""
        if score >= 90:
            return "A+ (Excellent)"
        elif score >= 85:
            return "A (Very Good)"
        elif score >= 80:
            return "B+ (Good)"
        elif score >= 75:
            return "B (Acceptable)"
        elif score >= 70:
            return "C (Marginal)"
        else:
            return "F (Unacceptable)"


# Global instance
accuracy_scorer = LegalAccuracyScorer()


# Standalone scoring function
def score_legal_response(response_text: str, expected_act: str = None, section_validator=None) -> Dict:
    """
    Convenience function to score a legal response

    Args:
        response_text: The AI-generated response
        expected_act: Optional Act code that should be cited
        section_validator: SectionValidator instance for section validation

    Returns:
        Scoring results with action recommendation
    """
    scorer = LegalAccuracyScorer(section_validator=section_validator)
    return scorer.score_response(response_text, expected_act)
