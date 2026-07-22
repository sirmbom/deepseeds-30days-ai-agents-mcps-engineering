from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
import asyncio

app = FastAPI(title="AI Agent Backend")

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", stream=True)

class ChatRequest(BaseModel):
    message: str
    thread_id: str | None = None

async def stream_agent_response(prompt: str):
    async for chunk in llm.astream([HumanMessage(content=prompt)]):
        if chunk.content:
            yield f"data: {chunk.content}\n\n"
    yield "data: [DONE]\n\n"

@app.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    return StreamingResponse(
        stream_agent_response(request.message),
        media_type="text/event-stream"
    )