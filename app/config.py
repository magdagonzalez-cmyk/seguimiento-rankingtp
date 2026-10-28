import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "tp-ranking-clave-local-2026")
    DATABASE = os.getenv(
        "DATABASE_PATH",
        str(BASE_DIR / "tp_ranking.db")
    )
