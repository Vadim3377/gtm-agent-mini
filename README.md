
## GTM Agent Mini

A minimal AI-driven system for **automating outbound prospecting in a fintech context**.

The project explores whether company-level understanding can be automated from public data and used to generate **high-quality, personalised outreach** for cross-border payments use cases.

---

## Problem

Outbound sales in fintech is still largely manual and template-driven.
This leads to:

* low relevance in messaging
* poor conversion rates
* inefficient use of sales resources

At the same time, companies have **heterogeneous payment needs** depending on their business model, geography, and customer base.

---

## Approach

This project implements a simple pipeline that:

1. extracts company information from public websites
2. structures it into commercially relevant signals
3. estimates relevance for cross-border payments
4. generates targeted outbound messaging

The system is intentionally designed as a **multi-step pipeline** rather than a single LLM call, to improve controllability and output quality.

---

## System Architecture

```
1) Input (company, website)
2) Web scraping (multi-page)
3) LLM-based analysis (structured extraction)
4) Fit scoring (relevance estimation)
5) Personalised email generation
6) Output (CSV / UI)
```

---

## Features

* Multi-page website scraping with fallback handling
* Structured extraction of:

  * company description
  * target customers
  * potential cross-border needs
  * outreach angle
* Fit scoring (1–10) for prioritisation
* Personalised outbound email generation
* Lightweight Streamlit interface for interactive use

---

## Tech Stack

* Python
* OpenAI API
* BeautifulSoup / requests
* Streamlit

---

## Running the Project

```bash
pip install -r requirements.txt
python app.py
```

For UI:

```bash
python -m streamlit run ui.py
```

---

## Limitations

* Relies on publicly available website content (may be incomplete or blocked)
* No external enrichment (LinkedIn, firmographic APIs)
* Fit scoring is heuristic and LLM-based
* No feedback loop or learning mechanism

---

## Future Improvements

* Integrate external data sources (LinkedIn, Crunchbase, etc.)
* Add feedback loop for message optimisation
* Automate prospect discovery
* Deploy as a continuous outbound pipeline

---

# AI Usage

AI was used to accelerate prompt design and UI prototyping.
The system architecture, pipeline structure, and integration between components were implemented manually.

---
