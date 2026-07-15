from app.database import SessionLocal
from app.models import Job


def enqueue_job(job_id, command):
    db = SessionLocal()

    job = Job(
        id=job_id,
        command=command,
        state="pending",
        attempts=0,
        max_retries=3
    )

    db.add(job)
    db.commit()
    db.close()

    print(f"Job '{job_id}' added successfully!")


def list_jobs():
    db = SessionLocal()

    jobs = db.query(Job).all()

    if not jobs:
        print("No jobs found.")
        db.close()
        return

    for job in jobs:
        print(
            f"ID: {job.id} | "
            f"Command: {job.command} | "
            f"State: {job.state} | "
            f"Attempts: {job.attempts}"
        )

    db.close()