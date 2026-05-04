import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
}

response = requests.get("https://itpro.lk/", headers=HEADERS)
soup = BeautifulSoup(response.text, "html.parser")

print("Status:", response.status_code)
print("Page length:", len(response.text))

# Find all job listing containers
for tag in soup.find_all(["div", "article", "li", "a"]):
    text = tag.get_text(strip=True)
    cls = tag.get("class")
    if text and len(text) > 20 and len(text) < 200 and cls:
        print(f"Tag: {tag.name} | class: {cls} | text: {text[:100]}")