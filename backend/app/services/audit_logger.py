"""
Enhanced Audit Logging Service
Immutable audit trail for Bar Council / Regulator compliance
"""

import hashlib
import logging
from datetime import datetime
from typing import Dict, Optional, Any
from sqlalchemy.orm import Session

from app.models.audit_log import (
    AIAuditLog, TemplateUsageLog, ValidationLog,
    AccuracyScoreLog, CaseLawLog  # Phase 3 additions
)
from app.core.database import get_db

logger = logging.getLogger(__name__)


class AuditLoggerService:
    """Enhanced audit logging for legal AI interactions"""

    @staticmethod
    def hash_text(text: str) -> str:
        """Create SHA-256 hash for tamper detection"""
        return hashlib.sha256(text.encode('utf-8')).hexdigest()

    @staticmethod
    async def log_ai_interaction(
        query: str,
        response: str,
        model_info: Dict,
        classification: Dict,
        validation_info: Optional[Dict] = None,
        user_info: Optional[Dict] = None,
        failover_info: Optional[Dict] = None,
        cost_info: Optional[Dict] = None,
        disclaimers: Optional[list] = None
    ) -> str:
        """
        Log AI query-response interaction

        Returns:
            log_id (str)
        """
        try:
            # Create response hash
            response_hash = AuditLoggerService.hash_text(response)

            # Prepare log entry
            log_entry = AIAuditLog(
                timestamp=datetime.utcnow(),

                # User info
                user_id=user_info.get('user_id') if user_info else None,
                user_email=user_info.get('email') if user_info else None,
                user_ip=user_info.get('ip') if user_info else None,

                # Query
                query_text=query,
                query_type=classification.get('query_type'),
                query_classification=classification,

                # Model
                model_provider=model_info.get('provider'),
                model_id=model_info.get('model_id'),
                model_tier=model_info.get('tier'),

                # Response
                response_text=response,
                response_hash=response_hash,

                # Validation
                sections_cited=validation_info.get('citations') if validation_info else None,
                citations_valid=validation_info.get('is_valid', True) if validation_info else True,
                validation_score=validation_info.get('accuracy_score') if validation_info else None,
                foreign_law_detected=validation_info.get('has_foreign_law', False) if validation_info else False,
                risky_language_detected=validation_info.get('has_risky_language', False) if validation_info else False,

                # Disclaimers
                disclaimers_added=disclaimers,

                # Cost
                tokens_used=cost_info.get('tokens') if cost_info else None,
                cost_estimate=str(cost_info.get('cost')) if cost_info else None,

                # Failover
                failover_attempts=failover_info.get('attempts', 1) if failover_info else 1,
                models_tried=failover_info.get('models_tried') if failover_info else [model_info.get('model_id')],

                # Session
                session_id=user_info.get('session_id') if user_info else None,
                request_id=user_info.get('request_id') if user_info else None,
                api_endpoint=user_info.get('endpoint') if user_info else None
            )

            # Save to database
            db: Session = next(get_db())
            db.add(log_entry)
            db.commit()
            db.refresh(log_entry)

            logger.info(f"AI interaction logged: {log_entry.id}")
            return log_entry.id

        except Exception as e:
            logger.error(f"Failed to log AI interaction: {e}")
            # Don't fail the request if logging fails
            return None

    @staticmethod
    async def log_template_usage(
        template_id: str,
        template_name: str,
        category: str,
        fields: Dict,
        generated_doc_hash: str,
        user_info: Optional[Dict] = None,
        context: Optional[Dict] = None
    ) -> str:
        """
        Log template usage

        Returns:
            log_id (str)
        """
        try:
            log_entry = TemplateUsageLog(
                timestamp=datetime.utcnow(),

                user_id=user_info.get('user_id') if user_info else None,
                user_email=user_info.get('email') if user_info else None,

                template_id=template_id,
                template_name=template_name,
                template_category=category,

                fields_filled=fields,
                generated_document_hash=generated_doc_hash,

                court_type=context.get('court') if context else None,
                act_type=context.get('act') if context else None,

                session_id=user_info.get('session_id') if user_info else None
            )

            db: Session = next(get_db())
            db.add(log_entry)
            db.commit()
            db.refresh(log_entry)

            logger.info(f"Template usage logged: {log_entry.id}")
            return log_entry.id

        except Exception as e:
            logger.error(f"Failed to log template usage: {e}")
            return None

    @staticmethod
    async def log_validation(
        source_type: str,
        source_id: str,
        validation_results: Dict
    ) -> str:
        """
        Log section validation check

        Returns:
            log_id (str)
        """
        try:
            log_entry = ValidationLog(
                timestamp=datetime.utcnow(),

                source_type=source_type,
                source_id=source_id,

                total_citations=validation_results.get('total_citations', 0),
                valid_citations=validation_results.get('valid_citations', 0),
                invalid_citations=validation_results.get('invalid_citations', []),

                accuracy_score=int(validation_results.get('accuracy_score', 100)),

                has_foreign_law=validation_results.get('has_foreign_law', False),
                has_risky_language=validation_results.get('has_risky_language', False),

                validation_details=validation_results
            )

            db: Session = next(get_db())
            db.add(log_entry)
            db.commit()
            db.refresh(log_entry)

            logger.info(f"Validation logged: {log_entry.id}")
            return log_entry.id

        except Exception as e:
            logger.error(f"Failed to log validation: {e}")
            return None

    @staticmethod
    async def get_user_audit_trail(
        user_id: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        limit: int = 100
    ) -> list:
        """Get audit trail for a specific user"""
        try:
            db: Session = next(get_db())
            query = db.query(AIAuditLog).filter(AIAuditLog.user_id == user_id)

            if start_date:
                query = query.filter(AIAuditLog.timestamp >= start_date)
            if end_date:
                query = query.filter(AIAuditLog.timestamp <= end_date)

            logs = query.order_by(AIAuditLog.timestamp.desc()).limit(limit).all()

            return [
                {
                    'id': log.id,
                    'timestamp': log.timestamp.isoformat(),
                    'query_type': log.query_type,
                    'model': log.model_id,
                    'validation_score': log.validation_score,
                    'cost': log.cost_estimate
                }
                for log in logs
            ]

        except Exception as e:
            logger.error(f"Failed to get audit trail: {e}")
            return []

    @staticmethod
    async def verify_response_integrity(log_id: str, response_text: str) -> bool:
        """Verify that response hasn't been tampered with"""
        try:
            db: Session = next(get_db())
            log = db.query(AIAuditLog).filter(AIAuditLog.id == log_id).first()

            if not log:
                return False

            current_hash = AuditLoggerService.hash_text(response_text)
            return current_hash == log.response_hash

        except Exception as e:
            logger.error(f"Failed to verify integrity: {e}")
            return False

    @staticmethod
    async def get_audit_statistics(
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Dict:
        """Get aggregate audit statistics"""
        try:
            db: Session = next(get_db())
            query = db.query(AIAuditLog)

            if start_date:
                query = query.filter(AIAuditLog.timestamp >= start_date)
            if end_date:
                query = query.filter(AIAuditLog.timestamp <= end_date)

            total_queries = query.count()

            avg_validation_score = db.query(
                AIAuditLog.validation_score
            ).filter(
                AIAuditLog.validation_score.isnot(None)
            ).all()

            avg_score = sum([s[0] for s in avg_validation_score if s[0]]) / len(avg_validation_score) if avg_validation_score else 0

            foreign_law_count = query.filter(AIAuditLog.foreign_law_detected == True).count()
            risky_language_count = query.filter(AIAuditLog.risky_language_detected == True).count()

            return {
                'total_queries': total_queries,
                'average_validation_score': round(avg_score, 2),
                'foreign_law_detections': foreign_law_count,
                'risky_language_detections': risky_language_count,
                'period': {
                    'start': start_date.isoformat() if start_date else None,
                    'end': end_date.isoformat() if end_date else None
                }
            }

        except Exception as e:
            logger.error(f"Failed to get statistics: {e}")
            return {}

    @staticmethod
    async def log_accuracy_score(
        source_type: str,
        source_id: str,
        score_results: Dict,
        ai_audit_log_id: Optional[str] = None,
        validation_log_id: Optional[str] = None
    ) -> str:
        """
        Log legal accuracy score (Phase 3)

        Args:
            source_type: Type of source (ai_response, template, user_text)
            source_id: ID of source
            score_results: Results from accuracy scorer
            ai_audit_log_id: Optional linked AI audit log ID
            validation_log_id: Optional linked validation log ID

        Returns:
            log_id (str)
        """
        try:
            breakdown = score_results.get('breakdown', {})

            log_entry = AccuracyScoreLog(
                timestamp=datetime.utcnow(),

                source_type=source_type,
                source_id=source_id,

                # Overall score
                total_score=score_results.get('total_score'),
                max_score=score_results.get('max_score', 100),
                percentage=score_results.get('percentage'),
                grade=score_results.get('grade'),

                # Dimension scores
                statute_citation_score=breakdown.get('statute_citation', {}).get('score'),
                section_validity_score=breakdown.get('section_validity', {}).get('score'),
                no_foreign_law_score=breakdown.get('no_foreign_law', {}).get('score'),
                no_guarantee_score=breakdown.get('no_guarantee_language', {}).get('score'),
                disclaimer_score=breakdown.get('disclaimer_present', {}).get('score'),

                # Enforcement
                action=score_results.get('action'),
                action_message=score_results.get('action_message'),
                is_safe_to_show=score_results.get('is_safe_to_show', True),

                # Details
                score_breakdown=breakdown,
                warnings=score_results.get('warnings', []),
                errors=score_results.get('errors', []),

                # Expected vs Actual
                expected_act=score_results.get('expected_act'),
                acts_cited=breakdown.get('statute_citation', {}).get('details', {}).get('indian_laws_cited', []),

                # Links
                ai_audit_log_id=ai_audit_log_id,
                validation_log_id=validation_log_id
            )

            db: Session = next(get_db())
            db.add(log_entry)
            db.commit()
            db.refresh(log_entry)

            logger.info(f"Accuracy score logged: {log_entry.id} (score={log_entry.total_score})")
            return log_entry.id

        except Exception as e:
            logger.error(f"Failed to log accuracy score: {e}")
            return None

    @staticmethod
    async def log_caselaw_citations(
        source_type: str,
        source_id: str,
        caselaw_results: Dict,
        ai_audit_log_id: Optional[str] = None
    ) -> str:
        """
        Log case-law citations (Phase 3)

        Args:
            source_type: Type of source (ai_response, template, user_document)
            source_id: ID of source
            caselaw_results: Results from case-law extractor
            ai_audit_log_id: Optional linked AI audit log ID

        Returns:
            log_id (str)
        """
        try:
            citations = caselaw_results.get('citations', [])
            validation = caselaw_results.get('validation', {})
            summary = caselaw_results.get('summary', {})

            # Extract landmark cases
            landmark_cases = [
                c.get('citation') for c in citations
                if c.get('is_landmark', False)
            ]

            log_entry = CaseLawLog(
                timestamp=datetime.utcnow(),

                source_type=source_type,
                source_id=source_id,

                # Citations
                total_citations=validation.get('total_citations', 0),
                valid_citations=validation.get('valid_citations', 0),
                invalid_citations=validation.get('invalid_citations', []),

                # Types
                landmark_count=summary.get('landmark_count', 0),
                supreme_court_count=summary.get('supreme_court_count', 0),
                high_court_count=summary.get('high_court_count', 0),

                # Courts
                courts_cited=validation.get('courts_cited', []),

                # Landmark cases
                landmark_cases_cited=landmark_cases,

                # Full details
                citations=citations,

                # Validation
                citation_accuracy_score=int(validation.get('accuracy_score', 100)),
                has_landmark_cases=validation.get('has_landmark_cases', False),

                # Link
                ai_audit_log_id=ai_audit_log_id
            )

            db: Session = next(get_db())
            db.add(log_entry)
            db.commit()
            db.refresh(log_entry)

            logger.info(f"Case-law citations logged: {log_entry.id} (citations={log_entry.total_citations})")
            return log_entry.id

        except Exception as e:
            logger.error(f"Failed to log case-law citations: {e}")
            return None


# Singleton instance
audit_logger = AuditLoggerService()
