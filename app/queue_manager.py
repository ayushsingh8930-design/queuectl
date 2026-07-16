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

def queue_status():
    db = SessionLocal()

    pending = db.query(Job).filter(Job.state == "pending").count()
    processing = db.query(Job).filter(Job.state == "processing").count()
    completed = db.query(Job).filter(Job.state == "completed").count()
    failed = db.query(Job).filter(Job.state == "failed").count()
    dead = db.query(Job).filter(Job.state == "dead").count()

    print("\n===== Queue Status =====")
    print(f"Pending    : {pending}")
    print(f"Processing : {processing}")
    print(f"Completed  : {completed}")
    print(f"Failed     : {failed}")
    print(f"Dead       : {dead}")

    db.close()


def dlq_list():
    db = SessionLocal()

    jobs = db.query(Job).filter(Job.state == "dead").all()

    if not jobs:
        print("Dead Letter Queue is empty.")
        db.close()
        return

    print("\n===== Dead Letter Queue =====")

    for job in jobs:
        print(
            f"ID: {job.id} | "
            f"Command: {job.command} | "
            f"Attempts: {job.attempts}"
        )

    db.close()


def dlq_retry(job_id):
    db = SessionLocal()

    job = db.query(Job).filter(Job.id == job_id, Job.state == "dead").first()

    if not job:
        print("Job not found in DLQ.")
        db.close()
        return

    job.state = "pending"
    job.attempts = 0

    db.commit()
    db.close()

    print(f"Job '{job_id}' moved back to pending queue.")


def list_jobs_by_state(state):
    db = SessionLocal()

    jobs = db.query(Job).filter(Job.state == state).all()

    if not jobs:
        print(f"No jobs found in '{state}' state.")
        db.close()
        return

    print(f"\n===== {state.upper()} JOBS =====")

    for job in jobs:
        print(
            f"ID: {job.id} | "
            f"Command: {job.command} | "
            f"Attempts: {job.attempts}"
        )

    db.close()