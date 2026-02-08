import os

from dotenv import load_dotenv

# Resolve possible project roots (app may be run from a different working directory)
_utils_dir = os.path.dirname(os.path.abspath(__file__))
_project_root_from_file = os.path.dirname(_utils_dir)
_cwd = os.getcwd()

# Load .env from every likely location so it works regardless of run context
for _dir in (_project_root_from_file, _cwd, os.path.dirname(_cwd)):
    if _dir:
        _env_file = os.path.join(_dir, ".env")
        if os.path.isfile(_env_file):
            load_dotenv(dotenv_path=_env_file)
load_dotenv()  # dotenv default: cwd and parents

# If keys still missing, try manual parse from first .env we find (handles encoding/parsing quirks)
def _load_env_manually():
    for _dir in (_project_root_from_file, _cwd):
        _env_file = os.path.join(_dir, ".env")
        if os.path.isfile(_env_file):
            try:
                with open(_env_file, "r", encoding="utf-8", errors="replace") as f:
                    for line in f:
                        line = line.strip().replace("\r", "")
                        if line and not line.startswith("#") and "=" in line:
                            k, _, v = line.partition("=")
                            k, v = k.strip().strip("\r"), v.strip().strip("\r")
                            if k and v and os.getenv(k) in (None, ""):
                                if len(v) >= 2 and v[0] in ("'", '"') and v[0] == v[-1]:
                                    v = v[1:-1].strip()
                                os.environ.setdefault(k, v)
            except Exception:
                pass
            break

_load_env_manually()


def _normalize_env(key):
    """Read env var and strip whitespace + optional surrounding quotes (handles KEY = \"value\" format)."""
    val = os.getenv(key)
    if val is None:
        return None
    s = str(val).strip()
    if len(s) >= 2 and ((s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'"))):
        s = s[1:-1].strip()
    return s if s else None


USAJOBS_API_KEY = _normalize_env("USAJOBS_API_KEY")
# Library accepts GOOGLE_API_KEY or GEMINI_API_KEY; prefer GEMINI for this project
GEMINI_API_KEY = _normalize_env("GEMINI_API_KEY") or _normalize_env("GOOGLE_API_KEY")


def _env_locations_checked():
    """Paths where we looked for .env (for error messages)."""
    locs = [os.path.join(_project_root_from_file, ".env"), os.path.join(_cwd, ".env")]
    return [p for p in locs if p]


def require_gemini_api_key():
    """Return the Gemini API key, or raise a clear error if missing (e.g. .env not set)."""
    key = (GEMINI_API_KEY or "").strip()
    if not key:
        locs = _env_locations_checked()
        raise ValueError(
            "Gemini API key is missing.\n\n"
            "• Put GEMINI_API_KEY=your_key in a .env file (one variable per line, no spaces around =).\n"
            "• App looked for .env here: " + ("; ".join(locs) if locs else "(unknown)") + "\n"
            "• Get a key: https://aistudio.google.com/apikey"
        )
    return key