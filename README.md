# QueueCTL

A CLI-based Background Job Queue System built in Python.

## Features

- Enqueue background jobs
- Execute jobs using workers
- Multiple worker support
- Retry failed jobs
- Exponential Backoff
- Dead Letter Queue (DLQ)
- SQLite persistent storage
- Configurable retry count
- Configurable backoff delay
- Queue status
- List jobs by state

---

## Tech Stack

- Python 3
- Typer
- SQLAlchemy
- SQLite

---

## Project Structure

```
queuectl/
│
├── app/
├── data/
├── tests/
├── main.py
├── requirements.txt
├── README.md
└── test_queue.bat
```

---

## Installation

```bash
git clone <repository_url>

cd queuectl

python -m venv .venv

.venv\Scripts\activate

pip install -r requirements.txt
```

---

## Commands

### Enqueue

```bash
python main.py enqueue job1 "echo Hello"
```

### List Jobs

```bash
python main.py list
```

### List by State

```bash
python main.py list --state pending
```

### Queue Status

```bash
python main.py status
```

### Start Worker

```bash
python main.py worker start --count 2
```

### Stop Worker

```bash
python main.py worker stop
```

### Dead Letter Queue

```bash
python main.py dlq list
```

Retry a DLQ Job

```bash
python main.py dlq retry fail
```

### Configuration

```bash
python main.py config set max_retries 5

python main.py config set backoff_base 3
```

---

## Job Lifecycle

Pending

↓

Processing

↓

Completed

OR

↓

Retry

↓

Dead Letter Queue

---

## Persistence

All jobs are stored in SQLite.

Jobs remain available after restarting the application.

---

## Future Improvements

- Job Priority
- Scheduled Jobs
- Job Timeout
- Dashboard
- Metrics

---

## Author

Ayush Singh