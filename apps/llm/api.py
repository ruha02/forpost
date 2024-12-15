from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import tempfile
import shutil
import git
from urllib.parse import urlparse
import validators

from src.main import SecurityScanOrchestrator
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI()

class Config:    
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Pydantic models for request/response
class MessageRequest(BaseModel):
    id: int
    message: str

class MessageResponse(BaseModel):
    text: str

def is_github_url(url):
    """Check if the given URL is a valid GitHub repository URL."""
    if not validators.url(url):
        return False
    
    parsed = urlparse(url)
    return parsed.netloc in ['github.com', 'www.github.com']

def clone_github_repo(url):
    """Clone a GitHub repository to a temporary directory and return the path."""
    # Create a temporary directory
    temp_dir = tempfile.mkdtemp()
    
    try:
        # Clone the repository
        git.Repo.clone_from(url, temp_dir)
        return temp_dir
    except git.GitCommandError as e:
        # Clean up the temporary directory if cloning fails
        shutil.rmtree(temp_dir, ignore_errors=True)
        raise Exception(f"Failed to clone repository: {str(e)}")

def process_input(input_path):
    """Process the input path and return the actual path to scan."""
    temp_dir = None
    
    try:
        if is_github_url(input_path):
            # Clone GitHub repository to temporary directory
            temp_dir = clone_github_repo(input_path)
            return temp_dir, temp_dir
        elif os.path.exists(input_path):
            # Local path
            return input_path, None
        else:
            raise Exception("Invalid path or URL")
    except Exception as e:
        if temp_dir:
            shutil.rmtree(temp_dir, ignore_errors=True)
        raise e

@app.post("/api/v1/chat/send_message/")
async def send_message(request: MessageRequest) -> MessageResponse:
    temp_dir = None
    try:
        # Process the input path
        scan_path, temp_dir = process_input(request.message)

        # Initialize orchestrator
        orchestrator = SecurityScanOrchestrator(
            repo_path=scan_path,
            cwe_path="./CWE.csv",
            openai_api_key=Config.OPENAI_API_KEY
        )

        # Run analysis
        report = orchestrator.run_analysis()

        # Clean up temporary directory if it was created
        if temp_dir and os.path.exists(temp_dir):
            try:
                shutil.rmtree(temp_dir)
            except Exception as cleanup_error:
                print(f"Warning: Failed to clean up temporary files: {str(cleanup_error)}")

        return MessageResponse(text=report)

    except Exception as e:
        # Clean up temporary directory in case of error
        if temp_dir and os.path.exists(temp_dir):
            shutil.rmtree(temp_dir, ignore_errors=True)
        
        # Raise HTTP exception with error details
        raise HTTPException(status_code=400, detail=str(e))

# Optional: Add a health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# To run the API:
# uvicorn your_file_name:app --reload
