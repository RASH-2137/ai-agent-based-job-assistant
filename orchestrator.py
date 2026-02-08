from crewai import Crew, Process

from agents.jd_analyst import (
    get_jd_analyst_agent,
    create_jd_analysis_task,
)
from agents.messaging_agent import (
    get_messaging_agent,
    create_messaging_task,
)
from agents.resume_cl_agent import (
    get_resume_cl_agent,
    create_resume_cl_task,
)
from utils.tracking import (
    log_application,
    save_cover_letter_file,
)



def extract_between_markers(text, start_marker, end_marker):
    """Extract text between two markers. If end_marker is empty or missing, returns rest of text after start."""
    try:
        start = text.index(start_marker) + len(start_marker)
        if not end_marker:
            return text[start:].strip()
        end = text.index(end_marker)
        return text[start:end].strip()
    except ValueError:
        return ""







def run_pipeline(job_data, resume_text, user_bio):
    """
    Runs the full agent workflow for ONE selected job.
    """

    descriptor = job_data.get("MatchedObjectDescriptor", {})

    job_summary = (
        descriptor.get("UserArea", {})
                  .get("Details", {})
                  .get("JobSummary", "")
    )

    agency_name = descriptor.get("OrganizationName", "Government Agency")
    job_title = descriptor.get("PositionTitle", "Job Role")

    if not job_summary:
        return "❌ Job summary not found."

    # Create agents
    jd_agent = get_jd_analyst_agent()
    resume_agent = get_resume_cl_agent()
    messaging_agent = get_messaging_agent()

    # Create tasks
    jd_task = create_jd_analysis_task(jd_agent, job_summary)

    resume_task = create_resume_cl_task(
        resume_agent,
        job_summary,
        resume_text
    )

    messaging_task = create_messaging_task(
        messaging_agent,
        job_summary,
        agency_name,
        user_bio
    )

    # Run Crew
    crew = Crew(
        agents=[jd_agent, resume_agent, messaging_agent],
        tasks=[jd_task, resume_task, messaging_task],
        process=Process.sequential,
        verbose=False
    )

    result = crew.kickoff()

    # -----------------------------
    # Extract resume agent output
    # -----------------------------
    resume_output = str(resume_task.output)

    resume_summary = extract_between_markers(
        resume_output,
        "<<RESUME_SUMMARY>>",
        "<<COVER_LETTER>>"
    )

    cover_letter = extract_between_markers(
        resume_output,
        "<<COVER_LETTER>>",
        "<<END>>" if "<<END>>" in resume_output else None,
    )

    # -----------------------------
    # Log application
    # -----------------------------
    log_application(
        job_title=job_title,
        agency=agency_name,
        resume_summary=resume_summary
    )

    # -----------------------------
    # Save cover letter file
    # -----------------------------
    save_cover_letter_file(
        job_title=job_title,
        agency=agency_name,
        cover_letter_text=cover_letter
    )

    return result



