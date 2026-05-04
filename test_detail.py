import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
}

session = requests.Session()

# Get session cookie from main page
main = session.get("https://www.topjobs.lk/applicant/vacancybyfunctionalarea.jsp", headers=HEADERS)
jsessionid = session.cookies.get("JSESSIONID")
print("JSESSIONID:", jsessionid)

# Embed session ID directly in the URL (JSP style)
url = f"https://www.topjobs.lk/applicant/JobAdvertismentServlet;jsessionid={jsessionid}?AC=JOBADVERT&EC=0000000445&JC=0001496108"
print("Fetching:", url)

response = session.get(url, headers=HEADERS, allow_redirects=False)
print("Status:", response.status_code)
print("Location header:", response.headers.get("Location", "none"))

# If 200, parse it
if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")
    for tag in soup.find_all(["div", "td", "p"]):
        text = tag.get_text(strip=True)
        if len(text) > 80:
            print(f"\nTag: {tag.name} | class: {tag.get('class')} | id: {tag.get('id')}")
            print(f"Text: {text[:150]}")
else:
    print("Response body preview:", response.text[:300])