import httpx
import os
import aiofiles
import logging
from typing import Optional, Dict, Any
from pathlib import Path
from src.config import settings

logger = logging.getLogger(__name__)

class VideoDownloaderAPI:
    """
    Client for interacting with the HuntAPI video download service.
    """
    def __init__(self):
        self.base_url = settings.huntapi_base_url
        self.api_key = settings.huntapi_api_key
        self.downloads_dir = Path(settings.downloads_dir)
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        if not self.downloads_dir.exists():
            self.downloads_dir.mkdir(parents=True, exist_ok=True)

    async def start_download(self, url: str) -> Optional[str]:
        """
        Starts the download process for a video URL.
        Returns the job_id if successful.
        """
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.base_url}",
                    headers=self.headers,
                    json={"url": url},
                    timeout=10.0
                )
                response.raise_for_status()
                data = response.json()
                return data.get("job_id")
            except httpx.HTTPStatusError as e:
                logger.error(f"HTTP error starting download: {e.response.status_code} - {e.response.text}")
                return None
            except httpx.RequestError as e:
                logger.error(f"Request error starting download: {e}")
                return None

    async def check_status(self, job_id: str) -> Optional[Dict[str, Any]]:
        """
        Checks the status of a download job.
        """
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.base_url}/{job_id}",
                    headers=self.headers,
                    timeout=10.0
                )
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError as e:
                logger.error(f"Error checking status for job {job_id}: {e}")
                return None

    async def download_file(self, file_url: str) -> Optional[str]:
        """
        Downloads the resulting video file to the local downloads directory.
        Returns the path to the downloaded file.
        """
        filename = file_url.split("/")[-1]
        if not filename.endswith(".mp4"):
            filename = f"{filename}.mp4"
            
        filepath = self.downloads_dir / filename

        async with httpx.AsyncClient() as client:
            try:
                async with client.stream("GET", file_url, headers=self.headers) as response:
                    response.raise_for_status()
                    async with aiofiles.open(filepath, "wb") as f:
                        async for chunk in response.aiter_bytes(chunk_size=8192):
                            await f.write(chunk)
                logger.info(f"File downloaded successfully to {filepath}")
                return str(filepath)
            except httpx.HTTPError as e:
                logger.error(f"Error downloading file {file_url}: {e}")
                return None
