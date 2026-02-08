from crewai import Agent, Task
from langchain_google_genai import ChatGoogleGenerativeAI

from utils.config import require_gemini_api_key

_llm = None


def _get_llm():
    global _llm
    if _llm is None:
        _llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            api_key=require_gemini_api_key(),
            temperature=0.5,
        )
    return _llm


def get_messaging_agent():
    """Agent that writes short, professional outreach messages for recruiters or hiring managers."""
    return Agent(
        role="Outreach Messaging Specialist",
        goal=(
            "Write concise, professional outreach messages that express "
            "interest in a job and highlight candidate relevance."
        ),
        backstory=(
            "You are an expert career communication assistant skilled at "
            "writing polite, effective outreach messages suitable for "
            "LinkedIn or professional email communication."
        ),
        llm=_get_llm(),
        verbose=True,
    )


def create_messaging_task(agent, job_summary, agency_name, user_bio):
    """Task: generate a short outreach message tailored to job, agency, and candidate bio."""

    prompt = f"""
You are given:
- A job summary
- The hiring agency or organization
- A short candidate bio

Write a brief, professional outreach message that the candidate
can send to a recruiter or hiring manager.

Guidelines:
- Keep the message concise and polite
- Express genuine interest in the role and agency
- Briefly connect the candidate's background to the role
- Suitable for LinkedIn message or professional email
- Do NOT exceed 150 words

Job Summary:
{job_summary}

Agency:
{agency_name}

Candidate Bio:
{user_bio}
"""

    return Task(
        description=prompt,
        agent=agent,
        expected_output=(
            "A concise, professional outreach message under 150 words, "
            "tailored for LinkedIn or email communication."
        )
    )