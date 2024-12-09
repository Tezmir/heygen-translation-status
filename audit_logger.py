# audit_logger.py
import logging
import json
from typing import Dict, Any
from datetime import datetime

class AuditLogger:
    """
    Comprehensive audit logging system for tracking translation job events.
    
    Supports file-based logging with structured, JSON-formatted entries.
    """
    def __init__(self, log_file: str = 'translation_audit.jsonl'):
        """
        Initialize audit logger.
        
        Args:
            log_file (str): Path to the audit log file
        """
        self.log_file = log_file
        self.logger = logging.getLogger('audit_logger')
        self.logger.setLevel(logging.INFO)
        
        # JSON Line format handler
        handler = logging.FileHandler(log_file)
        self.logger.addHandler(handler)

    def log_event(self, 
                  event_type: str, 
                  job_id: str, 
                  details: Dict[str, Any] = None
    ):
        """
        Log a structured audit event.
        
        Args:
            event_type (str): Type of event (e.g., 'job_started', 'job_completed')
            job_id (str): Unique identifier for the job
            details (Dict, optional): Additional event details
        """
        log_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'event_type': event_type,
            'job_id': job_id,
            'details': details or {}
        }
        
        self.logger.info(json.dumps(log_entry))