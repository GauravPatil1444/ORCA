from pypdf import PdfReader
import re

def adv_pdf(file_path,regex):
    reader = PdfReader(file_path)
    number_of_pages = len(reader.pages)
    pattern = rf"{regex}"

    extracted = []
    uploadDocs = []

    for i in range(number_of_pages):
        page = reader.pages[i]
        text = page.extract_text()
        # print(text)
        matches = re.findall(pattern, text)
        if len(matches)!=0:
            extracted.append(matches)
    
    for chunk in extracted:
        for item in chunk:
            uploadDocs.append({
                "data": str(item),
                "$vectorize": str(item)
            })

    return uploadDocs
