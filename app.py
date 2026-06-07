import os
from datetime import datetime
from pathlib import Path

from flask import Flask, render_template, request

app = Flask(__name__)
NOTES_DIR = Path(os.environ.get("NOTES_DIR", "/share/logbook"))
MAX_NOTE_BYTES = 5 * 1024 * 1024
app.config["MAX_FORM_MEMORY_SIZE"] = MAX_NOTE_BYTES + 1024
app.config["MAX_CONTENT_LENGTH"] = MAX_NOTE_BYTES + 1024
app.request_class.max_form_memory_size = MAX_NOTE_BYTES + 1024

def _note_file_path(date_str: str) -> Path:
    NOTES_DIR.mkdir(parents=True, exist_ok=True)
    return NOTES_DIR / f"{date_str}.txt"


def _load_note(date_str: str) -> str:
    note_file = _note_file_path(date_str)
    if not note_file.exists():
        return ""
    return note_file.read_text(encoding="utf-8", errors="replace")


def _save_note(date_str: str, note_text: str) -> bool:
    if len(note_text.encode("utf-8")) > MAX_NOTE_BYTES:
        return False

    note_file = _note_file_path(date_str)
    note_file.write_text(note_text, encoding="utf-8")
    return True


@app.route("/", methods=["GET", "POST"])
def index() -> str:
    current_date = datetime.now().strftime("%Y-%m-%d")
    message = ""
    note = _load_note(current_date)
    if request.method == "POST":
        note = request.form.get("note", "")
        if _save_note(current_date, note):
            message = "Saved"
        else:
            message = "Note is too large (max 5 MB)."

    return render_template(
        "index.html",
        note=note,
        date=current_date,
        message=message,
    )


@app.errorhandler(413)
def request_too_large(error: object) -> tuple[str, int]:
    _ = error
    current_date = datetime.now().strftime("%Y-%m-%d")
    return (
        render_template(
            "index.html",
            note=_load_note(current_date),
            date=current_date,
            message="Note is too large (max 5 MB).",
        ),
        413,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8099)
