# automated-product-research
 

Discover and analyze online products or services using keyword-driven search, automated scraping, NLP-based feature extraction, and LLMs descriptions. 

P.S: This tools is not fully born yet.

## Python Installation

```

pip install google-api-python-client beautifulsoup4 pandas requests spacy
python -m spacy download en_core_web_sm
pip install isort black

```

## Project Structure

```
ai_edtech_scraper/
│
├── config/
│   └── settings.py             # API keys, search config, paths
│
├── core/
│   ├── search_google.py        # Google CSE logic
│   ├── extractor.py            # NLP, metadata, contact extraction
│   ├── scraper.py              # Page scraping logic
│   ├── csv_writer.py           # CSV and progress tracking
│
├── run/
│   └── run_scraper.py          # Entrypoint script
│
├── data/
│   ├── ai_edtech_results.csv   # Output
│   └── scrape_progress.csv     # Progress tracker
│
├── app/                        # Future Streamlit UI
│   └── streamlit_ui.py
│
├── tests/                      # Unit tests
│
├── requirements.txt
└── README.md

```

## Google Search Engine:

```
Custom Search API
```

## Todo

[] Make product signal verifier more robust using spacy
[] Scrapers recieve timeout or blocked (Maybe selenium)
[] Make search criterias more robust