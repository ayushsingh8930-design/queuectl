import subprocess

from app.database import SessionLocal
from app.models import Job


def run_worker():
    db = SessionLocal()

    job = db.query(Job).filter(Job.state == "pending").first()

    if not job:
        print("No pending jobs.")
        db.close()
        return

    print(f"Running Job: {job.id}")

    job.state = "processing"
    db.commit()

    result = subprocess.run(job.command, shell=True)

    if result.returncode == 0:
        job.state = "completed"
        print("Job Completed Successfully!")
    else:
        job.state = "failed"
        job.attempts += 1
        print("Job Failed!")

    db.commit()
    db.close()