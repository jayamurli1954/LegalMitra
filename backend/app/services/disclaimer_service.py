"""
Disclaimer Service for LegalMitra
Automatically adds Bar Council-safe legal disclaimers to AI responses
"""

import re
from typing import Dict, List
from enum import Enum


class DisclaimerType(Enum):
    """Types of disclaimers for different contexts"""
    GENERAL = "general"
    LEGAL_ADVICE = "legal_advice"
    DRAFTING = "drafting"
    CASE_LAW = "case_law"
    COMPLIANCE = "compliance"
    PREDICTION = "prediction"
    COURT_FILING = "court_filing"


class DisclaimerService:
    """Manages legal disclaimers for AI-generated content"""

    def __init__(self):
        # Define disclaimer templates
        self.disclaimers = {
            DisclaimerType.GENERAL: (
                "\n\n"
                "⚖️ **Disclaimer**: This is general legal information provided by LegalMitra AI. "
                "It does not constitute legal advice. For specific legal guidance, "
                "please consult a qualified advocate."
            ),

            DisclaimerType.LEGAL_ADVICE: (
                "\n\n"
                "⚖️ **Important Notice**: The information provided above is for educational "
                "and informational purposes only. It does not constitute legal advice, "
                "representation, or create an attorney-client relationship. "
                "Please consult a qualified legal professional for advice specific to your situation."
            ),

            DisclaimerType.DRAFTING: (
                "\n\n"
                "📄 **Drafting Disclaimer**: This is an AI-assisted draft and must be reviewed "
                "and finalized by a qualified advocate before use. It is meant as a starting point "
                "and may require modifications based on your specific facts and circumstances. "
                "Do not file or use this document without professional legal review."
            ),

            DisclaimerType.CASE_LAW: (
                "\n\n"
                "📚 **Case Law Disclaimer**: Case law cited above is provided for reference. "
                "The applicability and interpretation of case law depends on specific facts "
                "and legal arguments. Please verify citations and consult a qualified advocate "
                "for case-specific legal analysis."
            ),

            DisclaimerType.COMPLIANCE: (
                "\n\n"
                "✅ **Compliance Disclaimer**: This compliance overview is based on general "
                "provisions of Indian law. Actual compliance requirements may vary based on "
                "specific circumstances, notifications, and circulars. Please verify with a "
                "qualified legal or compliance professional before taking action."
            ),

            DisclaimerType.PREDICTION: (
                "\n\n"
                "⚠️ **Outcome Disclaimer**: Any mention of possible outcomes, timelines, "
                "or procedural steps is for general information only. LegalMitra does not "
                "predict or guarantee court outcomes, case results, or judicial decisions. "
                "Every case depends on its specific facts and legal arguments."
            ),

            DisclaimerType.COURT_FILING: (
                "\n\n"
                "🏛️ **Court Filing Notice**: This document is AI-generated and intended "
                "as a draft only. It MUST be reviewed, verified, and finalized by a qualified "
                "advocate before filing with any court or authority. The filing advocate "
                "takes full responsibility for the accuracy and appropriateness of the final document."
            ),
        }

        # Risk patterns that trigger specific disclaimers
        self.risk_patterns = {
            DisclaimerType.LEGAL_ADVICE: [
                r'\byou should\b', r'\byou must\b', r'\bI recommend\b',
                r'\bmy advice\b', r'\badvised to\b', r'\bsuggested to\b'
            ],
            DisclaimerType.PREDICTION: [
                r'\bguarantee\b', r'\bwill definitely\b', r'\b100%\b',
                r'\bcourt will\b', r'\bjudge will\b', r'\bcertain to win\b',
                r'\bsure to succeed\b', r'\bguaranteed outcome\b'
            ],
            DisclaimerType.DRAFTING: [
                r'\bdraft\b', r'\bnotice\b', r'\bagreement\b', r'\bpetition\b',
                r'\bapplication\b', r'\baffidavit\b', r'\bcontract\b'
            ],
            DisclaimerType.CASE_LAW: [
                r'\bv\.\s', r'\bvs\.\s', r'\bversus\b', r'\bAIR\b', r'\bSCC\b',
                r'\bjudgment\b', r'\bjudgement\b', r'\bheld that\b', r'\bobserved that\b'
            ],
            DisclaimerType.COMPLIANCE: [
                r'\bcompliance\b', r'\bfiling requirement\b', r'\bmandatory to\b',
                r'\brequired to file\b', r'\bstatutory\b', r'\bregulation\b'
            ],
        }

    def add_disclaimers(self, response: str, query_type: str = "research") -> str:
        """
        Add appropriate disclaimers to AI response

        Args:
            response: The AI-generated response
            query_type: Type of query (research, drafting, case_search, etc.)

        Returns:
            Response with appropriate disclaimers appended
        """
        disclaimers_to_add = []

        # Always add general disclaimer
        disclaimers_to_add.append(DisclaimerType.GENERAL)

        # Check for risk patterns and add specific disclaimers
        response_lower = response.lower()

        for disclaimer_type, patterns in self.risk_patterns.items():
            for pattern in patterns:
                if re.search(pattern, response_lower):
                    if disclaimer_type not in disclaimers_to_add:
                        disclaimers_to_add.append(disclaimer_type)
                    break

        # Add query-type specific disclaimers
        if query_type == "drafting" or query_type == "draft_document":
            if DisclaimerType.DRAFTING not in disclaimers_to_add:
                disclaimers_to_add.append(DisclaimerType.DRAFTING)

        if query_type == "case_search":
            if DisclaimerType.CASE_LAW not in disclaimers_to_add:
                disclaimers_to_add.append(DisclaimerType.CASE_LAW)

        # Build final response with disclaimers
        result = response

        # Remove GENERAL if more specific ones are present
        if len(disclaimers_to_add) > 1 and DisclaimerType.GENERAL in disclaimers_to_add:
            disclaimers_to_add.remove(DisclaimerType.GENERAL)

        # Add all applicable disclaimers
        for disclaimer_type in disclaimers_to_add:
            result += self.disclaimers[disclaimer_type]

        return result

    def get_disclaimer_text(self, disclaimer_type: DisclaimerType) -> str:
        """Get specific disclaimer text"""
        return self.disclaimers.get(disclaimer_type, self.disclaimers[DisclaimerType.GENERAL])

    def check_risks(self, response: str) -> Dict[str, List[str]]:
        """
        Check response for risky language patterns

        Returns:
            Dict mapping disclaimer types to matched patterns
        """
        risks = {}
        response_lower = response.lower()

        for disclaimer_type, patterns in self.risk_patterns.items():
            matched = []
            for pattern in patterns:
                if re.search(pattern, response_lower):
                    matched.append(pattern)

            if matched:
                risks[disclaimer_type.value] = matched

        return risks

    def sanitize_response(self, response: str) -> str:
        """
        Sanitize response by replacing overly confident language

        Returns:
            Sanitized response with softened language
        """
        replacements = {
            r'\byou must\b': 'you may need to',
            r'\byou should\b': 'you may consider',
            r'\bguaranteed\b': 'typically expected',
            r'\b100% certain\b': 'generally',
            r'\bwill definitely\b': 'may likely',
            r'\bI guarantee\b': 'it is generally expected',
            r'\bcourt will\b': 'court may',
            r'\bjudge will\b': 'judge may',
        }

        sanitized = response
        for pattern, replacement in replacements.items():
            sanitized = re.sub(pattern, replacement, sanitized, flags=re.IGNORECASE)

        return sanitized


# Singleton instance
disclaimer_service = DisclaimerService()
