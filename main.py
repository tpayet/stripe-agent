from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from openai import OpenAI
import os
import logging
import asyncio

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Set up OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
if not client.api_key:
    logger.error("OPENAI_API_KEY environment variable is not set")
    raise ValueError("OPENAI_API_KEY environment variable is not set")

class Message(BaseModel):
    content: str
    history: list

async def generate_response(message: str, history: list):
    try:
        # Prepare the messages including the conversation history
        messages = [
            {"role": "system", "content": "You are a helpful assistant that provides information about Stripe accounts."}
        ]
        messages.extend(history)
        messages.append({"role": "user", "content": message})

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            stream=True
        )
        
        for chunk in response:
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content
            await asyncio.sleep(0.05)  # Add a small delay to simulate typing
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        yield f"An error occurred: {str(e)}"

@app.post("/chat")
async def chat(message: Message):
    return StreamingResponse(generate_response(message.content, message.history), media_type="text/event-stream")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
