# Data Analyst Agent API

This is a FastAPI-based agent that ingests a `questions.txt` file and optional datasets (CSV, Excel, JSON, Parquet, PDF, images), performs analysis (scraping, parsing, plotting), and responds in the requested JSON format.

## Run locally

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
