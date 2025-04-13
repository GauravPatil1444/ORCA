from groq import Groq
from dotenv import load_dotenv
import os
import requests
from bs4 import BeautifulSoup
from fastapi.responses import HTMLResponse

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY"),
)

KEY = os.getenv("KEY")
CX = os.getenv("CX")
URL1 = os.getenv("URL1")

def customsearch(query):
    metadata = []
    params = {
        'q' : query,
        'key' : KEY,
        'cx' : CX,
        'num' : 10
    }

    response = requests.get(URL1,params=params)
    results = response.json()
    for i in range(len(results['items'])):
        metadata.append(
            results["items"][i]["link"]
        )

    return "\n".join(metadata)

# print(customsearch("give me some info about computer engg placements in rcpit"))
def service(link,query):

    res = customsearch(f"{link} {query}")
    # print(res)
    def chat_model(model,message):
        chat_completion = client.chat.completions.create(
            messages=message,
            model=model,
        )
        return chat_completion.choices[0].message.content

    # print(chat_model(res,question))

    message1 = [
        {
            "role": "user",
            "content": f""" based on the provided query give most suitable link or generate one out of the provided results only give a link in output,
            "results": {res},
            "query": {query}
            """,
        }
    ]
    searchlink = chat_model("llama-3.1-8b-instant",message1)
    return searchlink

def embed(link,query,classes_to_remove):
    if not query:
        raise HTTPException(status_code=400, detail="URL parameter missing")

    try:
        url = service(link,query)
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException:
        raise HTTPException(status_code=500, detail="Failed to fetch the page")

    soup = BeautifulSoup(response.text, 'html.parser')

    # classes_to_remove = [
    #     "header-middle p-0 bg-heder xs-text-center",
    #     "inner-header bg-black-222",
    #     "widget no-border m-0",
    #     "header-nav",
    #     "side-bar",
    #     "navbar",
    #     "footer"
    # ]
    if len(classes_to_remove)!=0:
        for class_name in classes_to_remove:
            for tag in soup.find_all(class_=class_name):
                tag.decompose()
    # print(str(soup))
    # return HTMLResponse(content=str(soup), status_code=200)
    return str(soup)

