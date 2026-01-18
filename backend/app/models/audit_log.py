"""
Audit Log Models for Regulator/Bar Council Compliance
Immutable audit trail of all AI interactions
"""

from datetime import datetime
from sqlalchemy import Column, String, DateTime, Boolean, Integer, Text, JSON
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.core.database import Base


class AIAuditLog(Base):
    """
    Audit log for all AI query-response interactions

    Purpose:
    - Bar Council compliance
    - Regulator defense
    - Tamper-proof audit trail
    """
    __tablename__ = "ai_audit_logs"

    # Primary key
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    # Timestamp (immutable)
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)

    # User information
    user_id = Column(String, index=True)
    user_email = Column(String)
    user_ip = Column(String)

    # Query details
    query_text = Column(Text, nullable=False)
    query_type = Column(String)  # research, drafting, case_search, etc.
    query_classification = Column(JSON)  # Full classification details

    # AI Model details
    model_provider = Column(String)  # gemini, anthropic, openrouter
    model_id = Column(String)
    model_tier = Column(String)  # free, budget, balanced, premium

    # Response details
    response_text = Column(Text, nullable=False)
    response_hash = Column(String, nullable=False)  # SHA-256 hash for tamper detection

    # Citations & Validation
    sections_cited = Column(JSON)  # List of sections cited
    citations_valid = Column(Boolean, default=True)
    validation_score = Column(Integer)  # 0-100
    foreign_law_detected = Column(Boolean, default=False)
    risky_language_detected = Column(Boolean, default=False)

    # Disclaimers & Safety
    disclaimers_added = Column(JSON)  # List of disclaimer types added
    prompt_version = Column(String)  # Version of system prompt used

    # Cost tracking
    tokens_used = Column(Integer)
    cost_estimate = Column(String)  # In INR

    # Failover info
    failover_attempts = Column(Integer, default=1)
    models_tried = Column(JSON)  # List of models attempted

    # Metadata
    session_id = Column(String, index=True)
    request_id = Column(String)
    api_endpoint = Column(String)

    # Flags
    is_template_based = Column(Boolean, default=False)
    template_id = Column(String)

    def __repr__(self):
        return f"<AIAuditLog(id={self.id}, timestamp={self.timestamp}, model={self.model_id})>"


class TemplateUsageLog(Base):
    """
    Audit log for template usage
    """
    __tablename__ = "template_usage_logs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)

    # User
    user_id = Column(String, index=True)
    user_email = Column(String)

    # Template details
    template_id = Column(String, nullable=False, index=True)
    template_name = Column(String)
    template_category = Column(String)

    # Input fields
    fields_filled = Column(JSON)  # User inputs

    # Output
    generated_document_hash = Column(String)

    # Court/Act context
    court_type = Column(String)  # District, High Court, Supreme Court
    act_type = Column(String)  # IPC, CrPC, NI Act, etc.

    # Metadata
    session_id = Column(String)

    def __repr__(self):
        return f"<TemplateUsageLog(id={self.id}, template={self.template_id})>"


class ValidationLog(Base):
    """
    Audit log for section validation checks
    """
    __tablename__ = "validation_logs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)

    # Source
    source_type = Column(String)  # ai_response, user_document, template
    source_id = Column(String, index=True)

    # Validation results
    total_citations = Column(Integer, default=0)
    valid_citations = Column(Integer, default=0)
    invalid_citations = Column(JSON)

    # Scores
    accuracy_score = Column(Integer)  # 0-100

    # Flags
    has_foreign_law = Column(Boolean, default=False)
    has_risky_language = Column(Boolean, default=False)

    # Details
    validation_details = Column(JSON)

    def __repr__(self):
        return f"<ValidationLog(id={self.id}, score={self.accuracy_score})>"


class AccuracyScoreLog(Base):
    """
    Audit log for legal accuracy scoring (Phase 3)
    Tracks quality scores for AI-generated legal responses
    """
    __tablename__ = "accuracy_score_logs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)

    # Source
    source_type = Column(String)  # ai_response, template, user_text
    source_id = Column(String, index=True)

    # Overall score
    total_score = Column(Integer, nullable=False)  # 0-100
    max_score = Column(Integer, default=100)
    percentage = Column(Integer)
    grade = Column(String)  # A+, A, B+, B, C, F

    # Dimension scores
    statute_citation_score = Column(Integer)  # Max 30
    section_validity_score = Column(Integer)  # Max 30
    no_foreign_law_score = Column(Integer)  # Max 15
    no_guarantee_score = Column(Integer)  # Max 15
    disclaimer_score = Column(Integer)  # Max 10

    # Enforcement action
    action = Column(String)  # SHOW_NORMAL, SHOW_WITH_WARNING, BLOCK_OR_REGENERATE
    action_message = Column(String)
    is_safe_to_show = Column(Boolean, default=True)

    # Details
    score_breakdown = Column(JSON)  # Full breakdown with details
    warnings = Column(JSON)  # List of warnings
    errors = Column(JSON)  # List of errors

    # Expected vs Actual
    expected_act = Column(String)  # Expected Act that should be cited
    acts_cited = Column(JSON)  # List of Acts actually cited

    # Linked audit log
    ai_audit_log_id = Column(String, index=True)
    validation_log_id = Column(String, index=True)

    def __repr__(self):
        return f"<AccuracyScoreLog(id={self.id}, score={self.total_score}, grade={self.grade})>"


class CaseLawLog(Base):
    """
    Audit log for case-law citations (Phase 3)
    Tracks extracted case citations and validation
    """
    __tablename__ = "caselaw_logs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)

    # Source
    source_type = Column(String)  # ai_response, template, user_document
    source_id = Column(String, index=True)

    # Citations extracted
    total_citations = Column(Integer, default=0)
    valid_citations = Column(Integer, default=0)
    invalid_citations = Column(JSON)

    # Citation types
    landmark_count = Column(Integer, default=0)
    supreme_court_count = Column(Integer, default=0)
    high_court_count = Column(Integer, default=0)

    # Courts cited
    courts_cited = Column(JSON)  # List of court names

    # Landmark cases
    landmark_cases_cited = Column(JSON)  # List of landmark case names

    # Full citation details
    citations = Column(JSON)  # All extracted citations with metadata

    # Validation
    citation_accuracy_score = Column(Integer)  # 0-100
    has_landmark_cases = Column(Boolean, default=False)

    # Linked audit log
    ai_audit_log_id = Column(String, index=True)

    def __repr__(self):
        return f"<CaseLawLog(id={self.id}, citations={self.total_citations})>"
