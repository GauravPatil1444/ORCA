from langchain_text_splitters import RecursiveCharacterTextSplitter
import requests

def imageprocess(file_path,range,overlap):
    with open(file_path, "rb") as img_file:
        files = {"file": (file_path, img_file, "image/png")}
        response = requests.post('https://ocr-1-0-0.onrender.com/ocr/', files=files)
    
    json_response = response.json()
    extracted_text = json_response.get("text", "")
    print(extracted_text)
    uploadDocs = []
    uploadDocs.append({
        "data": extracted_text,
        "$vectorize": extracted_text
    })
    # uploadDocs.append({
    #     "data": extracted_text[len(extracted_text)/2:],
    #     "$vectorize": extracted_text[len(extracted_text)/2:]
    # })  
    return uploadDocs
    