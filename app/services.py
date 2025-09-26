from io import BytesIO
try:
    import pydicom
    import numpy as np
    from PIL import Image
except Exception as e:
    pydicom = None
    np = None
    Image = None

def extract_metadata(dicom_bytes: bytes) -> dict:
    """Return a dict with a safe subset of DICOM tags."""
    if pydicom is None:
        raise RuntimeError("pydicom is not installed in the environment")

    dataset = pydicom.dcmread(BytesIO(dicom_bytes), force=True)
    def safe(tag):
        return getattr(dataset, tag, None)
    out = {
        'PatientID': safe('PatientID'),
        'PatientName': str(safe('PatientName')) if safe('PatientName') else None,
        'StudyDate': safe('StudyDate'),
        'Modality': safe('Modality'),
        'Rows': safe('Rows'),
        'Columns': safe('Columns'),
    }
    return {k: v for k, v in out.items() if v is not None}

def dicom_to_png(dicom_bytes: bytes, scale_to=256) -> bytes:
    """Convert the first available image frame from DICOM to PNG bytes.

    Note: For multi-frame DICOMs or complex photometric interpretations more handling is needed.
    """
    if pydicom is None or Image is None or np is None:
        raise RuntimeError("Required imaging libraries (pydicom, Pillow, numpy) are not installed")

    ds = pydicom.dcmread(BytesIO(dicom_bytes), force=True)
    if not hasattr(ds, 'PixelData'):
        raise ValueError('DICOM has no PixelData')

    arr = ds.pixel_array 
    if arr.ndim == 3:
        arr = arr[0]
    arr = arr.astype('float32')
    arr -= arr.min()
    if arr.max() != 0:
        arr /= arr.max()
    arr = (arr * 255.0).astype('uint8')

    img = Image.fromarray(arr)
    img = img.convert('L')
    img.thumbnail((scale_to, scale_to))
    buf = BytesIO()
    img.save(buf, format='PNG')
    return buf.getvalue()
