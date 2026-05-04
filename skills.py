import pandas as pd
import re
from collections import Counter

df = pd.read_csv("jobs_clean.csv")

SKILLS = {
    # Programming Languages
    "Python":           [r"\bpython\b"],
    "Java":             [r"\bjava\b"],
    "JavaScript":       [r"\bjavascript\b", r"\bjs\b"],
    "TypeScript":       [r"\btypescript\b"],
    "C#":               [r"\bc#\b", r"\bcsharp\b"],
    "C++":              [r"\bc\+\+\b"],
    "PHP":              [r"\bphp\b"],
    "R":                [r"\brstudio\b", r"\br programming\b"],
    "Swift":            [r"\bswift\b"],
    "Kotlin":           [r"\bkotlin\b"],
    "Go":               [r"\bgolang\b"],
    "Ruby":             [r"\bruby\b"],

    # Data & ML
    "SQL":              [r"\bsql\b", r"\bmysql\b", r"\bpostgresql\b", r"\boracle\b"],
    "Machine Learning": [r"\bmachine learning\b", r"\b ml \b"],
    "Deep Learning":    [r"\bdeep learning\b"],
    "TensorFlow":       [r"\btensorflow\b"],
    "PyTorch":          [r"\bpytorch\b"],
    "Keras":            [r"\bkeras\b"],
    "Pandas":           [r"\bpandas\b"],
    "NumPy":            [r"\bnumpy\b"],
    "Scikit-learn":     [r"\bscikit-learn\b", r"\bsklearn\b"],
    "Computer Vision":  [r"\bcomputer vision\b", r"\bopencv\b", r"\bimage processing\b"],
    "NLP":              [r"\bnlp\b", r"\bnatural language processing\b"],
    "Data Analysis":    [r"\bdata anal", r"\bdata scientist\b"],
    "Power BI":         [r"\bpower bi\b", r"\bpowerbi\b"],
    "Tableau":          [r"\btableau\b"],

    # Cloud & DevOps
    "AWS":              [r"\baws\b", r"\bamazon web services\b"],
    "Azure":            [r"\bazure\b"],
    "GCP":              [r"\bgcp\b", r"\bgoogle cloud\b"],
    "Docker":           [r"\bdocker\b"],
    "Kubernetes":       [r"\bkubernetes\b", r"\bk8s\b"],
    "Git":              [r"\bgit\b", r"\bgithub\b", r"\bgitlab\b"],
    "CI/CD":            [r"\bci/cd\b", r"\bjenkins\b", r"\bgithub actions\b"],
    "Linux":            [r"\blinux\b", r"\bunix\b"],

    # Web & Frameworks
    "React":            [r"\breact\b", r"\breactjs\b"],
    "Angular":          [r"\bangular\b"],
    "Vue.js":           [r"\bvue\b", r"\bvuejs\b"],
    "Node.js":          [r"\bnode\.js\b", r"\bnodejs\b"],
    "Django":           [r"\bdjango\b"],
    "Flask":            [r"\bflask\b"],
    "Spring Boot":      [r"\bspring boot\b", r"\bspring\b"],
    "REST API":         [r"\brest api\b", r"\brestful\b"],

    # Databases
    "MongoDB":          [r"\bmongodb\b", r"\bmongo\b"],
    "Redis":            [r"\bredis\b"],

    # Roles & Soft Skills
    "Agile":            [r"\bagile\b", r"\bscrum\b", r"\bkanban\b"],
    "Excel":            [r"\bexcel\b"],
    "Project Management": [r"\bproject management\b", r"\bpmp\b"],
    "QA/Testing":       [r"\bquality assurance\b", r"\bqa\b", r"\btesting\b", r"\bselenium\b"],
    "UI/UX":            [r"\bui/ux\b", r"\bfigma\b", r"\bui design\b", r"\bux design\b"],
    "Network/Security": [r"\bnetwork\b", r"\bcybersecurity\b", r"\bsecurity engineer\b"],
    "DevOps":           [r"\bdevops\b"],
    "Data Engineer":    [r"\bdata engineer\b", r"\betl\b", r"\bpipeline\b"],
    "Business Analyst": [r"\bbusiness analyst\b", r"\bbusiness analysis\b"],
    "Mobile Dev":       [r"\bmobile\b", r"\bandroid\b", r"\bios developer\b", r"\bflutter\b", r"\breact native\b"],
    "Internship":       [r"\bintern\b", r"\btrainee\b", r"\bgraduate\b"],
}

def extract_skills(text):
    if pd.isna(text):
        return []
    text = text.lower()
    found = []
    for skill, patterns in SKILLS.items():
        for pattern in patterns:
            if re.search(pattern, text):
                found.append(skill)
                break
    return found

# Only use title since descriptions are empty
df["skills_found"] = df["title_clean"].apply(extract_skills)

all_skills = [s for skills in df["skills_found"] for s in skills]
skill_counts = Counter(all_skills)

print("Top 20 in-demand skills/roles in Sri Lankan job market:")
for skill, count in skill_counts.most_common(20):
    pct = round((count / len(df)) * 100, 1)
    print(f"  {skill:<25} {count:>4} jobs  ({pct}%)")

skill_df = pd.DataFrame(skill_counts.most_common(), columns=["skill", "count"])
skill_df["percentage"] = (skill_df["count"] / len(df) * 100).round(1)
skill_df.to_csv("skill_counts.csv", index=False)
df.to_csv("jobs_clean.csv", index=False)

print(f"\nTotal jobs analyzed: {len(df)}")
print(f"Jobs with at least one skill tag: {df['skills_found'].apply(len).gt(0).sum()}")

# ITPro skill analysis 
df2 = pd.read_csv("itpro_jobs.csv")

df2["skills_found"] = df2["title"].apply(extract_skills)

all_skills2 = [s for skills in df2["skills_found"] for s in skills]
skill_counts2 = Counter(all_skills2)

print("\n── ITPro.lk: Top 20 in-demand TECH skills ──")
for skill, count in skill_counts2.most_common(20):
    pct = round((count / len(df2)) * 100, 1)
    print(f"  {skill:<25} {count:>4} jobs  ({pct}%)")

skill_df2 = pd.DataFrame(skill_counts2.most_common(), columns=["skill", "count"])
skill_df2["percentage"] = (skill_df2["count"] / len(df2) * 100).round(1)
skill_df2.to_csv("itpro_skill_counts.csv", index=False)
print(f"\nSaved to itpro_skill_counts.csv")