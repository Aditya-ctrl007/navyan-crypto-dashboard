# Real-Time Cryptocurrency Dashboard

**Navyan Data Analytics Internship — Project 3**
**Author:** Singh Aditya Manoj Kumar
**Email:** officialadityasingh.in@gmail.com
**GitHub:** [Aditya-ctrl007](https://github.com/Aditya-ctrl007)

---

## What This Project Does

A live cryptocurrency dashboard that fetches real-time prices for the top 10 cryptocurrencies using the CoinGecko API and displays them in an interactive Streamlit dashboard — no API key required.

## Features

- Live prices for top 10 cryptocurrencies (updates every 60 seconds)
- 5 interactive charts: bar, horizontal bar, pie, bubble, high/low range
- Customisable price alerts with sidebar controls
- Full data table with colour-coded 24h change
- Auto-refresh toggle

## Tools Used

- **Python** — core language
- **requests** — API calls to CoinGecko
- **pandas** — data processing
- **Streamlit** — dashboard framework
- **Plotly** — interactive charts

## Data Source

[CoinGecko API](https://www.coingecko.com/en/api) — free, no API key needed

## How to Run

```bash
pip install -r requirements.txt
python fetch_data.py      # test API connection first
streamlit run dashboard.py
```

The dashboard opens at http://localhost:8501

## Project Structure

```
navyan_project3/
├── fetch_data.py       # API connection & data fetching
├── dashboard.py        # Streamlit dashboard
├── requirements.txt    # Python libraries
└── README.md           # This file
```

## Submission

- **GitHub:** https://github.com/Aditya-ctrl007/navyan-crypto-dashboard
- **Live Dashboard:** https://navyan-crypto-dashboard-smucruuxnintysw52wxzq2.streamlit.app/
