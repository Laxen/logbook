# logbook

A minimal Home Assistant app/add-on for daily notes.

## What it does

- Exposes an ingress web UI ("Open Web UI" button in Home Assistant)
- Shows and edits today’s note only
- Saves to `/share/logbook/YYYY-MM-DD.txt` so files can be copied later (for example via SCP)

## Files

- `/tmp/workspace/Laxen/logbook/config.yaml` — Home Assistant app/add-on metadata
- `/tmp/workspace/Laxen/logbook/app.py` — lightweight Flask server
- `/tmp/workspace/Laxen/logbook/templates/index.html` — minimalist mobile-friendly UI
