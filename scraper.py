import requests
from bs4 import BeautifulSoup
import pandas as pd

BASE_URL = "https://www.topjobs.lk/applicant/vacancybyfunctionalarea.jsp"

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
    for row in rows:
        cols = row.find_all("td")
        if len(cols) < 5:
            continue

        # Col 2: title is in <h2><span>, company is in <h1>
        col2 = cols[2]
        h2 = col2.find("h2")
        h1 = col2.find("h1")
        title   = h2.get_text(strip=True) if h2 else ""
        company = h1.get_text(strip=True) if h1 else ""

        job = {
            "ref_no":       cols[1].get_text(strip=True),
            "title":        title,
            "company":      company,
            "description":  cols[3].get_text(strip=True),
            "opening_date": cols[4].get_text(strip=True),
            "closing_date": cols[5].get_text(strip=True),
        }
        jobs.append(job)

    return jobs

if __name__ == "__main__":
    print("Scraping TopJobs.lk...")
    jobs = scrape_jobs()

    if jobs:
        df = pd.DataFrame(jobs)
        df.to_csv("jobs_raw.csv", index=False)
        print(f"Saved {len(df)} jobs to jobs_raw.csv")
        print(df[["title", "company", "description"]].head(10))
        print("\nNull counts:\n", df.isnull().sum())
    else:
        print("No jobs found.")