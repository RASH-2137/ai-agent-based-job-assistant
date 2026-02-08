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
        )
    return _llm


def get_jd_analyst_agent():
    return Agent(
        role="Job Description Analyst",
        goal="Analyze job descriptions and extract responsibilities, required skills, and qualifications",
        backstory="You are an expert HR analyst who breaks down job descriptions into clear, structured insights.",
        llm=_get_llm(),
        verbose=False,
        max_iter=1,
        allow_delegation=False,
    )


def create_jd_analysis_task(agent, description):
    return Task(
        description=(
            "Analyze the following job description and extract key details.\n\n"
            f"Job Description:\n{description}\n\n"
            "Provide the output in structured markdown with the following sections:\n"
            "## Responsibilities\n"
            "## Required Skills\n"
            "## Qualifications"
        ),
        agent=agent,
        expected_output=(
            "A markdown-formatted report with clear sections for "
            "Responsibilities, Required Skills, and Qualifications."
        ),
        output_file="data/report.md"
    )
