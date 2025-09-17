# LangChain components for text splitting, embeddings, and vector storage
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"

def get_relevant_context(document_text: str, query: str, k: int = 5) -> str:
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, # Max size of each chunk
        chunk_overlap=150, # Overlap helps maintain context between chunks
        length_function=len
    )
    chunks = text_splitter.split_text(document_text)

    if not chunks:
        print("Warning: Text splitting resulted in no chunks.")
        return ""

    print(f"Loading embedding model '{EMBEDDING_MODEL_NAME}'...")
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL_NAME,
        model_kwargs={'device': 'cpu'} 
    )

    print("Creating FAISS vector store from text chunks...")
    vector_store = FAISS.from_texts(texts=chunks, embedding=embeddings)

    print(f"Searching for context relevant to: '{query}'...")
    retriever = vector_store.as_retriever(search_kwargs={'k': k})
    retrieved_docs = retriever.invoke(query)
    
    context = "\n\n---\n\n".join([doc.page_content for doc in retrieved_docs])
    
    return context