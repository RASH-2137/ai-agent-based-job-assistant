import csv
import os
import datetime
import re


def _data_dir():
    """Return project data directory (works when run from project root)."""
    # utils/tracking.py -> project root = parent of utils
    _this_dir = os.path.dirname(os.path.abspath(__file__))
    _project_root = os.path.dirname(_this_dir)
    return os.path.join(_project_root, "data")


def save_cover_letter_file(job_title, cover_letter_text, agency=None, directory=None):
    """
    Save cover letter to a file under data/cover_letters.
    job_title and optional agency are sanitized for the filename.
    """
    if directory is None:
        directory = os.path.join(_data_dir(), "cover_letters")
    safe_title = re.sub(r'[\\/*?:"<>|]', "_", (job_title or "").strip())
    safe_agency = re.sub(r'[\\/*?:"<>|]', "_", (agency or "").strip())
    os.makedirs(directory, exist_ok=True)
    base = f"{safe_title}_{safe_agency}" if safe_agency else safe_title
    base = base or "cover_letter"
    filename = f"{base}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    filepath = os.path.join(directory, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(cover_letter_text or "")
    return filepath


def log_application(job_title, agency, resume_summary, filepath=None):
    """Append one row to the applications log CSV under data/."""
    if filepath is None:
        filepath = os.path.join(_data_dir(), "applications_log.csv")
    dirpath = os.path.dirname(filepath)
    if dirpath:
        os.makedirs(dirpath, exist_ok=True)
    summary = (resume_summary or "").strip()[:150]
    exists = os.path.exists(filepath)
    with open(filepath, "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        if not exists:
            writer.writerow(["Job Title", "Agency", "ResumeSummary", "DateApplied"])
        writer.writerow([
            (job_title or "").strip(),
            (agency or "").strip(),
            summary,
            datetime.datetime.now().strftime("%Y%m%d_%H%M%S"),
        ])