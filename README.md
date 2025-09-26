# DICOM Explorer (FastAPI)

Lightweight project demonstrating:
- upload and metadata extraction from DICOM files (using `pydicom`)
- conversion of a DICOM image to PNG thumbnail (`Pillow`, `numpy`)
- simple FastAPI endpoints + tests + CI

## Tech stack
- Python 3.10+
- FastAPI, pydicom, Pillow
- pytest for tests
- Dockerfile + GitHub Actions CI example

## Quickstart (local)
1. python -m venv .venv
2. source .venv/bin/activate   # (Linux / macOS) or `.venv\Scripts\activate` on Windows
3. pip install -r requirements.txt
4. uvicorn app.main:app --reload --port 8000
5. Upload a DICOM:
   curl -X POST "http://localhost:8000/upload/" -F "file=@/path/to/example.dcm"

## Endpoints
- `POST /upload/` - returns extracted metadata (JSON) and a thumbnail endpoint info
- `POST /thumbnail/` - returns PNG thumbnail for an uploaded DICOM file

## Tests
Run `pytest -q`.

## Notes
- This project is a demo skeleton. In production you must consider PHI handling, encryption at rest/in transit,
  rate limits, authentication, proper error handling, and regulatory traceability (e.g., for medtech).
