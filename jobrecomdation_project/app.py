import streamlit as st
from model import recommend_jobs

st.set_page_config(page_title="Job Recommender", layout="centered")

st.title("💼 Job Recommendation System")
st.write("Enter your skills to get job suggestions")

# Input
user_input = st.text_input("Enter skills (e.g. Python, ML, SQL)")

# Button
if st.button("Get Recommendations"):
    if user_input.strip() == "":
        st.warning("Please enter some skills")
    else:
        results = recommend_jobs(user_input)

        st.subheader("🎯 Recommended Jobs:")

        for job in results:
            st.write(f"### {job['title']}")
            st.write(f"Skills: {job['skills']}")
            st.write(f"Match Score: {job['score']}")
            st.markdown("---")