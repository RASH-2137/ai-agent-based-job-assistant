import os

from dotenv import load_dotenv

_utils_dir = os.path.dirname(os.path.abspath(__file__))
_project_root_from_file = os.path.dirname(_utils_dir)
_cwd = os.getcwd()

for _dir in (_project_root_from_file, _cwd, os.path.dirname(_cwd)):
    if _dir:
        _env_file = os.path.join(_dir, ".env")
        if os.path.isfile(_env_file):
            load_dotenv(dotenv_path=_env_file)
load_dotenv()

def _load_env_manually():
    """Fallback: parse .env by hand if load_dotenv missed keys (e.g. encoding quirks)."""
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
    """Read env var; strip whitespace and optional surrounding quotes."""
    val = os.getenv(key)
    if val is None:
        return None
    s = str(val).strip()
    if len(s) >= 2 and ((s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'"))):
        s = s[1:-1].strip()
    return s if s else None


USAJOBS_API_KEY = _normalize_env("USAJOBS_API_KEY")
GEMINI_API_KEY = _normalize_env("GEMINI_API_KEY") or _normalize_env("GOOGLE_API_KEY")


def _env_locations_checked():
    """Paths checked for .env (used in error messages)."""
    locs = [os.path.join(_project_root_from_file, ".env"), os.path.join(_cwd, ".env")]
    return [p for p in locs if p]


def require_gemini_api_key():
    """Return the Gemini API key, or raise ValueError with instructions if missing."""
    key = (GEMINI_API_KEY or "").strip()
    if not key:
        locs = _env_locations_checked()
        where = ("; ".join(locs) if locs else "current directory")
        raise ValueError(
            f"Gemini API key is missing. Add GEMINI_API_KEY=your_key to a .env file. "
            f"App looked for .env in: {where}. Get a key: https://aistudio.google.com/apikey"
        )
    return key