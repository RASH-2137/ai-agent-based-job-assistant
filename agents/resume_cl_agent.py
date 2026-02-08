from crewai import Agent, Task
from langchain_google_genai import ChatGoogleGenerativeAI

from utils.config import require_gemini_api_key

_llm = None


def _get_llm():
    global _llm
    if _llm is None:
        _llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            api_key=require_gemini_api_key(),
            temperature=0.6,
        )
    return _llm


def get_resume_cl_agent():
    return Agent(
        role='Resume and Cover Letter Specialist',
        goal=(
            "tailor resumes and generate clear, professional, "
            "role-specific cover letters based on job descriptions."
        ),
        backstory=(
            "You are an expert career assistant wtih deep experience in "
            "goverment hiring processes, ATS-friendly resume writing, "
            "and professional cover letter drafting"
        ),
        llm=_get_llm(),
        verbose=True,
    )


def create_resume_cl_task(agent, job_summary, resume_text):
    # create a task that tailors a resume summary and generates a personalized
    # cover letter for a government job

    prompt = f"""
you are given:
1. A summarized job description
2. A candidate's current resume text

    Your tasks:
- Rewrite and tailor the candidate's RESUME SUMMARY to better align with the job.
- Generate a personalized COVER LETTER suitable for a GOVERNMENT job application.

Guidelines:
- Keep tone professional, formal, and clear.
- Emphasize relevant skills, experience, and alignment with public service.
- Avoid exaggeration or casual language.
- Do NOT repeat the entire resume.

Use the exact output markers below so the results can be parsed automatically.

<<RESUME_SUMMARY>>
(Write the tailored resume summary here)

<<COVER_LETTER>>
(Write the personalized government-style cover letter here)

Job Summary:
{job_summary}

Candidate Resume:
{resume_text}
"""

    return Task(
        description=prompt,
        agent=agent,
        expected_output=(
            "A tailored resume summary and a personalized government-style "
            "cover letter, clearly separated using the required markers."
        ),
        output_file="data/resume_agent_output.txt"
    )