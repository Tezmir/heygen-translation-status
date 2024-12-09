# tracing.py
import uuid
import time
from dataclasses import dataclass, field
from typing import Optional, Dict

@dataclass
class DistributedTraceContext:
    """
    Comprehensive distributed tracing context for tracking job lifecycle.
    
    Provides unique identifiers and timing information for each job.
    """
    trace_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    parent_span_id: Optional[str] = None
    start_time: float = field(default_factory=time.time)
    spans: Dict[str, Dict] = field(default_factory=dict)

    def create_span(self, span_name: str):
        """
        Create a new span within the trace context.
        
        Args:
            span_name (str): Name of the current span
        
        Returns:
            Dict: Created span details
        """
        current_time = time.time()
        span = {
            'name': span_name,
            'start_time': current_time,
            'end_time': None,
            'duration': None,
            'metadata': {}
        }
        self.spans[span_name] = span
        return span

    def end_span(self, span_name: str, metadata: Optional[Dict] = None):
        """
        End a previously started span.
        
        Args:
            span_name (str): Name of the span to end
            metadata (Optional[Dict]): Additional metadata for the span
        """
        if span_name in self.spans:
            current_time = time.time()
            self.spans[span_name]['end_time'] = current_time
            self.spans[span_name]['duration'] = current_time - self.spans[span_name]['start_time']
            
            if metadata:
                self.spans[span_name]['metadata'].update(metadata)

    def to_dict(self):
        """
        Convert trace context to a dictionary representation.
        
        Returns:
            Dict: Comprehensive trace context details
        """
        return {
            'trace_id': self.trace_id,
            'parent_span_id': self.parent_span_id,
            'total_duration': time.time() - self.start_time,
            'spans': self.spans
        }