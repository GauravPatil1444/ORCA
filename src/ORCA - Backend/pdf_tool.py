from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

def pdfprocess(file_path):

    loader = PyPDFLoader('./temp/'+file_path)
    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )
    texts = text_splitter.split_documents(docs)

    uploadDocs = []

    for content in texts:
        uploadDocs.append({
            "data": content.page_content,
            "$vectorize": content.page_content
        }) 
    return uploadDocs