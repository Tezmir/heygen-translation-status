# server.py
from flask import Flask, jsonify, request
import time
import random
import uuid
from typing import Dict, Any

class VideoTranslationServer:
    def __init__(
        self, 
        min_delay: int = 5, 
        max_delay: int = 30, 
        error_probability: float = 0.1
    ):
        """
        Advanced video translation server simulator.
        
        Args:
            min_delay: Minimum seconds before job completes
            max_delay: Maximum seconds before job completes
            error_probability: Probability of returning an error
        """
        self.jobs: Dict[str, Dict[str, Any]] = {}
        self.min_delay = min_delay
        self.max_delay = max_delay
        self.error_probability = error_probability

    def create_job(self) -> str:
        """
        Create a new translation job.
        
        Returns:
            str: Unique job ID
        """
        job_id = str(uuid.uuid4())
        self.jobs[job_id] = {
            'start_time': time.time(),
            'status': 'pending',
            'created_at': time.time()
        }
        return job_id

    def get_job_status(self, job_id: str) -> Dict[str, str]:
        """
        Get the current status of a job.
        
        Args:
            job_id: Unique identifier for the job
        
        Returns:
            Dict containing job status
        """
        if job_id not in self.jobs:
            return {'result': 'error', 'message': 'Job not found'}

        job = self.jobs[job_id]
        elapsed_time = time.time() - job['start_time']

        # Simulate potential error
        if random.random() < self.error_probability:
            job['status'] = 'error'
            return {'result': 'error', 'message': 'Translation failed'}

        # Check if job is complete
        if elapsed_time >= random.uniform(self.min_delay, self.max_delay):
            job['status'] = 'completed'
            return {'result': 'completed'}

        return {'result': 'pending'}

# Flask App Setup
app = Flask(__name__)
translation_server = VideoTranslationServer(min_delay=5, max_delay=10)

@app.route('/job', methods=['POST'])
def create_job():
    job_id = translation_server.create_job()
    return jsonify({'job_id': job_id}), 201

@app.route('/status/<job_id>', methods=['GET'])
def get_status(job_id):
    status = translation_server.get_job_status(job_id)
    return jsonify(status)

if __name__ == '__main__':
    app.run(port=5000)