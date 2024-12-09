# metrics.py
import time
from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class TranslationMetrics:
    """
    Comprehensive metrics tracking for translation jobs.
    
    Provides insights into job performance, success rates, and processing times.
    """
    total_jobs: int = 0
    successful_jobs: int = 0
    failed_jobs: int = 0
    total_processing_time: float = 0.0
    job_durations: List[float] = field(default_factory=list)
    status_distribution: Dict[str, int] = field(default_factory=lambda: {
        'pending': 0, 
        'completed': 0, 
        'error': 0
    })

    def record_job(self, status: str, processing_time: float):
        """
        Record metrics for a completed job.
        
        Args:
            status (str): Final status of the job
            processing_time (float): Time taken to process the job
        """
        self.total_jobs += 1
        self.job_durations.append(processing_time)
        self.total_processing_time += processing_time
        
        self.status_distribution[status] += 1
        
        if status == 'completed':
            self.successful_jobs += 1
        else:
            self.failed_jobs += 1

    def get_summary(self):
        """
        Generate a comprehensive metrics summary.
        
        Returns:
            Dict: Detailed metrics report
        """
        return {
            'total_jobs': self.total_jobs,
            'successful_jobs': self.successful_jobs,
            'failed_jobs': self.failed_jobs,
            'success_rate': self.successful_jobs / self.total_jobs if self.total_jobs > 0 else 0,
            'avg_processing_time': self.total_processing_time / self.total_jobs if self.total_jobs > 0 else 0,
            'min_processing_time': min(self.job_durations) if self.job_durations else 0,
            'max_processing_time': max(self.job_durations) if self.job_durations else 0,
            'status_distribution': self.status_distribution
        }