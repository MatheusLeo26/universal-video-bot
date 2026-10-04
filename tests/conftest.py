import pytest
import tempfile
import shutil
from pathlib import Path
import os

@pytest.fixture
def temp_downloads_dir():
    """Fixture to create a temporary directory for downloads."""
    temp_dir = tempfile.mkdtemp()
    
    yield temp_dir
    
    # Cleanup after test
    shutil.rmtree(temp_dir)
