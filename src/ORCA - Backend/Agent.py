from groq import Groq
import os

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
groq_client = Groq(api_key=GROQ_API_KEY)

def Agent(question: str, collection):
        vector_match = collection.find(
            sort={"$vectorize": question},
            limit=5
        )

        prompt_data = [data["data"] for data in vector_match]

        chat_completion = groq_client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"""You are virtual asistant providing asistance to users based on the context provided, 
                    use that context to answer their query. never let them know you are refering any context. if context doesn't match the query just response with '404'
                    
                    "context": {prompt_data}
                    "query": {question}
                    """,
                }
            ],
            model="llama-3.1-8b-instant",
        )
        
        return chat_completion.choices[0].message.content