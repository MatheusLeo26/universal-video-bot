import asyncio
import uuid
from typing import Dict
from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.responses import RedirectResponse
from src.schemas import ProcessRequest, ProcessResponse, StatusResponse
from src.extractor import extract_video_metadata
from src.api_client import VideoDownloaderAPI
import logging

logger = logging.getLogger(__name__)

# Global in-memory dictionary to store job statuses
# Key: job_id (str), Value: status (str)
jobs: Dict[str, str] = {}

app = FastAPI(
    title="Async Resource Processor API",
    description="API for starting asynchronous resource processing jobs.",
    version="1.0.0"
)

@app.get("/", include_in_schema=False)
async def root():
    """Redirects to the API documentation."""
    return RedirectResponse(url="/docs")

async def process_video_task(job_id: str, resource_url: str):
    """
    Real asynchronous background processing using Playwright and HTTPX.
    """
    try:
        logger.info(f"[{job_id}] Starting extraction via Playwright for {resource_url}")
        
        # 1. Playwright Extraction
        metadata = await extract_video_metadata(resource_url)
        if not metadata:
            logger.error(f"[{job_id}] Failed to extract metadata.")
            jobs[job_id] = "failed"
            return
            
        download_url = metadata.get("video_url") or metadata.get("video_src_attribute") or resource_url
        logger.info(f"[{job_id}] Extracted URL: {download_url}")
        
        # 2. Call the HuntAPI download service
        api_client = VideoDownloaderAPI()
        remote_job_id = await api_client.start_download(download_url)
        
        if not remote_job_id:
            logger.error(f"[{job_id}] Failed to start remote download.")
            jobs[job_id] = "failed"
            return
            
        # 3. Poll remote API status
        logger.info(f"[{job_id}] Polling remote status for {remote_job_id}")
        file_url = None
        while True:
            status_data = await api_client.check_status(remote_job_id)
            if not status_data:
                jobs[job_id] = "failed"
                return
                
            status = status_data.get("status")
            if status == "completed":
                file_url = status_data.get("file_url")
                break
            elif status == "failed":
                jobs[job_id] = "failed"
                return
                
            await asyncio.sleep(5)
            
        # 4. Download final .mp4 locally
        if file_url:
            local_path = await api_client.download_file(file_url)
            if local_path:
                logger.info(f"[{job_id}] Video successfully saved to {local_path}")
                jobs[job_id] = "completed"
            else:
                jobs[job_id] = "failed"
        else:
            jobs[job_id] = "failed"

    except Exception as e:
        logger.exception(f"[{job_id}] Unexpected error: {e}")
        jobs[job_id] = "failed"

@app.post("/api/v1/process", response_model=ProcessResponse, status_code=202)
async def start_processing(request: ProcessRequest, background_tasks: BackgroundTasks):
    """
    Receives a resource_url, generates a unique job_id, starts processing
    in the background, and returns the job_id.
    """
    job_id = str(uuid.uuid4())
    
    # Initialize the job status as 'processing'
    jobs[job_id] = "processing"
    
    # Start the real background task
    background_tasks.add_task(process_video_task, job_id, request.resource_url)
    
    return ProcessResponse(job_id=job_id)

@app.get("/api/v1/status/{job_id}", response_model=StatusResponse)
async def check_status(job_id: str):
    """
    Returns the current status of the processing job.
    """
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
        
    return StatusResponse(status=jobs[job_id])

@app.get("/api/v1/fly")
async def easter_egg():
    """
    Easter egg endpoint that imports antigravity.
    """
    import antigravity
    return {"message": "You are flying now!"}
