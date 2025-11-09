# 🧰 QueueCTL — Background Job Queue System

## 📘 Overview  
**QueueCTL** is a Python-based CLI background job system that manages and executes queued tasks using worker processes.  
It supports **automatic retries**, **exponential backoff**, and a **Dead Letter Queue (DLQ)** for permanently failed jobs —  
all with **persistent storage** powered by SQLite.

This project was developed as part of a **Backend Developer Internship Assignment**.

---

## 🚀 Features
- ✅ Enqueue and manage background jobs via CLI  
- ✅ Multiple worker process support (`--count`)  
- ✅ Retry mechanism with exponential backoff  
- ✅ Dead Letter Queue (DLQ) for failed jobs  
- ✅ Persistent SQLite database  
- ✅ Simple and modular Python codebase  

---

## ⚙️ Tech Stack
- **Language:** Python 3  
- **Database:** SQLite  
- **CLI Framework:** Click  
- **Operating System:** Windows / macOS / Linux  

---

## 🧩 Project Structure

| File | Description |
|------|-------------|
| `queuectl.py` | Main CLI entry point |
| `worker.py` | Handles job execution, retry logic, and DLQ |
| `storage.py` | SQLite database management |
| `config.py` | Configuration (retries, backoff, etc.) |
| `requirements.txt` | Dependencies |
| `queue.db` | Persistent job storage |
| `README.md` | Project documentation |

---

## ⚙️ Setup & Installation

### ✅ Step 1 — Clone the Repository
```bash
git clone https://github.com/PavanBoggavarapu/queuectl.git
cd queuectl

✅ Step 2 — Install Dependencies
pip install -r requirements.txt

💻 Usage Guide
➕ Enqueue Jobs
python queuectl.py enqueue "{\"id\":\"job1\",\"command\":\"echo hello\"}"
python queuectl.py enqueue "{\"id\":\"job2\",\"command\":\"echo success\"}"
python queuectl.py enqueue "{\"id\":\"job3\",\"command\":\"wrongcmd\"}"

📋 List All Jobs
python queuectl.py list

⚙️ Start Worker
python queuectl.py worker --count 1

💀 View Dead Letter Queue
python queuectl.py dlq

| State        | Meaning                            |
| ------------ | ---------------------------------- |
| `pending`    | Job waiting for execution          |
| `processing` | Job is running                     |
| `completed`  | Job executed successfully          |
| `failed`     | Job failed and will retry          |
| `dead`       | Job moved to DLQ after max retries |


🧠 Retry & Backoff Logic
QueueCTL uses exponential backoff for retries:

Example (base = 2):
✅ 1st retry → 2 seconds
✅ 2nd retry → 4 seconds
✅ 3rd retry → 8 seconds

After exceeding max_retries, the job is moved to the Dead Letter Queue.

🧪 Example Run
python queuectl.py enqueue "{\"id\":\"demo1\",\"command\":\"echo demo\"}"
python queuectl.py list
python queuectl.py worker --count 1
python queuectl.py dlq

✅ Expected Output
✅ Job 'demo1' added successfully.
[Worker 1] ▶️ Running job demo1 (attempt 1)
[Worker 1] ✅ Completed job demo1

## 🎥 Demo Video  
[🎬 Click here to watch the demo]( https://drive.google.com/file/d/1zE5SecvG2_1Did6zn91PCQW93BJfAY2A/view?usp=drive_link)



👤 Author
Pavan B
B.Tech CSE (AI/ML)
Amrita Vishwa Vidyapeetham, Amaravati
