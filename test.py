from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from llm.email_convo import EmailConvo

GenAIapp = FastAPI()

class CommandRequest(BaseModel):
    editorTopContent: str
    editorLeftContent: str
    editorRightContent: str
    chatMessages: List[Dict[str, str]]

@GenAIapp.post("/command")
async def command(request: CommandRequest):
    email_convo = EmailConvo()
    response = email_convo.handle_command(request)
    return response

# Include other routes and middlewares as needed
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(GenAIapp, host="0.0.0.0", port=8000)
