import os
from datetime import datetime
from pathlib import Path

from flask import Flask, render_template, request

app = Flask(__name__)
NOTES_DIR = Path(os.environ.get("NOTES_DIR", "/share/logbook"))


def _today_file_path() -> Path:
    NOTES_DIR.mkdir(parents=True, exist_ok=True)
    return NOTES_DIR / f"{datetime.now().strftime('%Y-%m-%d')}.txt"


def _load_today_note() -> str:
    note_file = _today_file_path()
    if not note_file.exists():
        return ""
    return note_file.read_text(encoding="utf-8")


def _save_today_note(note_text: str) -> None:
    note_file = _today_file_path()
    note_file.write_text(note_text, encoding="utf-8")


@app.route("/", methods=["GET", "POST"])
def index() -> str:
    message = ""
    if request.method == "POST":
        _save_today_note(request.form.get("note", ""))
        message = "Saved"

    return render_template(
        "index.html",
        note=_load_today_note(),
        date=datetime.now().strftime("%Y-%m-%d"),
        message=message,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8099)
