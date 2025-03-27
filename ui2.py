import streamlit as st
import requests
import os

# Set up Databricks Token
DATABRICKS_TOKEN = os.getenv("DATABRICKS_TOKEN", "your-databricks-token-here")
API_URL = "https://your-databricks-api-endpoint"

# Streamlit UI
st.set_page_config(page_title="Job Analyzer", layout="centered")

st.title("🔍 Job Description Analyzer")
st.write("Paste a job description and get instant insights!")

job_description = st.text_area("Enter job description:", height=150)

if st.button("Analyze"):
    if not job_description.strip():
        st.error("⚠ Please enter a job description.")
    else:
        st.info("🔄 Analyzing... Please wait.")
        headers = {"Authorization": f"Bearer {DATABRICKS_TOKEN}", "Content-Type": "application/json"}
        payload = {"job_description": job_description}

        try:
            response = requests.post(API_URL, json=payload, headers=headers)
            if response.status_code == 200:
                data = response.json()
                st.success("✅ Analysis Complete!")

                # Display Insights
                st.subheader("📌 Job Overview & Ratings")
                st.write(f"*Title:* {data.get('job_title', 'N/A')}")
                st.write(f"*Company:* {data.get('company', 'N/A')}")
                st.write(f"*Salary:* {data.get('salary', 'Not mentioned')}")

                # Ratings
                ratings = data.get("ratings", {})
                st.progress(ratings.get("salary_transparency", 0) / 10)
                st.write(f"*Salary Transparency:* {ratings.get('salary_transparency', 0)}/10")
                st.write(f"*Work-Life Balance:* {ratings.get('work_life_balance', 0)}/10")
                st.write(f"*Career Growth:* {ratings.get('career_growth', 0)}/10")
                st.write(f"*Toxic Culture Risk:* {ratings.get('toxic_culture_risk', 0)}/10")

                # Red Flags
                st.subheader("⚠ Red Flags & Risk Score")
                red_flags = data.get("red_flags", [])
                st.write(", ".join(red_flags) if red_flags else "No major red flags detected.")
                st.progress(data.get("red_flag_score", 0) / 10)

                # Job Score
                st.subheader("💼 Job Worth Score")
                st.write(f"*Score:* {data.get('job_score', 0)}/100")
                st.success(f"*Verdict:* {data.get('verdict', 'N/A')}")

                # Suggested Interview Questions
                st.subheader("💡 Questions to Ask")
                questions = data.get("interview_questions", {}).get("candidate_should_ask", [])
                for q in questions:
                    st.write(f"- {q}")

            else:
                st.error(f"❌ API Error: {response.status_code} - {response.text}")

        except requests.exceptions.RequestException as e:
            st.error(f"❌ Request Failed: {e}")import streamlit as st
import requests
import os

# Set up Databricks Token
DATABRICKS_TOKEN = os.getenv("DATABRICKS_TOKEN", "your-databricks-token-here")
API_URL = "https://your-databricks-api-endpoint"

# Streamlit UI
st.set_page_config(page_title="Job Analyzer", layout="centered")

st.title("🔍 Job Description Analyzer")
st.write("Paste a job description and get instant insights!")

job_description = st.text_area("Enter job description:", height=150)

if st.button("Analyze"):
    if not job_description.strip():
        st.error("⚠ Please enter a job description.")
    else:
        st.info("🔄 Analyzing... Please wait.")
        headers = {"Authorization": f"Bearer {DATABRICKS_TOKEN}", "Content-Type": "application/json"}
        payload = {"job_description": job_description}

        try:
            response = requests.post(API_URL, json=payload, headers=headers)
            if response.status_code == 200:
                data = response.json()
                st.success("✅ Analysis Complete!")

                # Display Insights
                st.subheader("📌 Job Overview & Ratings")
                st.write(f"*Title:* {data.get('job_title', 'N/A')}")
                st.write(f"*Company:* {data.get('company', 'N/A')}")
                st.write(f"*Salary:* {data.get('salary', 'Not mentioned')}")

                # Ratings
                ratings = data.get("ratings", {})
                st.progress(ratings.get("salary_transparency", 0) / 10)
                st.write(f"*Salary Transparency:* {ratings.get('salary_transparency', 0)}/10")
                st.write(f"*Work-Life Balance:* {ratings.get('work_life_balance', 0)}/10")
                st.write(f"*Career Growth:* {ratings.get('career_growth', 0)}/10")
                st.write(f"*Toxic Culture Risk:* {ratings.get('toxic_culture_risk', 0)}/10")

                # Red Flags
                st.subheader("⚠ Red Flags & Risk Score")
                red_flags = data.get("red_flags", [])
                st.write(", ".join(red_flags) if red_flags else "No major red flags detected.")
                st.progress(data.get("red_flag_score", 0) / 10)

                # Job Score
                st.subheader("💼 Job Worth Score")
                st.write(f"*Score:* {data.get('job_score', 0)}/100")
                st.success(f"*Verdict:* {data.get('verdict', 'N/A')}")

                # Suggested Interview Questions
                st.subheader("💡 Questions to Ask")
                questions = data.get("interview_questions", {}).get("candidate_should_ask", [])
                for q in questions:
                    st.write(f"- {q}")

            else:
                st.error(f"❌ API Error: {response.status_code} - {response.text}")

        except requests.exceptions.RequestException as e:
            st.error(f"❌ Request Failed: {e}")