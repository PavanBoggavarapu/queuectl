import sqlite3
from datetime import datetime

DB_FILE = "queue.db"

def init_db():
    """Create the jobs table if it doesn’t exist"""
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id TEXT PRIMARY KEY,
            command TEXT,
            state TEXT,
            attempts INTEGER,
            max_retries INTEGER,
            created_at TEXT,
            updated_at TEXT
        )
    """)
    conn.commit()
    conn.close()


def add_job(job_id, command, max_retries=3):
    """Insert a new job"""
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    created = datetime.utcnow().isoformat()
    cur.execute("""
        INSERT INTO jobs (id, command, state, attempts, max_retries, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (job_id, command, "pending", 0, max_retries, created, created))
    conn.commit()
    conn.close()


def list_jobs():
    """Return all jobs"""
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT id, command, state, attempts, max_retries, created_at FROM jobs")
    jobs = cur.fetchall()
    conn.close()
    return jobs
