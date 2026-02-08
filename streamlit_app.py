import streamlit as st

from usajobs_api import fetch_usajobs
from orchestrator import run_pipeline


st.title("Job Hunt Assistant")
st.markdown("Search USAJOBS, select listings, and run the pipeline to get a tailored resume summary, cover letter, and outreach message.")

job_keyword = st.text_input("Job keyword", placeholder="e.g. data analyst")
job_location = st.text_input(
    "Location (optional – leave blank for nationwide)",
    placeholder="e.g. Washington DC",
)
resume_text = st.text_area("Resume text", height=200, placeholder="Paste your resume text here.")
user_bio = st.text_input(
    "Short bio",
    placeholder="e.g. Data analyst with 3 years in public sector",
)

# Fetch jobs
if st.button("🔍 Fetch Jobs"):
    if not resume_text.strip():
        st.error("Please enter your resume text.")
    else:
        jobs, err = fetch_usajobs(job_keyword, location=job_location or None, results_per_page=10)
        if err:
            st.error(err)
            st.session_state.jobs = []
            st.session_state.jobs_error = err
        else:
            st.session_state.jobs_error = None
            st.session_state.jobs = jobs[:10] if jobs else []
            if not st.session_state.jobs:
                st.info("No jobs found for that keyword. Try a different term or leave location blank for nationwide search.")

# Job selection
selected_jobs = []

if "jobs" in st.session_state and st.session_state.jobs:
    st.subheader("Available Jobs")

    for idx, job in enumerate(st.session_state.jobs):
        descriptor = job.get("MatchedObjectDescriptor", {})
        title = descriptor.get("PositionTitle", "Job Title")
        agency = descriptor.get("OrganizationName", "Agency")

        if st.checkbox(f"{title} — {agency}", key=f"job_{idx}"):
            selected_jobs.append(job)

# Run pipeline for selected jobs
if st.button("🚀 Apply to Selected Jobs"):
    if not selected_jobs:
        st.warning("Please select at least one job.")
    else:
        for job in selected_jobs:
            descriptor = job.get("MatchedObjectDescriptor", {})
            title = descriptor.get("PositionTitle", "Job")

            st.markdown(f"## 📄 {title}")

            with st.spinner("Running pipeline..."):
                try:
                    result = run_pipeline(
                        job_data=job,
                        resume_text=resume_text,
                        user_bio=user_bio,
                    )
                    st.markdown(result)
                except ValueError as e:
                    st.error(str(e))
