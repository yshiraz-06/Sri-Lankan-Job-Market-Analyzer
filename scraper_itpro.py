import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
}

CATEGORIES = {
    "Software Engineering":     "https://itpro.lk/jobs/software-engineering/",
    "Quality Assurance":        "https://itpro.lk/jobs/quality-assurance/",
    "Web Development":          "https://itpro.lk/jobs/web-development/",
    "Mobile Development":       "https://itpro.lk/jobs/mobile-development/",
    "IT and Operations":        "https://itpro.lk/jobs/information-technology/",
    "DevOps and Cloud":         "https://itpro.lk/jobs/devops-cloud/",
    "AI and Data":              "https://itpro.lk/jobs/ai-and-data/",
    "Management and Business":  "https://itpro.lk/jobs/management-business/",
    "Design and Creative":      "https://itpro.lk/jobs/design-creative/",
    "Digital Marketing":        "https://itpro.lk/jobs/digital-marketing/",
    "Hardware and Networking":  "https://itpro.lk/jobs/hardware-networking/",
}

def scrape_category(url, category):
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")
    cards = soup.find_all("article", class_="job-card")

    jobs = []
    for card in cards:
        title_tag = card.find(["h2", "h3", "a"])
        title = title_tag.get_text(strip=True) if title_tag else ""

        company_tag = card.find(class_=lambda x: x and "company" in x.lower())
        company = company_tag.get_text(strip=True) if company_tag else ""

        location_tag = card.find(class_=lambda x: x and "location" in x.lower())
        location = location_tag.get_text(strip=True) if location_tag else ""

        date_tag = card.find("time")
        date = date_tag.get("datetime", date_tag.get_text(strip=True)) if date_tag else ""

        full_text = card.get_text(separator=" ", strip=True)

        jobs.append({
            "title": title,
            "company": company,
            "location": location,
            "date": date,
            "category": category,
            "full_text": full_text,
            "source": "itpro.lk"
        })

    return jobs

if __name__ == "__main__":
    all_jobs = []

    for category, url in CATEGORIES.items():
        print(f"Scraping: {category}")
        jobs = scrape_category(url, category)
        print(f"  → {len(jobs)} jobs")
        all_jobs.extend(jobs)
        time.sleep(1)

    df = pd.DataFrame(all_jobs)
    df = df.drop_duplicates(subset=["title", "company"])
    df.to_csv("itpro_jobs.csv", index=False)

    print(f"\nTotal saved: {len(df)} jobs")
    print("\nJobs by category:")
    print(df["category"].value_counts())
    print("\nSample titles:")
    print(df["title"].head(15).to_string())