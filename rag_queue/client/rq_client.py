import os
from redis import Redis
from rq import Queue
from dotenv import load_dotenv

load_dotenv()

redis_conn=Redis.from_url(os.getenv(("REDIS_URL")))

queue=Queue("rag-queue",connection=redis_conn,default_timeout=None)