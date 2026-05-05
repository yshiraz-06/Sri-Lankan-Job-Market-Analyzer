import streamlit as st
import pandas as pd
import plotly.express as px
from collections import Counter

st.set_page_config(
    page_title="Sri Lankan Job Market Analyzer",
    page_icon="LK",
    layout="wide",
)

st.title("Sri Lankan Job Market Analyzer")
st.markdown("Real-time analysis of tech job demand in Sri Lanka based on web-scraped data from **TopJobs.lk** and **ITPro.lk**.")

# Load Data
@st.cache_data
def load_data():
    topjobs = pd.read_csv("jobs_clean.csv")
    itpro = pd.read_csv("itpro_jobs.csv")
    skill_topjobs = pd.read_csv("skill_counts.csv")
    skill_itpro = pd.read_csv("itpro_skill_counts.csv")
    return topjobs, itpro, skill_topjobs, skill_itpro

topjobs, itpro, skill_topjobs, skill_itpro = load_data()

# Sidebar
st.sidebar.header("Filters")
source = st.sidebar.radio("Data Source", ["TopJobs.lk (All Jobs)", "ITPro.lk (Tech Jobs)", "Both"])
top_n = st.sidebar.slider("Top N Skills to Display", 5, 30, 15) 

# Metrics Row
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("TopJobs Listings", f"{len(topjobs):,}")
col2.metric("ITPro Listings",   f"{len(itpro):,}")
col3.metric("Total Jobs",       f"{len(topjobs) + len(itpro):,}")
col4.metric("Tech Categories",  f"{itpro['category'].nunique()}")
intern_count = int(skill_itpro[skill_itpro["skill"] == "Internship"]["count"].sum())
col5.metric("Internship Roles", f"{intern_count}")

st.divider()

# Skill Demand Chart
st.subheader("Top In-Demand Skills/Roles")

if source == "ITPro.lk (Tech Jobs)":
    skill_df = skill_itpro.query("skill != 'Internship'").head(top_n)
    subtitle = "Source: ITPro.lk"
elif source == "TopJobs.lk (All Jobs)":
    skill_df = skill_topjobs.query("skill != 'Internship'").head(top_n)
    subtitle = "Source: TopJobs.lk"
else:
    merged = pd.concat([skill_topjobs, skill_itpro]).groupby("skill")["count"].sum().reset_index()
    merged["percentage"] = (merged["count"] / (len(topjobs) + len(itpro)) * 100).round(1)
    skill_df = merged.sort_values("count", ascending=False).query("skill != 'Internship'").head(top_n)
    subtitle = "Source: ITPro.lk + TopJobs.lk"

fig = px.bar(
    skill_df.query("skill != 'Internship'").sort_values("count"),
    x="count", y="skill", orientation="h",
    title=f"Top {top_n} In-Demand Skills - {subtitle}",
    labels={"count": "Number of Job Listings", "skill": "Skill"},
    color="count", color_continuous_scale="Blues",
    text="count"
)

fig.update_traces(textposition="outside")
fig.update_layout(height=500, showlegend=False, coloraxis_showscale=False)
st.plotly_chart(fig, use_container_width=True)

st.divider()

#Two Column Section
left, right = st.columns(2)

with left:
    st.subheader("Jobs by Category (ITPro.lk)")
    cats_counts = itpro["category"].value_counts().reset_index()
    cats_counts.columns = ["category", "count"]
    fig2 = px.pie(cats_counts, names="category", values="count",
                   title="Tech Job distribution by Category (ITPro.lk)",
                   hole=0.4
    )
    fig2.update_layout(height=400)
    st.plotly_chart(fig2, use_container_width=True)

with right:
    st.subheader("Jobs by Location (TopJobs.lk)")
    loc = topjobs[
        (topjobs["location"] != "Not Specified") & 
        (topjobs["location"].notna()) &
        (topjobs["location"] != "")]["location"].value_counts().head(10).reset_index()
    loc.columns = ["location", "count"]
    fig3 = px.bar(loc, x="location", y="count", title="Top 10 Hiring Locations",
                  color = "count", color_continuous_scale="Greens"
    )
    fig3.update_layout(height=400, coloraxis_showscale=False)
    st.plotly_chart(fig3, use_container_width=True)

st.divider()

# Job Table
st.subheader("Browse Job Listings")

tab1, tab2 = st.tabs(["ITPro.lk", "TopJobs.lk"])

with tab1:
    category_filter = st.selectbox("Filter by Category", ["All"] + sorted(itpro["category"].unique().tolist()))
    filtered = itpro if category_filter == "All" else itpro[itpro["category"] == category_filter]
    st.dataframe(
        filtered[["title", "company", "location", "category", "date"]].reset_index(drop=True),
        use_container_width=True, height=400
    )

with tab2:
    search = st.text_input("Search Job Titles")
    filtered2 = topjobs[topjobs["title_clean"].str.contains(search, case=False, na=False)] if search else topjobs
    st.dataframe(
        filtered2[["title_clean", "company", "location", "opening_date", "closing_date"]].reset_index(drop=True),
        use_container_width=True, height=400
    )

st.caption("Data Scraped from TopJobs.lk and ITPro.lk - Built by Yahya Shiraz")

