from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Optional
from src.main import SecurityScanOrchestrator
import tempfile
import os

app = FastAPI()

# Pydantic models for request/response
class MessageRequest(BaseModel):
    id: int
    message: str

class MessageResponse(BaseModel):
    text: str

@app.post("/api/v1/chat/send_message/")
async def send_message(request: MessageRequest) -> MessageResponse:
    try:
        # Create a temporary directory to simulate repository
        with tempfile.TemporaryDirectory() as temp_dir:
            # Write the message content to a temporary file
            file_path = os.path.join(temp_dir, "content.txt")
            with open(file_path, "w") as f:
                f.write(request.message)

            # Initialize the orchestrator with the temporary directory
            orchestrator = SecurityScanOrchestrator(
                repo_path=temp_dir,
                cwe_path="./CWE.csv",  # Make sure this path is correct
                openai_api_key="your_api_key_here"  # Replace with actual key or env variable
            )

            # Run the security analysis
            report = orchestrator.run_analysis()

            return MessageResponse(text=report)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing security check: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
