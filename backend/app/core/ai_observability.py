"""
AI Observability and Tracing for LegalMitra

Provides structured logging and tracing for AI requests to support:
- Performance monitoring
- Cost tracking
- Error debugging
- SOC-2 / ISO-27001 compliance
"""

import time
import logging
import uuid
from typing import Optional, Callable, Tuple
from functools import wraps

logger = logging.getLogger("legalmitra.ai")


def ai_trace(query: str, provider: str, query_type: str = "research") -> Tuple[str, Callable]:
    """
    Create a trace for an AI request.
    
    Args:
        query: The user query
        provider: AI provider name (gemini, openai, etc.)
        query_type: Type of query (research, drafting, etc.)
    
    Returns:
        Tuple of (trace_id, end_function)
        
    Usage:
        trace_id, end = ai_trace(query, "gemini", "research")
        try:
            response = ai_client.generate_content(prompt)
            end(success=True)
        except Exception as e:
            end(success=False, error=str(e))
            raise
    """
    trace_id = str(uuid.uuid4())[:8]  # Short ID for logs
    start = time.time()
    
    logger.info(
        "AI request started",
        extra={
            "trace_id": trace_id,
            "provider": provider,
            "query_type": query_type,
            "query_len": len(query),
            "query_preview": query[:100] if len(query) > 100 else query
        }
    )
    
    def end(success: bool = True, error: Optional[str] = None, model: Optional[str] = None, 
             tokens_used: Optional[int] = None, cost_estimate: Optional[float] = None):
        """
        End the trace and log completion.
        
        Args:
            success: Whether the request succeeded
            error: Error message if failed
            model: Model used (e.g., "gemini-1.5-flash")
            tokens_used: Number of tokens used (if available)
            cost_estimate: Estimated cost in USD (if available)
        """
        duration = round(time.time() - start, 3)
        log_level = logger.info if success else logger.error
        
        log_level(
            "AI request completed",
            extra={
                "trace_id": trace_id,
                "provider": provider,
                "query_type": query_type,
                "duration_sec": duration,
                "success": success,
                "error": error,
                "model": model,
                "tokens_used": tokens_used,
                "cost_estimate": cost_estimate
            }
        )
        
        # Also print for immediate visibility in logs
        status = "✅" if success else "❌"
        print(f"{status} AI [{trace_id}] {provider} {query_type} - {duration}s" + 
              (f" - {model}" if model else "") +
              (f" - ERROR: {error}" if error else ""))
    
    return trace_id, end


def trace_ai_request(provider: str, query_type: str = "research"):
    """
    Decorator to automatically trace AI service method calls.
    
    Usage:
        @trace_ai_request(provider="gemini", query_type="research")
        async def process_query(self, query: str):
            ...
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            # Extract query from args/kwargs
            query = kwargs.get('query') or (args[0] if args else "")
            trace_id, end = ai_trace(query, provider, query_type)
            
            try:
                result = await func(self, *args, **kwargs)
                end(success=True)
                return result
            except Exception as e:
                end(success=False, error=str(e))
                raise
        
        return wrapper
    return decorator
