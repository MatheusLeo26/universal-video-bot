import pytest
from pathlib import Path
import os
from src.api_client import VideoDownloaderAPI

@pytest.mark.asyncio
async def test_start_download_success(httpx_mock):
    httpx_mock.add_response(
        url="https://api.huntapi.com/v1/video/download",
        method="POST",
        json={"job_id": "job-12345"},
        status_code=200
    )
    
    api = VideoDownloaderAPI()
    job_id = await api.start_download("https://example.com/video")
    
    assert job_id == "job-12345"

@pytest.mark.asyncio
async def test_start_download_failure(httpx_mock):
    httpx_mock.add_response(
        url="https://api.huntapi.com/v1/video/download",
        method="POST",
        status_code=400,
        text="Invalid URL"
    )
    
    api = VideoDownloaderAPI()
    job_id = await api.start_download("https://invalid-url.com")
    
    assert job_id is None

@pytest.mark.asyncio
async def test_check_status_success(httpx_mock):
    httpx_mock.add_response(
        url="https://api.huntapi.com/v1/video/download/job-12345",
        method="GET",
        json={"status": "completed", "file_url": "https://example.com/file.mp4"},
        status_code=200
    )
    
    api = VideoDownloaderAPI()
    status_data = await api.check_status("job-12345")
    
    assert status_data is not None
    assert status_data["status"] == "completed"
    assert status_data["file_url"] == "https://example.com/file.mp4"

@pytest.mark.asyncio
async def test_download_file_success(httpx_mock, temp_downloads_dir):
    file_content = b"fake video content"
    httpx_mock.add_response(
        url="https://example.com/file.mp4",
        method="GET",
        content=file_content,
        status_code=200
    )
    
    api = VideoDownloaderAPI()
    api.downloads_dir = Path(temp_downloads_dir)
    
    filepath = await api.download_file("https://example.com/file.mp4")
    
    assert filepath is not None
    assert os.path.exists(filepath)
    with open(filepath, "rb") as f:
        assert f.read() == file_content
