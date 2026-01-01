"""
Document Storage Service
Handles storage and retrieval of uploaded documents (cases, news, etc.)
Uses file-based storage (JSON) for simplicity, can be upgraded to MongoDB later
"""

import json
import os
from typing import List, Dict, Optional
from datetime import datetime
from pathlib import Path
import logging
import time

logger = logging.getLogger(__name__)

# File locking (cross-platform)
try:
    if os.name == 'nt':  # Windows
        import msvcrt
        HAS_FILE_LOCKING = True
    else:  # Unix/Linux
        import fcntl
        HAS_FILE_LOCKING = True
except ImportError:
    HAS_FILE_LOCKING = False
    logger.warning("File locking not available - may have race conditions with concurrent requests")

# Storage directory
STORAGE_DIR = Path("data/documents")
STORAGE_DIR.mkdir(parents=True, exist_ok=True)

CASES_FILE = STORAGE_DIR / "cases.json"
NEWS_FILE = STORAGE_DIR / "news.json"
DOCUMENTS_FILE = STORAGE_DIR / "documents.json"


class DocumentStorage:
    """Service for storing and retrieving uploaded documents"""
    
    def __init__(self):
        self._ensure_files_exist()
    
    def _ensure_files_exist(self):
        """Ensure storage files exist"""
        for file_path in [CASES_FILE, NEWS_FILE, DOCUMENTS_FILE]:
            if not file_path.exists():
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump([], f, ensure_ascii=False, indent=2)
    
    def _lock_file(self, file_handle):
        """Lock file for exclusive access (cross-platform)"""
        if not HAS_FILE_LOCKING:
            return  # Skip locking if not available
        try:
            if os.name == 'nt':  # Windows
                msvcrt.locking(file_handle.fileno(), msvcrt.LK_NBLCK, 1)
            else:  # Unix/Linux
                fcntl.flock(file_handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except (IOError, OSError) as e:
            # File is locked by another process, wait and retry
            logger.debug(f"File is locked, will retry: {e}")
            raise
        except Exception as e:
            logger.warning(f"Could not lock file: {e}")
    
    def _unlock_file(self, file_handle):
        """Unlock file"""
        if not HAS_FILE_LOCKING:
            return
        try:
            if os.name == 'nt':  # Windows
                msvcrt.locking(file_handle.fileno(), msvcrt.LK_UNLCK, 1)
            else:  # Unix/Linux
                fcntl.flock(file_handle.fileno(), fcntl.LOCK_UN)
        except Exception:
            pass  # Ignore unlock errors
    
    def _load_json(self, file_path: Path) -> List[Dict]:
        """Load JSON data from file with error handling and retry"""
        max_retries = 3
        retry_delay = 0.1
        
        for attempt in range(max_retries):
            try:
                if not file_path.exists():
                    return []
                
                with open(file_path, 'r', encoding='utf-8') as f:
                    try:
                        self._lock_file(f)
                    except (IOError, OSError):
                        # File locked, wait a bit and retry
                        time.sleep(0.1)
                        continue
                    try:
                        data = json.load(f)
                        return data if isinstance(data, list) else []
                    finally:
                        self._unlock_file(f)
            except json.JSONDecodeError as e:
                logger.error(f"JSON decode error in {file_path} (attempt {attempt + 1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    # Try to backup corrupted file and create new one
                    try:
                        backup_path = file_path.with_suffix('.json.bak')
                        if file_path.exists():
                            import shutil
                            shutil.copy2(file_path, backup_path)
                        # Create empty file
                        with open(file_path, 'w', encoding='utf-8') as f:
                            json.dump([], f, ensure_ascii=False, indent=2)
                        logger.warning(f"Created new file after corruption detected. Backup saved to {backup_path}")
                        return []
                    except Exception as backup_error:
                        logger.error(f"Failed to recover from JSON corruption: {backup_error}")
                time.sleep(retry_delay * (attempt + 1))
            except Exception as e:
                logger.error(f"Error loading {file_path} (attempt {attempt + 1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay * (attempt + 1))
                else:
                    return []
        
        return []
    
    def _save_json(self, file_path: Path, data: List[Dict]):
        """Save JSON data to file with error handling and atomic write"""
        max_retries = 3
        retry_delay = 0.1
        
        for attempt in range(max_retries):
            try:
                # Atomic write: write to temp file first, then rename
                temp_path = file_path.with_suffix('.json.tmp')
                
                with open(temp_path, 'w', encoding='utf-8') as f:
                    self._lock_file(f)
                    try:
                        json.dump(data, f, ensure_ascii=False, indent=2)
                        f.flush()
                        os.fsync(f.fileno())  # Force write to disk
                    finally:
                        self._unlock_file(f)
                
                # Atomic rename (works on both Windows and Unix)
                if os.name == 'nt':  # Windows
                    # On Windows, rename might fail if file exists, so remove first
                    if file_path.exists():
                        os.remove(file_path)
                os.rename(temp_path, file_path)
                return  # Success
                
            except PermissionError as e:
                logger.error(f"Permission error saving {file_path} (attempt {attempt + 1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay * (attempt + 1))
                else:
                    raise
            except Exception as e:
                logger.error(f"Error saving {file_path} (attempt {attempt + 1}/{max_retries}): {e}")
                # Clean up temp file if it exists
                try:
                    if temp_path.exists():
                        os.remove(temp_path)
                except:
                    pass
                if attempt < max_retries - 1:
                    time.sleep(retry_delay * (attempt + 1))
                else:
                    raise
    
    async def save_document(
        self,
        filename: str,
        document_type: str,
        extracted_text: str,
        metadata: Optional[Dict] = None
    ) -> str:
        """
        Save an uploaded document with error handling
        
        Returns: document_id
        """
        try:
            documents = self._load_json(DOCUMENTS_FILE)
            
            # Generate unique document ID with timestamp and random component
            import random
            random_suffix = random.randint(1000, 9999)
            document_id = f"doc_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{random_suffix}"
            
            # Limit extracted text size to prevent huge files (max 1MB of text)
            max_text_length = 1000000  # ~1MB
            if len(extracted_text) > max_text_length:
                extracted_text = extracted_text[:max_text_length] + "\n\n[Text truncated due to size]"
                logger.warning(f"Document text truncated to {max_text_length} characters")
            
            document = {
                "id": document_id,
                "filename": filename or "unnamed_document",
                "document_type": document_type,
                "extracted_text": extracted_text,
                "metadata": metadata or {},
                "created_at": datetime.now().isoformat(),
                "is_case": False,
                "is_news": False
            }
            
            # Try to detect if it's a case or news based on content
            # Use scoring system: document is case OR news, not both
            text_lower = extracted_text.lower()
            
            case_score = 0
            news_score = 0
            
            # Case keywords (stronger weight for legal case indicators)
            case_keywords = {
                "judgment": 3, "court": 2, "petitioner": 3, "respondent": 3, 
                "case": 2, "citation": 3, "supreme court": 4, "high court": 4,
                "judge": 2, "order": 2, "verdict": 3, "legal notice": 2,
                "plaintiff": 2, "defendant": 2, "writ petition": 4
            }
            
            # News keywords
            news_keywords = {
                "news": 2, "update": 2, "amendment": 3, "reform": 2,
                "notification": 3, "circular": 3, "ministry": 2,
                "government": 1, "gst": 2, "finance act": 3, "press release": 3
            }
            
            # Calculate scores
            for keyword, weight in case_keywords.items():
                if keyword in text_lower:
                    case_score += weight
            
            for keyword, weight in news_keywords.items():
                if keyword in text_lower:
                    news_score += weight
            
            # Assign to category with higher score (with minimum threshold)
            if case_score >= 3 and case_score >= news_score:
                document["is_case"] = True
                document["is_news"] = False
            elif news_score >= 3 and news_score > case_score:
                document["is_news"] = True
                document["is_case"] = False
            # If scores are too low or equal, don't mark as either (will appear in both as fallback)
            
            documents.append(document)
            self._save_json(DOCUMENTS_FILE, documents)
            
            logger.info(f"Saved document {document_id}: {filename} (type: {document_type})")
            return document_id
        except Exception as e:
            logger.error(f"Failed to save document {filename}: {e}", exc_info=True)
            # Return a temporary ID even if save fails, so the request doesn't completely fail
            return f"doc_temp_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            documents.append(document)
            self._save_json(DOCUMENTS_FILE, documents)
            
            logger.info(f"Saved document {document_id}: {filename} (type: {document_type})")
            return document_id
        except Exception as e:
            logger.error(f"Failed to save document {filename}: {e}", exc_info=True)
            # Return a temporary ID even if save fails, so the request doesn't completely fail
            return f"doc_temp_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    async def get_recent_cases(self, limit: int = 5) -> List[Dict]:
        """Get recent cases from uploaded documents with error handling"""
        try:
            documents = self._load_json(DOCUMENTS_FILE)
            
            if not documents:
                return []
            
            # Filter for cases - only documents explicitly marked as cases
            # Exclude documents that are marked as news (to avoid duplicates)
            cases = [
                doc for doc in documents
                if isinstance(doc, dict) and doc.get("is_case", False) and not doc.get("is_news", False)
            ]
            
            # If no explicit cases found, include PDFs that aren't marked as news
            if not cases:
                cases = [
                    doc for doc in documents
                    if isinstance(doc, dict) and doc.get("document_type") == "pdf" and not doc.get("is_news", False)
                ]
            
            # Sort by created_at (most recent first) with error handling
            def safe_sort_key(x):
                try:
                    created_at = x.get("created_at", "")
                    if created_at:
                        return created_at
                    return ""
                except:
                    return ""
            
            cases.sort(key=safe_sort_key, reverse=True)
            
            # Convert to CaseItem format
            result = []
            for case in cases[:limit]:
                try:
                    # Extract title from filename or first line of text
                    title = case.get("filename", "Uploaded Case Document") or "Uploaded Case Document"
                    if title.endswith(('.pdf', '.doc', '.docx', '.txt')):
                        title = title.rsplit('.', 1)[0]
                    
                    text = case.get("extracted_text", "")
                    if text:
                        # Use first 300 chars as summary
                        summary = text[:300] + "..." if len(text) > 300 else text
                    else:
                        summary = "Case document uploaded by user."
                    
                    # Safe date parsing
                    try:
                        created_at_str = case.get("created_at", datetime.now().isoformat())
                        year = datetime.fromisoformat(created_at_str).year
                    except:
                        year = datetime.now().year
                    
                    result.append({
                        "title": title[:200],  # Limit title length
                        "court": "Uploaded Document",
                        "year": year,
                        "citation": None,
                        "summary": summary[:500],  # Limit summary length
                        "query": f"Tell me about the case: {title[:100]}",
                        "source": "uploaded_document",
                        "document_id": case.get("id")
                    })
                except Exception as e:
                    logger.warning(f"Error processing case document: {e}")
                    continue
            
            return result
        except Exception as e:
            logger.error(f"Error getting recent cases: {e}", exc_info=True)
            return []
    
    async def get_recent_news(self, limit: int = 5) -> List[Dict]:
        """Get recent news from uploaded documents with error handling"""
        try:
            documents = self._load_json(DOCUMENTS_FILE)
            
            if not documents:
                return []
            
            # Filter for news - only documents explicitly marked as news
            # Exclude documents that are marked as cases (to avoid duplicates)
            news_items = [
                doc for doc in documents
                if isinstance(doc, dict) and doc.get("is_news", False) and not doc.get("is_case", False)
            ]
            
            # If no explicit news found, include non-PDF documents that aren't marked as cases
            if not news_items:
                news_items = [
                    doc for doc in documents
                    if isinstance(doc, dict) and doc.get("document_type") in ["word", "text"] and not doc.get("is_case", False)
                ]
            
            # Sort by created_at (most recent first) with error handling
            def safe_sort_key(x):
                try:
                    created_at = x.get("created_at", "")
                    if created_at:
                        return created_at
                    return ""
                except:
                    return ""
            
            news_items.sort(key=safe_sort_key, reverse=True)
            
            # Convert to NewsItem format
            result = []
            for news in news_items[:limit]:
                try:
                    # Extract title from filename or first line of text
                    title = news.get("filename", "Uploaded Legal Document") or "Uploaded Legal Document"
                    if title.endswith(('.pdf', '.doc', '.docx', '.txt')):
                        title = title.rsplit('.', 1)[0]
                    
                    text = news.get("extracted_text", "")
                    if text:
                        # Use first 300 chars as summary
                        summary = text[:300] + "..." if len(text) > 300 else text
                    else:
                        summary = "Legal document uploaded by user."
                    
                    # Safe date parsing
                    try:
                        created_at_str = news.get("created_at", datetime.now().isoformat())
                        created_at = datetime.fromisoformat(created_at_str)
                        date_str = created_at.strftime("%Y")
                    except:
                        date_str = str(datetime.now().year)
                    
                    result.append({
                        "title": title[:200],  # Limit title length
                        "source": "Uploaded Document",
                        "date": date_str,
                        "summary": summary[:500],  # Limit summary length
                        "query": f"Tell me more about: {title[:100]}",
                        "document_id": news.get("id")
                    })
                except Exception as e:
                    logger.warning(f"Error processing news document: {e}")
                    continue
            
            return result
        except Exception as e:
            logger.error(f"Error getting recent news: {e}", exc_info=True)
            return []
    
    async def search_documents(self, query: str, limit: int = 10) -> List[Dict]:
        """Search documents by query text"""
        documents = self._load_json(DOCUMENTS_FILE)
        
        query_lower = query.lower()
        results = []
        
        for doc in documents:
            text = doc.get("extracted_text", "").lower()
            filename = doc.get("filename", "").lower()
            
            if query_lower in text or query_lower in filename:
                results.append(doc)
        
        # Sort by relevance (simple: documents with query in title ranked higher)
        results.sort(key=lambda x: (
            query_lower not in x.get("filename", "").lower(),
            x.get("created_at", "")
        ))
        
        return results[:limit]


# Singleton instance
document_storage = DocumentStorage()

