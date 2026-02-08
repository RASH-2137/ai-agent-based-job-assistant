# AI Job Hunt Assistant

A local Streamlit app that uses **CrewAI** and **Google Gemini** to tailor your resume and cover letter for USAJOBS listings. You select jobs from search results and run a multi-agent pipeline to get a tailored resume summary, cover letter, and outreach message.

## Architecture

- **Streamlit UI** (`streamlit_app.py`): Job keyword search, resume/bio inputs, job selection, and "Apply to Selected Jobs" triggers the pipeline per job.
- **USAJOBS API** (`usajobs_api.py`): Fetches job listings from the official USAJOBS API (real API; requires `USAJOBS_API_KEY`).
- **Orchestrator** (`orchestrator.py`): For each selected job, builds a sequential Crew of three agents, runs them, parses the resume agent’s output (markers `<<RESUME_SUMMARY>>`, `<<COVER_LETTER>>`), then logs the application and saves the cover letter under `data/`.
- **Agents** (under `agents/`):
  - **JD Analyst** (`jd_analyst.py`): Analyzes job descriptions and outputs Responsibilities, Required Skills, Qualifications (Gemini 2.0 Flash).
  - **Resume & Cover Letter** (`resume_cl_agent.py`): Tailors resume summary and writes a government-style cover letter with fixed markers for parsing (Gemini 2.0 Flash).
  - **Messaging** (`messaging_agent.py`): Writes a short outreach message for recruiters/hiring managers (Gemini 2.5 Flash).
- **Utils**:
  - **Config** (`utils/config.py`): Loads `.env` from the project root; exposes `USAJOBS_API_KEY` and `GEMINI_API_KEY`.
  - **Tracking** (`utils/tracking.py`): Writes cover letters to `data/cover_letters/` and appends rows to `data/applications_log.csv`.

All APIs are **real** (Gemini + USAJOBS); there is no mock mode.

## Requirements

- Python 3.10+
- Virtual environment recommended (e.g. `venv`)

## Setup

1. **Clone or copy the project** and open a terminal in the project root (the folder that contains `streamlit_app.py`, `requirements.txt`, and the `agents`/`utils` directories).

2. **Create and activate a virtual environment** (Windows):

   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**:
   - Copy `.env.example` to `.env`.
   - Set `USAJOBS_API_KEY` (from [USAJOBS API Registration](https://developer.usajobs.gov/APIRequest/Register)).
   - Set `GEMINI_API_KEY` (from [Google AI Studio](https://aistudio.google.com/apikey)).

## Run the app

From the **project root** (same directory as `streamlit_app.py`):

```bash
python -m streamlit run streamlit_app.py
```

Then open the URL shown in the terminal (usually http://localhost:8501).

## Data and outputs

- **Input**: Resume text and short bio in the UI; job data comes from USAJOBS.
- **Outputs**:
  - Cover letters: `data/cover_letters/<JobTitle>_<Agency>_<timestamp>.txt`
  - Application log: `data/applications_log.csv` (Job Title, Agency, ResumeSummary, DateApplied)
  - Optional CrewAI task outputs: `data/report.md`, `data/resume_agent_output.txt` (if Crew writes them relative to project root)

## Project layout

```
project_root/
├── streamlit_app.py      # Streamlit entrypoint
├── orchestrator.py       # CrewAI pipeline for one job
├── usajobs_api.py        # USAJOBS API client
├── agents/
│   ├── jd_analyst.py
│   ├── resume_cl_agent.py
│   └── messaging_agent.py
├── utils/
│   ├── config.py         # .env and API keys
│   └── tracking.py       # Log + save cover letters
├── data/
│   ├── applications_log.csv
│   ├── cover_letters/
│   └── sample_resume.txt
├── .env.example
├── .env                  # Your keys (not committed)
├── requirements.txt
└── README.md
```

## License

Use and modify as needed for your job search. USAJOBS and Google APIs are subject to their respective terms of use.
