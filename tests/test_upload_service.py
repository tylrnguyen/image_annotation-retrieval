from app.services.upload_service import submit_image

def test_upload_missing_file_returns_none():
    result = submit_image("images/does_not_exist.jpg")
    assert result is None