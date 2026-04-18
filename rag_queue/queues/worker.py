import os
from redis import Redis
from rq import Queue, SimpleWorker
from dotenv import load_dotenv

from openai import OpenAI
from pathlib import Path
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

# -------- Disable SIGALRM (FINAL FIX) --------
class NoSignalDeathPenalty:
    def __init__(self, *args, **kwargs):
        pass

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass


# -------- OpenAI client --------
client = OpenAI()

# -------- Load PDF --------
pdf_path = Path(__file__).parent.parent / "nodejs.pdf"

loader = PyPDFLoader(file_path=pdf_path)
documents = loader.load()

# -------- Chunking --------
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)

chunks = text_splitter.split_documents(documents)

# -------- Embeddings --------
embedding_model = OpenAIEmbeddings(
    model="text-embedding-3-small"
)

vector_store = FAISS.from_documents(chunks, embedding_model)

print("worker ready...")

# -------- MAIN FUNCTION --------
def process_query(query: str):
    print("🔥 JOB STARTED:", query)

    docs = vector_store.similarity_search(query, k=2)

    context = "\n\n".join([doc.page_content for doc in docs])

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "Answer ONLY from context. If not found, say 'I don't know'."
            },
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion: {query}"
            }
        ]
    )

    print("✅ response received")

    return response.choices[0].message.content


# -------- Redis + Queue --------
redis_con = Redis.from_url(os.getenv("REDIS_URL"))

queue = Queue(
    "rag-queue",
    connection=redis_con,
    default_timeout=None
)

# -------- Worker Start --------
if __name__ == "__main__":
    worker = SimpleWorker(
        [queue],
        connection=redis_con,
        
    )
    worker.death_penalty_class = NoSignalDeathPenalty

    worker.work()