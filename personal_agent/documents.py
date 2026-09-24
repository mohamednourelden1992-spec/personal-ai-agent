from pathlib import Path
from pypdf import PdfReader


def extract_text(path: str) -> str:
    file = Path(path)
    if file.suffix.lower() == ".pdf":
        return "\n".join(page.extract_text() or "" for page in PdfReader(str(file)).pages)
    return file.read_text(encoding="utf-8")
