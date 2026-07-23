# pdf_web_tool.py
import os
import gc
import requests
from bs4 import BeautifulSoup
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from app.ingestion.metadata_utils import create_metadata

def process(docs, range_val, overlap, source, category, config):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=range_val,
        chunk_overlap=overlap,
    )
    texts = text_splitter.split_documents(docs)
    uploadDocs = []
    metadata = create_metadata(source, category, config)
    
    for content in texts:
        uploadDocs.append({
            "data": content.page_content,
            "$vectorize": content.page_content,
            "metadata": metadata
        }) 
    return uploadDocs

def process_pdf(file_path, range_val, overlap):
    loader = PyPDFLoader(file_path)
    docs = loader.load()
    del loader
    gc.collect()
    
    source = os.path.basename(file_path)
    config = {"chunk_size": range_val, "chunk_overlap": overlap}
    return process(docs, range_val, overlap, source, "pdf_standard", config)

def process_web(url, range_val, overlap, classes_to_remove=None):
    # Fetch and parse HTML
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Apply class exclusions BEFORE text splitting (Spec 2.2)
    if classes_to_remove:
        for class_name in classes_to_remove:
            for tag in soup.find_all(class_=class_name):
                tag.decompose()
                
    text = soup.get_text(separator='\n', strip=True)
    docs = [Document(page_content=text)]
    
    config = {"chunk_size": range_val, "chunk_overlap": overlap}
    if classes_to_remove:
        config["excluded_css_classes"] = classes_to_remove
        
    return process(docs, range_val, overlap, url, "web_page", config)