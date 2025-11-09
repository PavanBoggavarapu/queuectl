QueueCTL — Background Job Queue System
📘 Overview

QueueCTL is a Python-based CLI background job system that manages and executes queued tasks using worker processes.
It supports automatic retries, exponential backoff, and a Dead Letter Queue (DLQ) for permanently failed jobs —
all with persistent storage powered by SQLite.

🚀 Features
✅ Enqueue and manage background jobs via CLI
✅ Multiple worker process support (--count)
✅ Retry mechanism with exponential backoff
✅ Dead Letter Queue (DLQ) for failed jobs
✅ Persistent SQLite database
✅ Simple and modular Python codebase

⚙️ Tech Stack
Language: Python 3
Database: SQLite
CLI Framework: Click
Operating System: Windows

🧩 Project Structure
File	Description
queuectl.py	Main CLI entry point
worker.py	Handles job execution, retry logic, and DLQ
storage.py	SQLite database management
config.py	Configuration (retries, backoff, etc.)
requirements.txt	Dependencies list
queue.db	Persistent job storage
README.md	Documentation
⚙️ Setup & Installation
Step 1 — Clone the Repository
git clone https://github.com/PavanBoggavarapu/queuectl.git
cd queuectl

Step 2 — Install Dependencies
pip install -r requirements.txt

💻 Usage Guide
 Enqueue Jobs
python queuectl.py enqueue "{\"id\":\"job1\",\"command\":\"echo hello\"}"
python queuectl.py enqueue "{\"id\":\"job2\",\"command\":\"echo success\"}"
python queuectl.py enqueue "{\"id\":\"job3\",\"command\":\"wrongcmd\"}"

📋 List All Jobs
python queuectl.py list

⚙️ Start Worker
python queuectl.py worker --count 1

🔄 Job Lifecycle
State	Description
pending	Job waiting for execution
processing	Job currently being executed
completed	Job finished successfully
failed	Job failed but will retry
dead	Job permanently failed (moved to DLQ)
🧠 Retry & Backoff Logic

Jobs are retried automatically using exponential backoff:
delay = base ^ attempts


Example: if base = 2 → retries after 2s, 4s, and 8s.
After exceeding max_retries, the job is sent to the DLQ.

🧪 Example Run
python queuectl.py enqueue "{\"id\":\"demo1\",\"command\":\"echo demo\"}"
python queuectl.py list
python queuectl.py worker --count 1
python queuectl.py dlq

✅ Expected Output:
✅ Job 'demo1' added successfully.
[Worker 1] ▶️ Running job demo1 (attempt 1)
[Worker 1] ✅ Completed job demo1

🎥 Demo Video
https://drive.google.com/file/d/1zE5SecvG2_1Did6zn91PCQW93BJfAY2A/view?usp=sharing

👤 Author
Pavan B
B.Tech CSE (AI/ML)
Amrita Vishwa Vidyapeetham, Amaravati
(AV.EN.U4AIE22056)

🏁 Summary
QueueCTL is a lightweight yet production-style job queue system that demonstrates:
Backend design principles
Process management
Resilience through retries and DLQ
CLI development using Python
