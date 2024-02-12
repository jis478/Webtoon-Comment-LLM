# Webtoon Comment Analyzer with Open-Source LLMs

## Purpose
This repository aims to provide in-depth insights into Webtoon comments using open-source Language Model Models (LLMs) and the Retrieval Augmented Generation (RAG) framework.

## Functions
- **Crawling**: Scrapes Webtoon comments using Selenium.
- **Parsing and Cleaning**: Processes and cleans the scraped data using Pandas.
- **LLM Loading**: Loads pre-trained Language Model Models (LLMs) such as Mixtral and OpenChat.
- **RAG Setup**: Sets up the Retrieval Augmented Generation (RAG) framework for generating responses.
- **App Building**: Develops a Streamlit frontend application for interacting with the analyzed data.

## Tech Stack
- Crawling and Parsing: Selenium and Pandas
- Backend (LLM serving): Ollama API
- RAG: Langchain
- LLMs: Mixtral, OpenChat, etc.
- Frontend App: Streamlit

## Installation
- Install GoogleChrome driver
  ```bash
  sudo apt install ./google-chrome-stable_current_amd64.deb'

- Create a Conda environment and install required packages:
  ```bash
  conda create --name <env> --file requirements.txt

## Usage
- **Step 1: Crawling**

  ```bash
  python crawling_comments.py --title "lore-olympus" --title_id "1320" --start_ep 1 --end_ep 10 

- **Step 2: Parsing and cleaning**
   - To be updated

- **Step 3: App building**
   - To be updated

  
## License
To be updated

