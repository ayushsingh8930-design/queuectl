import typer

from app.queue_manager import (
    enqueue_job,
    list_jobs,
    list_jobs_by_state,
    queue_status,
    dlq_list,
    dlq_retry,
)
from app.worker import run_worker
from app.config import load_config, set_config

app = typer.Typer(help="QueueCTL")

worker_app = typer.Typer(help="Worker Commands")
dlq_app = typer.Typer(help="Dead Letter Queue")

app.add_typer(worker_app, name="worker")
app.add_typer(dlq_app, name="dlq")


@app.command()
def enqueue(job_id: str, command: str):
    enqueue_job(job_id, command)


@app.command()
def list(state: str = typer.Option(None, "--state")):
    if state:
        list_jobs_by_state(state)
    else:
        list_jobs()


@app.command()
def status():
    queue_status()


@worker_app.command("start")
def start(count: int = typer.Option(1, "--count")):
    print(f"Starting {count} worker(s)...")

    for i in range(count):
        print(f"Worker {i+1} started")
        run_worker()


@worker_app.command("stop")
def stop():
    global WORKER_RUNNING
    WORKER_RUNNING = False
    print("Workers stopped.")


@dlq_app.command("list")
def dlqlist():
    dlq_list()


@dlq_app.command("retry")
def retry(job_id: str):
    dlq_retry(job_id)

config_app = typer.Typer(help="Configuration")
app.add_typer(config_app, name="config")


@config_app.command("set")
def config_set(key: str, value: int):
    set_config(key, value)