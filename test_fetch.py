import requests
from bs4 import BeautifulSoup

url = "https://www.topjobs.lk/applicant/vacancybyfunctionalarea.jsp"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
}

response = requests.get(url, headers=headers)
print("Status code:", response.status_code)
print("Page length:", len(response.text))

# Check if the table is present
soup = BeautifulSoup(response.text, "html.parser")
table = soup.find("table", {"id": "tbldata_2"})
print("Table found:", table is not None)

tables = soup.find_all("table")
for t in tables:
    print("Table id:", t.get("id"), "| class:", t.get("class"))