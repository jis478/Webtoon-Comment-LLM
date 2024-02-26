# Webtoon Comment Analyzer with Open-Source LLMs

## Purpose
This repository aims to provide in-depth insights into Webtoon comments using open-source Language Model Models (LLMs) and the Retrieval Augmented Generation (RAG) framework.

## Functions
- **Crawling & Parsing**: Scrapes Webtoon comments using Selenium and parsed them accordingly
- **LLM Loading**: Loads LLM such as Mixtral and OpenChat
- **RAG Setup**: Sets up the RAG framework for generating responses
- **App Building**: Chat-based Streamlit app for analyzing comments

## Tech Stack
- Crawling and Parsing: Selenium and Pandas
- Backend (LLM serving): Ollama API
- RAG: Langchain
- Frontend (App): Streamlit

## Installation
- Install GoogleChrome driver
  ```bash
  sudo apt install ./google-chrome-stable_current_amd64.deb'

- Create a Conda environment and install required packages:
  ```bash
  conda create --name <env> --file requirements.txt

## Usage
- **Step 0: Conda env activation**

  ```bash
  conda activate <env>

- **Step 1: Crawling & parsing**

  ```bash
  python crawling_comments.py --title "lore-olympus" --title_id "1320" --start_ep 1 --end_ep 10 

- **Step 2: Ollama serve**
  
  ```bash
  CUDA_VISIBLE_DEVICES=0 ollama serve

- **Step 3: Streamlit app**

  - execution (Upload the csv file created in Step 1)  

    ```bash
    streamlit run app.py --server.port 7087 --server.address 0.0.0.0
  
## Upcoming features
- More advanced features (within the RAG pipeline) will be introduced