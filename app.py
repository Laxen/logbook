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


def _today_file_path() -> Path:
    NOTES_DIR.mkdir(parents=True, exist_ok=True)
    return NOTES_DIR / f"{datetime.now().strftime('%Y-%m-%d')}.txt"


def _load_today_note() -> str:
    note_file = _today_file_path()
    if not note_file.exists():
        return ""
    return note_file.read_text(encoding="utf-8", errors="replace")


def _save_today_note(note_text: str) -> bool:
    if len(note_text.encode("utf-8")) > MAX_NOTE_BYTES:
        return False

    note_file = _today_file_path()
    note_file.write_text(note_text, encoding="utf-8")
    return True


@app.route("/", methods=["GET", "POST"])
def index() -> str:
    message = ""
    if request.method == "POST":
        if _save_today_note(request.form.get("note", "")):
            message = "Saved"
        else:
            message = "Note is too large (max 5 MB)."

    return render_template(
        "index.html",
        note=_load_today_note(),
        date=datetime.now().strftime("%Y-%m-%d"),
        message=message,
    )


@app.errorhandler(413)
def request_too_large(_error: object) -> tuple[str, int]:
    return (
        render_template(
            "index.html",
            note=_load_today_note(),
            date=datetime.now().strftime("%Y-%m-%d"),
            message="Note is too large (max 5 MB).",
        ),
        413,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8099)
