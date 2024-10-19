from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from openai import OpenAI
import asyncio
import logging
from backend_config import OPENAI_API_KEY, OPENAI_MODEL, TYPING_DELAY

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Set up OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

class Message(BaseModel):
    content: str
    history: list

async def generate_response(message: str, history: list):
    try:
        messages = [
            {"role": "system", "content": "You are a helpful assistant that provides information about Stripe accounts."}
        ]
        messages.extend(history)
        messages.append({"role": "user", "content": message})

        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=messages,
            stream=True
        )
        
        for chunk in response:
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content
            await asyncio.sleep(TYPING_DELAY)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        yield f"An error occurred: {str(e)}"

@app.post("/chat")
async def chat(message: Message):
    return StreamingResponse(generate_response(message.content, message.history), media_type="text/event-stream")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
