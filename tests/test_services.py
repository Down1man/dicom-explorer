import io
import pytest
from unittest.mock import patch, MagicMock

from app import services

def make_fake_dataset(**attrs):
    fake = MagicMock()
    for k, v in attrs.items():
        setattr(fake, k, v)
    if 'pixel_array' in attrs:
        fake.pixel_array = attrs['pixel_array']
    return fake

@patch('app.services.pydicom')
def test_extract_metadata(mock_pydicom):
    fake_ds = make_fake_dataset(PatientID='ABC123', StudyDate='20250101', Modality='US')
    mock_pydicom.dcmread.return_value = fake_ds

    metadata = services.extract_metadata(b'dummybytes')

    assert metadata['PatientID'] == 'ABC123'
    assert metadata['StudyDate'] == '20250101'
    assert metadata['Modality'] == 'US'

@patch('app.services.pydicom')
def test_dicom_to_png_no_pixeldata(mock_pydicom):
    fake_ds = make_fake_dataset()
    delattr(fake_ds, 'PixelData')
    mock_pydicom.dcmread.return_value = fake_ds
    with pytest.raises(ValueError):
        services.dicom_to_png(b'dummy')

@patch('app.services.pydicom')
def test_dicom_to_png_basic(mock_pydicom):
    import numpy as np
    arr = (np.linspace(0, 1, 64*64).reshape(64,64) * 255).astype('uint8')
    fake_ds = make_fake_dataset()
    fake_ds.PixelData = b'pixeldata'
    fake_ds.pixel_array = arr
    mock_pydicom.dcmread.return_value = fake_ds

    png = services.dicom_to_png(b'dummy')
    # PNG header check: first 8 bytes of a PNG file
    assert png[:8] == b'\x89PNG\r\n\x1a\n'
