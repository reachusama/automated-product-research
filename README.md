# automated-product-research
 

Discover and analyze online products or services using keyword-driven search, automated scraping, NLP-based feature extraction, and LLMs descriptions. 

P.S: This tools is not fully born yet.

## Todo

* [x] Made google search engine URLs filtering more flexible & extensive
* [x] Added website classification using zero-shot model
* [x] Added playwright search (got robot checks immed)
* [x] Yahoo search integrated works like a charm
* [ ] Find, Fix, Analyse
* [ ] Integrate proxies with search
* [ ] Integrate LLMs to classify and summarise text.
* [ ] Create fields like target audience etc 
* [ ] Improve Zero-shot classification labels
* [ ] Bug in CSV writing that starts writing text
* [ ] Improve website classification more robust using spaCy / AI
* [ ] Scrapers are receiving timeouts or getting blocked (consider using Selenium)
* [ ] Consider using only SEO data, rather raw_text data from home page
* [ ] Add LLMs to process data and create labels
* [ ] 

## Python Installation

```

pip install google-api-python-client beautifulsoup4 pandas requests spacy
python -m spacy download en_core_web_sm
pip install isort black
pip install tldextract
pip install transformers torch
pip install playwright
playwright install
```

## Project Structure

```
automated-product-research/
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



