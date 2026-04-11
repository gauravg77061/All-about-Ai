from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from  langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI   


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

llm=ChatOpenAI(model='gpt-4o-mini')

def retrieve_docs(query):
    results=vector_store.similarity_search(query,k=2)
    return results


def ask_question(query):
    docs=retrieve_docs(query)
    
    context="\n\n".join([doc.page_content for doc in docs])
    
    response=llm.invoke(
        f"Answer only using this context:\n{context}\n\nQuestion: {query}"
    )
    
    return response.content 

while True:
    q = input("\nAsk question (type 'exit'): ")

    if q.lower() == "exit":
        break

    answer = ask_question(q)

    print("\nAnswer:", answer)
