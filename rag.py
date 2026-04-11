from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from  langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

pdf_path=Path(__file__).parent / "nodejs.pdf"

loader=PyPDFLoader(file_path=pdf_path)
doc=loader.load()

# this is how you load the pdf 

#split the docs into small chunking 

text_splitter=RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)

chunks=text_splitter.split_documents(documents=doc)

# vector embedings 

embedding_model=OpenAIEmbeddings(
    model="text-embedding-3-large"
)

#vector store 
vector_store=FAISS.from_documents(
    documents=chunks,
    embedding=embedding_model
)

print("indexing of document done...")
print("Total vectors stored:", vector_store.index.ntotal)