import typer

from app.queue_manager import enqueue_job, list_jobs
from app.worker import run_worker

app = typer.Typer()

@app.command()
def enqueue(job_id: str, command: str):
    enqueue_job(job_id, command)

@app.command()
def status():
    print("QueueCTL is running!")

@app.command()
def list():
    list_jobs()

@app.command()
def worker():
    run_worker()