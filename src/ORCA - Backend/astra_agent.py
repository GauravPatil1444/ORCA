from dotenv import load_dotenv
from groq import Groq
import os

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
groq_client = Groq(api_key=GROQ_API_KEY)

def Agent(question: str, collection, prompt:str):
        vector_match = collection.find(
            sort={"$vectorize": question},
            limit=5
        )

        prompt_data = [data["data"] for data in vector_match]

        chat_completion = groq_client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"""You are virtual assistant named 'ORCA' providing assistance to users based on the context provided, 
                    use that context to answer their query.{prompt}. never let them know you are refering any context. Also handle out of context queries.  
                    "context": {prompt_data}
                    "query": {question}
                    """,
                }
            ],
            model="meta-llama/llama-4-maverick-17b-128e-instruct",
        )
        res = chat_completion.choices[0].message.content
        return res
        