#!/usr/bin/env python3
"""
Example showing how to run the MCP YouTube Search server.
"""

import os
from dotenv import load_dotenv
from mcp_youtube_search.mcp_server import run_server

def main():
    # Load environment variables from .env file (if it exists)
    load_dotenv()
    
    # Get API key from environment or use your own
    api_key = os.getenv("SERP_API_KEY")
    if not api_key:
        print("Error: SERP_API_KEY environment variable not set.")
        print("Please set it or provide your key directly to the run_server function.")
        return
    
    print("Starting MCP YouTube Search server...")
    print("The server will listen on stdin/stdout for MCP protocol messages.")
    print("Press Ctrl+C to exit.")
    
    # Run the server
    run_server(api_key=api_key)

if __name__ == "__main__":
    main() 