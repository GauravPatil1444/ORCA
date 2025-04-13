from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

def process(docs,range,overlap):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=range,   
        chunk_overlap=overlap,
    )
    texts = text_splitter.split_documents(docs)

    uploadDocs = []

    for content in texts:
        uploadDocs.append({
            "data": content.page_content,
            "$vectorize": content.page_content
        }) 
    return uploadDocs


def pdfprocess(file_path,range,overlap):

    loader = PyPDFLoader(file_path)
    docs = loader.load()
    return process(docs,range,overlap)


def webprocess(file_path,range,overlap):

    loader = WebBaseLoader(file_path)
    docs = loader.load()
    return process(docs,range,overlap)
