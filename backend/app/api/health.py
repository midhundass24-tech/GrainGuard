from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.config import settings
from app.database.session import get_db

router = APIRouter()

@router.get("/health")
def health_check(db: Session = Depends(get_db)):
    db_status = "connected"
    try:
        db.execute(text("SELECT 1"))
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"

    candidate_models = list(settings.MODELS_DIR.glob("grain_model.*"))
    model_loaded = len(candidate_models) > 0 and settings.AI_MODE == "model"

    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "ai_mode": settings.AI_MODE,
        "model_loaded": model_loaded,
        "database": db_status,
        "supported_grains": list(settings.QUALITY_THRESHOLDS.keys()),
    }
