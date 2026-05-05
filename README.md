# Sri Lankan Job Market Analyzer

A data pipeline that scrapes, cleans, and analyzes real-time job listings from **TopJobs.lk** and **ITPro.lk** to identify in-demand skills and hiring trends in the Sri Lankan tech market.

**[Live Dashboard](https://sri-lankan-job-market-analyzer-ph8zaedjxjmjcbb5mfdlqf.streamlit.app/)** · **[GitHub](https://github.com/yshiraz/Sri-Lankan-Job-Market-Analyzer)**

---

## What It Does

- Scrapes 1,300+ live job listings across 11 tech categories
- Cleans and normalizes data — extracting locations, parsing dates, removing duplicates
- Identifies in-demand skills using a regex-based keyword extraction engine
- Visualizes findings in an interactive Streamlit dashboard with filters and searchable tables

## Key Findings

- QA/Testing and UI/UX are the most in-demand roles on Sri Lanka's dedicated tech job board
- Software Engineering has the highest number of openings
- Colombo accounts for the majority of specified-location listings
- 396 tech-specific roles scraped from ITPro.lk across categories including AI & Data, DevOps, Mobile, and Web Development

## Stack

| Layer | Tools |
|---|---|
| Scraping | Python, requests, BeautifulSoup |
| Data Processing | pandas, regex |
| Visualization | Streamlit, Plotly |
| Deployment | Streamlit Community Cloud |

## Project Structure
- scraper.py          # TopJobs.lk scraper
- scraper_itpro.py    # ITPro.lk category scraper
- clean.py            # Data cleaning pipeline
- skills.py           # Skill extraction engine
- app.py              # Streamlit dashboard
- jobs_clean.csv      # Cleaned TopJobs data
- itpro_jobs.csv      # ITPro data with categories
- skill_counts.csv    # Skill frequency (TopJobs)
- itpro_skill_counts.csv  # Skill frequency (ITPro)

## Run Locally

```bash
git clone https://github.com/yshiraz/Sri-Lankan-Job-Market-Analyzer.git
cd Sri-Lankan-Job-Market-Analyzer
pip install -r requirements.txt

python scraper.py          # scrape TopJobs
python scraper_itpro.py    # scrape ITPro
python clean.py            # clean data
python skills.py           # extract skills
streamlit run app.py       # launch dashboard
```

## Author

**Yahya Shiraz** — AI & Data Science Undergraduate, IIT / Robert Gordon University  
[LinkedIn](https://www.linkedin.com/in/yahya-shiraz/) · [GitHub](https://github.com/yshiraz-06)