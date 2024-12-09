# HeyGen Video Translation Client and Server

This project contains a server and client library for simulating HeyGen's video translation system. It demonstrates efficient polling, error handling, logging, and metrics tracking.

## Features

### Server (`server.py`)
- Simulates video translation jobs with random delays and error probabilities.
- Provides a `/status` API that returns `pending`, `completed`, or `error`.

### Client Library (`client.py`)
- Efficient polling mechanism using **exponential backoff** to avoid frequent requests.
- Implements **audit logging** to track job lifecycle events in a structured format.
- Tracks **job performance metrics** like success rates and processing times.
- Includes **rate limiting** to prevent overloading the server.

### Integration Test (`integration_test.py`)
- Demonstrates the end-to-end workflow:
  - Creates a translation job.
  - Polls the job's status until completion or failure.
  - Logs job events and displays detailed metrics.

## Quickstart Guide

### 1. Prerequisites
- Python 3.x installed on your system.
- Install dependencies using:
  ```bash
  pip install -r requirements.txt
  ```

### 2. Running the Server
Open a terminal and navigate to the project directory.
Start the server:
```bash
python server.py
```
The server will start at http://localhost:5000.

### 3. Using the Client Library
The client library provides an interface to interact with the server. This is an example of how to use the client library directly in a Python script. For a full demonstration of the workflow, run `integration_test.py` (see below).

#### Example Usage
```python
from client import VideoTranslationClient

# Initialize the client
client = VideoTranslationClient(base_url="http://localhost:5000")

# Create a new job
job_creation = client.create_job()
job_id = job_creation['job_id']
print(f"Created job with ID: {job_id}")

# Poll the job status
result = client.wait_for_result(job_id)
print(f"Job result: {result}")
```

#### Explanation
- **Create Job**: The `create_job()` method sends a request to start a translation job and returns the `job_id`.
- **Poll Status**: The `wait_for_result()` method polls the server for the job status until it's completed or encounters an error.

### 4. Running the Integration Test
Open another terminal (keep the server running).
Run the integration test:
```bash
python integration_test.py
```
The test will:
- Create a job on the server.
- Poll for its status.
- Display the result and metrics.

## Configuration

### Server (`server.py`)
- **Delay**: Configure `min_delay` and `max_delay` for job completion time.
- **Error Probability**: Adjust `error_probability` to simulate job failures.

### Client (`config.py`)
- **Retries**: Configure `max_retries` (default: 10).
- **Timeout**: Set timeout (default: 300 seconds).
- **Retry Strategy**: Choose exponential or other strategies.

## Example Metrics Output
Example output from the integration test:
```
Job Metrics:
{
  'total_jobs': 5, 
  'successful_jobs': 1, 
  'failed_jobs': 4, 
  'success_rate': 0.2, 
  'avg_processing_time': 4.85,
  'min_processing_time': 2, 
  'max_processing_time': 12, 
  'status_distribution': {
    'pending': 2, 
    'completed': 1, 
    'error': 2
  }
}
```

## File Structure
```
heygen-translation-status/
├── server.py               # Server implementation
├── client.py               # Client library
├── config.py               # Client configuration
├── metrics.py              # Metrics tracking
├── audit_logger.py         # Audit logging system
├── rate_limiter.py         # Rate limiter for client
├── tracing.py              # Distributed tracing context
├── integration_test.py     # Integration test script
├── requirements.txt        # Python dependencies
├── README.md               # Documentation
```
