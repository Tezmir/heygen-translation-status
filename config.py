# config.py
from dataclasses import dataclass, field
from typing import Optional, Dict, Any

@dataclass
class TranslationJobConfig:
    """
    Comprehensive configuration for video translation jobs.
    
    Attributes:
        max_retries (int): Maximum number of retry attempts
        timeout (float): Total timeout for job processing
        retry_strategy (str): Retry approach (exponential, linear)
        callback_url (Optional[str]): Webhook URL for job updates
        priority (int): Job priority (0-10)
        metadata (Dict[str, Any]): Additional job-specific metadata
    """
    max_retries: int = 10
    timeout: float = 60.0
    retry_strategy: str = 'exponential'
    callback_url: Optional[str] = None
    priority: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)

    def validate(self):
        """
        Validate configuration parameters.
        
        Raises:
            ValueError: If configuration parameters are invalid
        """
        if self.max_retries < 0:
            raise ValueError("Retries cannot be negative")
        if self.timeout <= 0:
            raise ValueError("Timeout must be positive")
        if self.priority < 0 or self.priority > 10:
            raise ValueError("Priority must be between 0 and 10")