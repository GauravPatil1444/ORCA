from langchain_community.tools import DuckDuckGoSearchRun
from dotenv import load_dotenv
from groq import Groq
import os

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
groq_client = Groq(api_key=GROQ_API_KEY)

def searchtool(query):

    search = DuckDuckGoSearchRun()
    prompt_data = search.invoke("oops concepts in java")
    
    chat_completion = groq_client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"""You are virtual asistant providing asistance to users based on the context provided, 
                    use that context to answer their query. never let them know you are refering any context. if context doesn't match the query just respond like a normal agent according to query.
                    
                    "context": {prompt_data}
                    "query": {query}
                    """,
                }
            ],
            model="llama-3.1-8b-instant",
        )
        
    return chat_completion.choices[0].message.content