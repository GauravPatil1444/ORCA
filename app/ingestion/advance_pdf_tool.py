# advance_pdf_tool.py
import os
import re
from pypdf import PdfReader
from metadata_utils import create_metadata

def adv_pdf(file_path, regex):
    reader = PdfReader(file_path)
    number_of_pages = len(reader.pages)
    pattern = rf"{regex}"
    extracted = []
    
    for i in range(number_of_pages):
        page = reader.pages[i]
        text = page.extract_text()
        matches = re.findall(pattern, text)
        if matches:
            extracted.extend(matches)
            
    source = os.path.basename(file_path)
    config = {"regex_expression": regex}
    metadata = create_metadata(source, "pdf_regex", config)
    
    uploadDocs = []
    for item in extracted:
        uploadDocs.append({
            "data": str(item),
            "$vectorize": str(item),
            "metadata": metadata
        })
    return uploadDocs