#!/usr/bin/env python3
"""
Basic example of using the mcp_youtube_search package.
"""

import os
from dotenv import load_dotenv
from mcp_youtube_search.search import YouTubeSearch

def main():
    # Load environment variables from .env file (if it exists)
    load_dotenv()
    
    # Get API key from environment or use your own
    api_key = os.getenv("SERP_API_KEY")
    if not api_key:
        print("Error: SERP_API_KEY environment variable not set.")
        print("Please set it or provide your key directly to the YouTubeSearch constructor.")
        return
    
    # Create search client
    search = YouTubeSearch(api_key=api_key)
    
    # Define search query
    query = "Python programming tutorial"
    max_results = 5
    
    print(f"Searching YouTube for '{query}'...")
    
    # Perform search
    results = search.search(query=query, max_results=max_results)
    
    # Check for errors
    if "error" in results:
        print(f"Error: {results['error']}")
        return
    
    # Display results
    print(f"\nFound {results['count']} results:")
    for i, video in enumerate(results['results'], 1):
        print(f"\n{i}. {video['title']}")
        print(f"   Channel: {video['channel']}")
        print(f"   URL: {video['link']}")
        print(f"   Duration: {video['duration']}")
        print(f"   Views: {video['views']}")
        print(f"   Published: {video['published_date']}")
        print(f"   Description: {video['description'][:100]}...")  # Show just start of description

if __name__ == "__main__":
    main() 