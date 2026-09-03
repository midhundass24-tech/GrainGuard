import os
from pathlib import Path
from typing import Dict, Any, List
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent
# Load .env from project root or backend dir
load_dotenv(BASE_DIR.parent / ".env")
load_dotenv(BASE_DIR / ".env")

import re

def get_all_gemini_api_keys() -> List[str]:
    keys = []
    single = os.getenv("GEMINI_API_KEY", "").strip()
    if single:
        for k in single.split(","):
            k_clean = k.strip()
            if k_clean and k_clean not in keys:
                keys.append(k_clean)

    env_matches = []
    for k in os.environ.keys():
        if k.startswith("GEMINI_API_KEY_") or k.startswith("GEMINI_KEY_"):
            num_match = re.search(r'\d+', k)
            idx = int(num_match.group()) if num_match else 999
            env_matches.append((idx, k))

    env_matches.sort(key=lambda x: (x[0], x[1]))
    for _, k in env_matches:
        val = os.getenv(k, "").strip()
        if val and val not in keys:
            keys.append(val)

    return keys

class Settings(BaseSettings):
    PROJECT_NAME: str = "GrainGuard"
    VERSION: str = "1.0.0"
    API_PREFIX: str = "/api"
    
    # AI Engine Mode: "auto", "gemini", "model", or "demo"
    AI_MODE: str = os.getenv("AI_MODE", "auto").lower()
    
    # Dynamically detected Gemini API Keys
    GEMINI_API_KEYS: List[str] = get_all_gemini_api_keys()
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR}/grainguard.db")
    
    # Host & Ports
    BACKEND_HOST: str = os.getenv("BACKEND_HOST", "0.0.0.0")
    BACKEND_PORT: int = int(os.getenv("BACKEND_PORT", 8000))
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:5173")
    
    # Storage Paths
    STATIC_DIR: Path = BASE_DIR / "static"
    UPLOAD_RAW_DIR: Path = STATIC_DIR / "uploads" / "raw"
    UPLOAD_ANNOTATED_DIR: Path = STATIC_DIR / "uploads" / "annotated"
    CERTIFICATE_DIR: Path = STATIC_DIR / "certificates"
    MODELS_DIR: Path = BASE_DIR / "models"
    
    # Image Quality Thresholds (calibrated for smartphone cameras and standard trays)
    MIN_BLUR_LAPLACIAN: float = 30.0
    MIN_LUMINANCE: float = 20.0
    MAX_LUMINANCE: float = 245.0
    MIN_DETECTED_OBJECTS: int = 4
    
    # Configurable Demonstration Quality Penalties & Reject Limits
    QUALITY_THRESHOLDS: Dict[str, Any] = {
        "rice": {
            "penalties": {
                "broken_penalty_per_pct": 1.5,
                "discoloration_penalty_per_pct": 2.0,
                "insect_penalty_per_pct": 5.0,
                "foreign_matter_penalty_per_pct": 10.0,
            },
            "limits": {
                "broken_warning": 5.0,
                "broken_reject": 15.0,
                "foreign_matter_warning": 1.0,
                "foreign_matter_reject": 3.0,
                "insect_damage_warning": 0.5,
                "insect_damage_reject": 2.0,
            }
        },
        "wheat": {
            "penalties": {
                "broken_penalty_per_pct": 1.2,
                "discoloration_penalty_per_pct": 2.5,
                "insect_penalty_per_pct": 5.0,
                "foreign_matter_penalty_per_pct": 8.0,
            },
            "limits": {
                "broken_warning": 6.0,
                "broken_reject": 18.0,
                "foreign_matter_warning": 1.5,
                "foreign_matter_reject": 4.0,
                "insect_damage_warning": 1.0,
                "insect_damage_reject": 2.5,
            }
        },
        "pulses": {
            "penalties": {
                "broken_penalty_per_pct": 2.0,
                "discoloration_penalty_per_pct": 3.0,
                "insect_penalty_per_pct": 6.0,
                "foreign_matter_penalty_per_pct": 10.0,
            },
            "limits": {
                "broken_warning": 4.0,
                "broken_reject": 10.0,
                "foreign_matter_warning": 1.0,
                "foreign_matter_reject": 2.5,
                "insect_damage_warning": 0.5,
                "insect_damage_reject": 1.5,
            }
        }
    }

    def init_directories(self) -> None:
        self.UPLOAD_RAW_DIR.mkdir(parents=True, exist_ok=True)
        self.UPLOAD_ANNOTATED_DIR.mkdir(parents=True, exist_ok=True)
        self.CERTIFICATE_DIR.mkdir(parents=True, exist_ok=True)
        self.MODELS_DIR.mkdir(parents=True, exist_ok=True)

    class Config:
        case_sensitive = True

settings = Settings()
settings.init_directories()
