
#!/usr/bin/env python3
"""
Google Search App - A simple Python application to perform Google searches
"""

import sys
import time
from googlesearch import search
import requests
from bs4 import BeautifulSoup
import re

def perform_google_search(query, num_results=10):
    """
    Perform a Google search and return results
    """
    try:
        print(f"\nSearching Google for: '{query}'...\n")
        print("Please wait, fetching results...\n")
        
        # Perform the search
        results = []
        for url in search(query, num_results=num_results, stop=num_results, pause=2):
            results.append(url)
            # Show progress
            print(f"Found: {url}")
        
        return results
        
    except Exception as e:
        print(f"Error performing search: {e}")
        return []

def get_page_title(url):
    """
    Get the title of a webpage
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.title.string if soup.title else "No title found"
        return title.strip()
        
    except Exception as e:
        return f"Error fetching title: {e}"

def display_results(query, urls):
    """
    Display search results in a formatted way
    """
    if not urls:
        print("\nNo results found.")
        return
    
    print(f"\n{'='*80}")
    print(f"GOOGLE SEARCH RESULTS FOR: '{query}'")
    print(f"{'='*80}")
    
    for i, url in enumerate(urls, 1):
        title = get_page_title(url)
        print(f"\n{i}. {title}")
        print(f"   URL: {url}")
        print(f"   {'-'*60}")
    
    print(f"\nTotal results: {len(urls)}")

def main():
    """
    Main function to run the Google search app
    """
    print("========================================")
    print("     GOOGLE SEARCH APP")
    print("========================================")
    
    while True:
        print("\n1. Perform a Google search")
        print("2. Exit")
        
        choice = input("\nChoose an option (1 or 2): ").strip()
        
        if choice == '2':
            print("\nThank you for using Google Search App!")
            break
        elif choice == '1':
            query = input("\nEnter your search query: ").strip()
            
            if not query:
                print("Please enter a valid search query.")
                continue
            
            # Get number of results (optional)
            try:
                num_results = input("Number of results (default 10): ").strip()
                num_results = int(num_results) if num_results else 10
                if num_results < 1:
                    num_results = 10
                elif num_results > 20:
                    num_results = 20
                    print("Maximum 20 results allowed.")
            except ValueError:
                num_results = 10
            
            # Perform search
            urls = perform_google_search(query, num_results)
            
            # Display results
            display_results(query, urls)
            
            # Ask if user wants to search again
            again = input("\nPerform another search? (y/n): ").strip().lower()
            if again != 'y' and again != 'yes':
                print("\nThank you for using Google Search App!")
                break
        else:
            print("Invalid option. Please choose 1 or 2.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nApplication interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        sys.exit(1)
