# Web Scraper with GUI

## Overview
This web scraper allows you to scrape blog titles and links from a given URL. You can specify the CSS selectors for the title and link elements to precisely extract the data. The scraper also supports pagination, allowing you to scrape multiple pages if needed.

## Features
- Scrape blog titles and links from a given URL.
- Specify CSS selectors for title and link elements.
- Support for scraping multiple pages through pagination.
- Export results in CSV, JSON, or TXT formats.
- Easy-to-use GUI built with `tkinter`.
- Configuration file (`config.json`) to store the last used settings.

## Setup and Installation

### Requirements
- **Python 3.x** (Preferably Python 3.6+)
- **Libraries**: `requests`, `beautifulsoup4`, and `tkinter`.

### Install Dependencies
To install the required dependencies, open a terminal and run the following command:
```bash
pip install requests beautifulsoup4

