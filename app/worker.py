from logging import config
import subprocess
import time

from app.database import SessionLocal
from app.models import Job
from app.config import load_config

WORKER_RUNNING = True


def run_worker():
    global WORKER_RUNNING

    if not WORKER_RUNNING:
     print("Worker stopped.")
     return
    config = load_config()

    BASE_DELAY = config["backoff_base"]
    MAX_RETRIES = config["max_retries"]


    db = SessionLocal()

    job = (
    db.query(Job)
    .filter(Job.state == "pending", Job.locked == 0)
    .first()
)

    if not job:
        print("No pending jobs.")
        db.close()
        return
    
    job.state = "processing"
    job.locked = 1
    db.commit()

    print(f"Running Job: {job.id}")

    result = subprocess.run(job.command, shell=True)

    if result.returncode == 0:
        job.state = "completed"
        job.locked = 0
        print("Job Completed Successfully!")

    else:
        job.attempts += 1

        if job.attempts >= MAX_RETRIES:
            job.state = "dead"
            job.locked = 0
            print("Job moved to Dead Letter Queue.")
        else:
            delay = BASE_DELAY ** job.attempts
            print(f"Retrying in {delay} seconds...")

            time.sleep(delay)

            job.state = "pending"
            job.locked = 0

    db.commit()
    db.close()