from fastapi import FastAPI
from client.rq_client import queue

from redis import Redis
from rq.job import Job
import os
from dotenv import load_dotenv



load_dotenv()

app = FastAPI()

redis_conn = Redis.from_url(os.getenv("REDIS_URL"))


@app.get('/')
def root():
    return {"status": "Server is running"}


@app.post("/ask")
def ask(query: str):
    job = queue.enqueue("queues.worker.process_query", query, job_timeout=None)

    return {
        "status": "queued",
        "job_id": job.id
    }


@app.get("/result/{job_id}")
def get_result(job_id: str):
    job = Job.fetch(job_id, connection=redis_conn)

    if job.is_finished:
        return {
            "status": "finished",
            "result": job.result
        }

    elif job.is_failed:
        return {
            "status": "failed"
        }

    else:
        return {
            "status": "processing"
        }