# Job Hunt Assistant

A Streamlit app to streamline applying to federal jobs on USAJOBS: search by keyword, pick listings, and run a pipeline (CrewAI + Google Gemini) to get a tailored resume summary, cover letter, and outreach message. Runs locally; you supply your own API keys.

## Architecture

- **Streamlit UI** (`streamlit_app.py`): Keyword search, resume/bio inputs, job selection, and "Apply to Selected Jobs" to run the pipeline per job.
- **USAJOBS API** (`usajobs_api.py`): Fetches listings from the official USAJOBS API.
- **Orchestrator** (`orchestrator.py`): For each selected job, runs a sequential Crew of three agents, parses output (markers `<<RESUME_SUMMARY>>`, `<<COVER_LETTER>>`), logs the application, and saves the cover letter under `data/`.
- **Agents** (`agents/`): JD Analyst (job description → responsibilities, skills, qualifications); Resume & Cover Letter (tailored summary + government-style cover letter); Messaging (short outreach for recruiters). All use Google Gemini (2.0/2.5 Flash).
- **Utils**: Config loads `.env` for `USAJOBS_API_KEY` and `GEMINI_API_KEY`. Tracking writes cover letters to `data/cover_letters/` and appends to `data/applications_log.csv`.

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

## Notes

- **API keys:** You need a [USAJOBS API key](https://developer.usajobs.gov/APIRequest/Register) and a [Gemini API key](https://aistudio.google.com/apikey). Put them in `.env` (copy from `.env.example`). No mock mode; the app calls real APIs.
- **Scope:** Built for USAJOBS federal listings. Output quality depends on the LLM (Gemini); always review generated cover letters and messages before sending.
- **Data:** All generated files (cover letters, application log) live under `data/`. No data is sent except to USAJOBS and Google as required for search and generation.

## License

Use and modify as needed. USAJOBS and Google APIs are subject to their respective terms of use.
