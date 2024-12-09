# integration_test.py
import threading
import time
from server import app, translation_server
from client import VideoTranslationClient
import logging

def test_video_translation_workflow():
    """
    Comprehensive integration test for video translation workflow.
    """
    # Configure logging
    logging.basicConfig(
        level=logging.INFO, 
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)

    # Configure server for test
    translation_server.min_delay = 2
    translation_server.max_delay = 5
    translation_server.error_probability = 0.05

    # Start Flask server in a separate thread
    def run_server():
        app.run(port=5000)

    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()

    # Give server a moment to start
    time.sleep(1)

    try:
        # Create client
        client = VideoTranslationClient('http://localhost:5000')

        # Create job
        job_creation = client.create_job()
        job_id = job_creation['job_id']
        logger.info(f"Created job: {job_id}")

        # Wait for job completion
        for attempt in range(3):  # Retry up to 3 times
            try:
                result = client.wait_for_result(job_id)
                logger.info(f"Job completed: {result}")
                break  # Exit loop on success
            except RuntimeError as e:
                logger.warning(f"Job attempt {attempt + 1} failed: {e}")
                if attempt == 2:  # On the last attempt, log as a failure
                    logger.error("Job ultimately failed.")
        # Print job metrics
        print("\nJob Metrics:")
        print(client.metrics.get_summary())

    except Exception as e:
        logger.error(f"Test failed: {e}")
        raise

if __name__ == '__main__':
    test_video_translation_workflow()