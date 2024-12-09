# client.py
import requests
import time
import logging
from typing import Dict, Any, Optional

from config import TranslationJobConfig
from metrics import TranslationMetrics
from tracing import DistributedTraceContext
from audit_logger import AuditLogger
from rate_limiter import RateLimiter

class VideoTranslationClient:
    def __init__(
        self, 
        base_url: str, 
        config: Optional[TranslationJobConfig] = None,
        metrics: Optional[TranslationMetrics] = None,
        audit_logger: Optional[AuditLogger] = None
    ):
        """
        Advanced video translation job client.
        
        Args:
            base_url: Base URL of translation server
            config: Job configuration
            metrics: Metrics tracking object
            audit_logger: Audit logging system
        """
        self.base_url = base_url
        self.config = config or TranslationJobConfig()
        self.metrics = metrics or TranslationMetrics()
        self.audit_logger = audit_logger or AuditLogger()
        self.logger = logging.getLogger(__name__)
        
        # Configure logging
        logging.basicConfig(
            level=logging.INFO, 
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

    @RateLimiter(max_calls=5, period=1.0)
    def create_job(self) -> Dict[str, str]:
        """
        Create a new translation job.
        
        Returns:
            Dict containing job details
        """
        # Create trace context
        trace_context = DistributedTraceContext()
        create_span = trace_context.create_span('job_creation')

        try:
            response = requests.post(f"{self.base_url}/job", 
                                     json=self.config.metadata)
            response.raise_for_status()
            job_id = response.json()['job_id']

            # End span and log event
            trace_context.end_span('job_creation', 
                                   {'job_id': job_id})
            
            self.audit_logger.log_event(
                'job_created', 
                job_id, 
                {'metadata': self.config.metadata}
            )

            return {'job_id': job_id}

        except requests.RequestException as e:
            self.logger.error(f"Job creation failed: {e}")
            raise

    def wait_for_result(self, job_id: str) -> Dict[str, Any]:
        """
        Wait for job completion with intelligent polling.
        
        Args:
            job_id: Unique job identifier
        
        Returns:
            Dict containing final job result
        """
        start_time = time.time()
        attempts = 0
        trace_context = DistributedTraceContext()
        polling_span = trace_context.create_span('job_polling')

        while time.time() - start_time < self.config.timeout:
            try:
                response = requests.get(f"{self.base_url}/status/{job_id}")
                response.raise_for_status()
                status = response.json()

                # Log and track metrics
                self.metrics.record_job(
                    status['result'], 
                    time.time() - start_time
                )
                
                # Audit logging
                self.audit_logger.log_event(
                    f'job_status_{status["result"]}', 
                    job_id
                )

                # Check job status
                if status['result'] == 'completed':
                    trace_context.end_span('job_polling', 
                                           {'final_status': 'completed'})
                    return status

                if status['result'] == 'error':
                    trace_context.end_span('job_polling', 
                                           {'final_status': 'error'})
                    raise RuntimeError(f"Job failed: {status.get('message', 'Unknown error')}")

                # Exponential backoff
                attempts += 1
                wait_time = min(2 ** attempts, 30)
                time.sleep(wait_time)

            except requests.RequestException as e:
                self.logger.warning(f"Status check failed: {e}")
                
                if attempts >= self.config.max_retries:
                    break

        # Timeout reached
        raise RuntimeError("Job processing timed out")

# Example usage function
def run_translation_job():
    """
    Demonstration of how to use the advanced translation client.
    """
    client = VideoTranslationClient('http://localhost:5000')
    
    try:
        # Create job
        job_creation = client.create_job()
        job_id = job_creation['job_id']
        
        # Wait for result
        result = client.wait_for_result(job_id)
        
        print(f"Job completed: {result}")
        
        # Optional: print metrics
        print("\nJob Metrics:")
        print(client.metrics.get_summary())
        
    except Exception as e:
        print(f"Translation job failed: {e}")

if __name__ == '__main__':
    run_translation_job()