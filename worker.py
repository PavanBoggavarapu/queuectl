import sqlite3
import subprocess
import time
import math
from datetime import datetime

DB_FILE = "queue.db"
CONFIG_FILE = "config.json"


def get_config():
    """Read retry and backoff settings."""
    import json, os
    if not os.path.exists(CONFIG_FILE):
        return {"max_retries": 3, "backoff_base": 2}
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)


def get_next_job():
    """Fetch one pending job."""
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute(
        "SELECT id, command, attempts, max_retries FROM jobs WHERE state='pending' ORDER BY created_at LIMIT 1"
    )
    job = cur.fetchone()
    conn.close()
    return job


def update_job_state(job_id, state, attempts):
    """Update job state and attempts."""
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute(
        "UPDATE jobs SET state=?, attempts=?, updated_at=? WHERE id=?",
        (state, attempts, datetime.utcnow().isoformat(), job_id),
    )
    conn.commit()
    conn.close()


def process_job(worker_id, job):
    """Run and handle job execution."""
    job_id, command, attempts, max_retries = job
    print(f"[Worker {worker_id}] ▶️  Running job {job_id} (attempt {attempts+1})")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"[Worker {worker_id}] ✅ Completed job {job_id}")
            update_job_state(job_id, "completed", attempts + 1)
        else:
            print(f"[Worker {worker_id}] ❌ Failed job {job_id}")
            handle_retry(worker_id, job)
    except Exception as e:
        print(f"[Worker {worker_id}] ⚠️ Error: {e}")
        handle_retry(worker_id, job)


def handle_retry(worker_id, job):
    """Retry failed jobs with exponential backoff, or move to DLQ."""
    job_id, command, attempts, max_retries = job
    cfg = get_config()
    backoff_base = cfg.get("backoff_base", 2)

    attempts += 1
    if attempts >= max_retries:
        print(f"[Worker {worker_id}] 💀 Job {job_id} moved to DLQ after {attempts} attempts")
        update_job_state(job_id, "dead", attempts)
        return

    delay = int(math.pow(backoff_base, attempts))
    print(f"[Worker {worker_id}] 🔁 Retrying job {job_id} in {delay}s (attempt {attempts})")
    update_job_state(job_id, "pending", attempts)
    time.sleep(delay)


def worker_loop(worker_id):
    """Continuously process pending jobs."""
    while True:
        job = get_next_job()
        if not job:
            time.sleep(2)
            continue
        update_job_state(job[0], "processing", job[2])
        process_job(worker_id, job)
