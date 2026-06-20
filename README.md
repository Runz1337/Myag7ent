
# Google Search App (Python)

A simple command-line Python application that performs Google searches and displays results.

## Features
- Search Google with custom queries
- Display search results with page titles
- Configurable number of results (1-20)
- User-friendly interface with menu options
- Error handling and input validation

## Requirements
- Python 3.6+
- googlesearch-python
- requests
- beautifulsoup4

## Installation

1. Make sure you have Python 3.6+ installed
2. Install the required packages:

```bash
pip install -r requirements.txt
```

## Usage

Run the application:

```bash
python google_search_app.py
```

Follow the on-screen menu options to perform searches.

## Notes

- This app uses the `googlesearch-python` library to perform searches
- The app fetches page titles using BeautifulSoup to provide more meaningful results
- Due to Google's terms of service, this app is intended for educational purposes only
- Rate limiting is implemented (2-second pause between requests) to be respectful
- Maximum 20 results are allowed per search to prevent excessive requests

## Disclaimer

This application is for educational purposes only. Please respect Google's Terms of Service and robots.txt files. Do not use this for automated scraping or commercial purposes without proper authorization.
