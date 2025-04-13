import csv
import json

def csvprocess(file_path):
    json_data = []

    with open(file_path, mode="r", newline='', encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            json_data.append(row)

    with open('./json_data.json', "w", encoding="utf-8") as json_file:
        json.dump(json_data, json_file, indent=4)
    
    upload_data = []
    for item in json_data:
        upload_data.append(
            {
                "data": str(item),
                "$vectorize":str(item)
            }
        )

    return upload_data

def jsonprocess(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        upload_data = []
        for item in data:
            upload_data.append(
                {
                    "data": str(item),
                    "$vectorize":str(item)
                }
            )  
    return upload_data