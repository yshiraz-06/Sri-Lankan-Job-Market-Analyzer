import pandas as pd
import re

df = pd.read_csv("jobs_raw.csv")
print(f"Raw jobs: {len(df)}")

df = df.drop_duplicates(subset=["ref_no"])
print(f"After removing duplicates: {len(df)}")

# Sri Lankan locations whitelist
SL_LOCATIONS = [
    "Colombo", "Gampaha", "Kandy", "Galle", "Negombo", "Matara",
    "Jaffna", "Kurunegala", "Ratnapura", "Badulla", "Anuradhapura",
    "Trincomalee", "Batticaloa", "Hambantota", "Kalutara", "Kegalle",
    "Matale", "Nuwara Eliya", "Polonnaruwa", "Puttalam", "Ampara",
    "Mullaitivu", "Vavuniya", "Mannar", "Kilinochchi", "Ja Ela",
    "Ja-Ela", "Wattala", "Panadura", "Moratuwa", "Dehiwala",
    "Mount Lavinia", "Nugegoda", "Maharagama", "Kaduwela", "Malabe",
    "Ragama", "Minuwangoda", "Katunayake", "Seeduwa", "Ekala",
    "Peliyagoda", "Kelaniya", "Kadawatha", "Biyagama", "Horana",
    "Piliyandala", "Boralesgamuwa", "Nawala", "Rajagiriya", "Battaramulla",
    "Kotte", "Sri Jayawardenepura", "Nawinna", "Athurugiriya", "Hokandara"
]

def extract_location(title):
    title_lower = title.lower()
    for loc in SL_LOCATIONS:
        if loc.lower() in title_lower:
            return loc
    return "Not Specified"

def clean_title(title):
    # Remove " - anything (count)" suffix
    cleaned = re.sub(r'\s*-\s*[^(]+\s*\(\d+\)\s*$', '', title)
    # Remove just " (count)" suffix
    cleaned = re.sub(r'\s*\(\d+\)\s*$', '', cleaned)
    return cleaned.strip()

df["location"] = df["title"].apply(extract_location)
df["title_clean"] = df["title"].apply(clean_title)

df["opening_date"] = pd.to_datetime(df["opening_date"], errors="coerce")
df["closing_date"] = pd.to_datetime(df["closing_date"], errors="coerce")

df["company"] = df["company"].str.strip()
df["title_clean"] = df["title_clean"].str.strip()
df = df[df["title_clean"] != ""]

df.to_csv("jobs_clean.csv", index=False)
print(f"Cleaned jobs saved: {len(df)}")
print("\nLocation value counts (top 10):")
print(df["location"].value_counts().head(10))