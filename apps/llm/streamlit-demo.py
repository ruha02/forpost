import streamlit as st
from src.main import SecurityScanOrchestrator
import os
import tempfile
import shutil
import git
from urllib.parse import urlparse
import validators

import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

class Config:    
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

def initialize_chat_history():
    if "messages" not in st.session_state:
        st.session_state.messages = []

def initialize_orchestrator(scan_path):
    if "orchestrator" not in st.session_state:
        st.session_state.orchestrator = SecurityScanOrchestrator(
            repo_path=scan_path,  # Will be updated dynamically
            cwe_path="./CWE.csv",
            openai_api_key=Config.OPENAI_API_KEY
        )

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

def is_github_url(url):
    """Check if the given URL is a valid GitHub repository URL."""
    if not validators.url(url):
        return False
    
    parsed = urlparse(url)
    return parsed.netloc in ['github.com', 'www.github.com']

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

def main():
    st.title("Security Vulnerability Scanner Chat")
    
    # Initialize chat history and orchestrator
    initialize_chat_history()

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Enter a file path or GitHub repository URL to scan"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)

        # Process the input
        with st.chat_message("assistant"):
            temp_dir = None
            try:
                with st.spinner("Processing input..."):
                    scan_path, temp_dir = process_input(prompt)
                
                with st.spinner("Analyzing..."):
                    # Update orchestrator with new path
                    print(scan_path)
                    initialize_orchestrator(scan_path=scan_path)

                    
                    # Run analysis
                    report = st.session_state.orchestrator.run_analysis()
                    
                    # Display results
                    st.markdown(report)
                    
                    # Add assistant message to chat history
                    st.session_state.messages.append({"role": "assistant", "content": report})
            
            except Exception as e:
                error_message = f"Error: {str(e)}"
                st.error(error_message)
                st.session_state.messages.append({"role": "assistant", "content": error_message})
            
            finally:
                # Clean up temporary directory if it exists
                if temp_dir and os.path.exists(temp_dir):
                    try:
                        shutil.rmtree(temp_dir)
                    except Exception as e:
                        st.warning(f"Failed to clean up temporary files: {str(e)}")

    # Add sidebar with information
    with st.sidebar:
        st.header("About")
        st.markdown("""
        This security vulnerability scanner can analyze:
        - Local file paths
        - GitHub repository URLs
        
        Simply paste the path or URL in the chat input to begin scanning.
        """)
        
        # Add clear chat button
        if st.button("Clear Chat"):
            st.session_state.messages = []
            st.rerun()

if __name__ == "__main__":
    main()
