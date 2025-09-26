from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
from .services import extract_metadata, dicom_to_png
import io

app = FastAPI(title="DICOM Explorer")

@app.post("/upload/")
async def upload_dicom(file: UploadFile = File(...)):
    content = await file.read()
    try:
        metadata = extract_metadata(content)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse DICOM: {e}")
    return JSONResponse({"metadata": metadata, "thumbnail_endpoint": "/thumbnail/"})

@app.post("/thumbnail/")
async def thumbnail(file: UploadFile = File(...)):
    content = await file.read()
    try:
        png_bytes = dicom_to_png(content)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to generate thumbnail: {e}")
    return StreamingResponse(io.BytesIO(png_bytes), media_type="image/png")
