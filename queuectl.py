import click
import json
import time
from storage import init_db, add_job, list_jobs

@click.group()
def cli():
    """QueueCTL - Simple Background Job Queue System"""
    init_db()   # Ensure DB is ready


@cli.command()
@click.argument('job_json')
def enqueue(job_json):
    """Add a new job in JSON format"""
    try:
        job = json.loads(job_json)
        job_id = job.get("id")
        command = job.get("command")
        max_retries = job.get("max_retries", 3)

        if not job_id or not command:
            click.echo("❌ Missing required fields: id or command")
            return

        add_job(job_id, command, max_retries)
        click.echo(f"✅ Job '{job_id}' added successfully.")
    except json.JSONDecodeError:
        click.echo("❌ Invalid JSON format")


@cli.command()
def list():
    """List all jobs"""
    jobs = list_jobs()
    if not jobs:
        click.echo("No jobs found.")
        return

    click.echo(f"{'ID':<10} {'STATE':<10} {'CMD':<20} {'ATTEMPTS':<9} {'CREATED AT'}")
    click.echo("-" * 70)
    for j in jobs:
        click.echo(f"{j[0]:<10} {j[2]:<10} {j[1]:<20} {j[3]:<9} {j[5]}")

@cli.command()
def dlq():
    """List all jobs in Dead Letter Queue"""
    import sqlite3
    conn = sqlite3.connect("queue.db")
    cur = conn.cursor()
    cur.execute("SELECT id, command, attempts, created_at FROM jobs WHERE state='dead'")
    jobs = cur.fetchall()
    conn.close()

    if not jobs:
        click.echo("No jobs in DLQ.")
        return

    click.echo(f"{'ID':<10} {'CMD':<20} {'ATTEMPTS':<9} {'CREATED AT'}")
    click.echo("-" * 70)
    for j in jobs:
        click.echo(f"{j[0]:<10} {j[1]:<20} {j[2]:<9} {j[3]}")



@cli.command()
@click.option('--count', default=1, help='Number of workers to start')
def worker(count):
    """Start worker(s)"""
    import threading
    from worker import worker_loop

    click.echo(f"🚀 Starting {count} worker(s)... Press Ctrl+C to stop.")
    threads = []

    for i in range(count):
        t = threading.Thread(target=worker_loop, args=(i + 1,))
        t.daemon = True
        t.start()
        threads.append(t)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        click.echo("\n🛑 Shutting down workers...")

@cli.command()
@click.argument('key')
@click.argument('value')
def config(key, value):
    """Set configuration value (max_retries or backoff_base)"""
    import json, os
    cfg = {}
    if os.path.exists("config.json"):
        with open("config.json", "r") as f:
            cfg = json.load(f)
    cfg[key] = int(value)
    with open("config.json", "w") as f:
        json.dump(cfg, f, indent=4)
    click.echo(f"⚙️  Config updated: {key} = {value}")



if __name__ == "__main__":
    cli()
