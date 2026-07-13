from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter 
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
import os

RUTA_DATOS = "data"
RUTA_VECTORSTORE = "vectorstore"

embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

def cargar_documentos():
    documentos =[] 
    for archivo in os.listdir(RUTA_DATOS):
        ruta = os.path.join(RUTA_DATOS, archivo)
        if archivo.endswith(".pdf"):
            loader = PyPDFLoader(ruta)
            documentos.extend(loader.load())
        elif archivo.endswith(".txt"):
            loader = TextLoader(ruta, encoding="utf-8")
            documentos.extend(loader.load())
    return documentos

def crear_vectorstore():
    documentos = cargar_documentos()
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap = 50)
    fragmentos = splitter.split_documents(documentos)
    vectorstore = Chroma.from_documents(
        fragmentos,
        embeddings,
        persist_directory=RUTA_VECTORSTORE
    )

    return vectorstore

def buscar_contexto(pregunta, k=3):
    vectorstore=Chroma(
        persist_directory=RUTA_VECTORSTORE,
        embedding_function=embeddings
    )
    resultados = vectorstore.similarity_search(pregunta, k=k)
    contexto = "\n\n".join([doc.page_content for doc in resultados])
    return contexto 


