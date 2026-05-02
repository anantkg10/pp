# Brain Tumor Demo Tool

This is the standalone demo-only project. It highlights suspicious bright regions in an uploaded MRI-like image and returns a rule-based tumor-like estimate.

## What this project contains

- Django web app for upload and result display
- demo heuristic backend only
- no deep-learning training code
- no model checkpoint files

## How the demo works

The demo backend:

- converts the image to grayscale
- increases contrast
- gives more weight to the center of the image
- finds the largest suspicious bright region
- draws a highlight
- guesses a tumor-like pattern from size and position

## Project layout

- `brain_mri_project/` Django settings and routing
- `detector/` upload UI and demo inference code
- `docs/PROJECT_MAP.md` file map for this demo-only project

## Open Cleanly In VS Code

Open:

- `C:\Users\HP\Documents\New project\brain_tumor_demo_tool.code-workspace`

## Run locally

```powershell
cd C:\Users\HP\Documents\New project\brain_tumor_demo_tool
python manage.py migrate
python manage.py runserver
```

Open `http://127.0.0.1:8000/`.

## Inference backend

This project uses the demo heuristic backend only.

## API

POST `api/predict/` with multipart form-data:

- `image`: MRI image file

Response:

- `prediction_id`
- `tumor_detected`
- `predicted_type`
- `confidence`
- `backend`
- `overlay_url`
- `bbox`
- `location_summary`
- `size_summary`
- `disclaimer`

## Tests

```powershell
cd C:\Users\HP\Documents\New project\brain_tumor_demo_tool
python manage.py test
```
