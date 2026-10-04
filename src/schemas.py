from pydantic import BaseModel

class ProcessRequest(BaseModel):
    """Schema for the start processing job request."""
    resource_url: str

class ProcessResponse(BaseModel):
    """Schema for the start processing job response."""
    job_id: str

class StatusResponse(BaseModel):
    """Schema for the job status response."""
    status: str
