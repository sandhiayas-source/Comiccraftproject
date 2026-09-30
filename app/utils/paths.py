from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GENERATED_DIR = ROOT / "generated"
IMAGE_DIR = GENERATED_DIR / "images"
PDF_DIR = GENERATED_DIR / "pdf"

def ensure_directories():
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    PDF_DIR.mkdir(parents=True, exist_ok=True)
