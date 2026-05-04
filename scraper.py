import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

BASE_URL = "https://www.topjobs.lk/applicant/vacancybyfunctionalarea.jsp"
DETAIL_URL = "https://www.topjobs.lk/applicant/JobAdvertismentServlet?AC=JOBADVERT&EC={ec}&JC={jc}"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
}

def scrape_jobs():
    response = requests.get(BASE_URL, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", {"class": "vbfa-table"})

    if not table:
        print("Table not found!")
        return []

    rows = table.find_all("tr")[1:]
    print(f"Found {len(rows)} job rows")

    jobs = []
    for i, row in enumerate(rows):
        cols = row.find_all("td")
        if len(cols) < 5:
            continue

        col2 = cols[2]
        h2 = col2.find("h2")
        h1 = col2.find("h1")

        # Each row has its own index-matched hidden spans: hdnJC0, hdnEC0 for row 0, etc.
        jc_span = col2.find("span", id=f"hdnJC{i}")
        ec_span = col2.find("span", id=f"hdnEC{i}")
        jc = jc_span.get_text(strip=True) if jc_span else ""
        ec = ec_span.get_text(strip=True) if ec_span else ""

        job = {
            "ref_no":        cols[1].get_text(strip=True),
            "title":         h2.get_text(strip=True) if h2 else "",
            "company":       h1.get_text(strip=True) if h1 else "",
            "description":   cols[3].get_text(strip=True),
            "opening_date":  cols[4].get_text(strip=True),
            "closing_date":  cols[5].get_text(strip=True),
            "job_code":      jc,
            "employer_code": ec,
            "detail_url":    DETAIL_URL.format(ec=ec, jc=jc) if ec and jc else ""
        }
        jobs.append(job)

    return jobs

def scrape_job_detail(url):
    """Scrape full description from individual job page"""
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        # Job descriptions are usually in a div with class containing 'job' or a large text block
        # Try common containers
        for selector in ["div.job-description", "div#jobDetails", "td.job-desc", "div.vacancy-details"]:
            container = soup.select_one(selector)
            if container:
                return container.get_text(separator=" ", strip=True)
        # Fallback: get the largest text block on the page
        paragraphs = soup.find_all("p")
        if paragraphs:
            return " ".join(p.get_text(strip=True) for p in paragraphs[:10])
        return ""
    except Exception as e:
        return ""

if __name__ == "__main__":
    print("Scraping TopJobs.lk...")
    jobs = scrape_jobs()

    if jobs:
        df = pd.DataFrame(jobs)
        df.to_csv("jobs_raw.csv", index=False)
        print(f"Saved {len(df)} jobs to jobs_raw.csv")

        # Test detail scraping on first 3 jobs with valid URLs
        print("\nTesting detail page scraping on 3 jobs...")
        sample = df[df["detail_url"] != ""].head(3)
        for _, row in sample.iterrows():
            print(f"\nJob: {row['title']}")
            print(f"URL: {row['detail_url']}")
            detail = scrape_job_detail(row["detail_url"])
            print(f"Description preview: {detail[:200]}")
            time.sleep(1) 