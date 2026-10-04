import pytest
from src.extractor import extract_video_metadata
from unittest.mock import patch, AsyncMock, MagicMock
from playwright.async_api import TimeoutError as PlaywrightTimeoutError

@pytest.mark.asyncio
@patch('src.extractor.async_playwright')
async def test_extract_video_metadata_success(mock_async_playwright):
    # Mock playwright objects
    mock_playwright = AsyncMock()
    mock_browser = AsyncMock()
    mock_context = AsyncMock()
    mock_page = AsyncMock()
    mock_page.on = MagicMock()
    
    mock_async_playwright.return_value.__aenter__.return_value = mock_playwright
    mock_playwright.chromium.launch.return_value = mock_browser
    mock_browser.new_context.return_value = mock_context
    mock_context.new_page.return_value = mock_page
    
    # Mock page behavior
    mock_page.title.return_value = "Test Video"
    
    mock_video_element = AsyncMock()
    mock_video_element.get_attribute.return_value = "https://example.com/video.mp4"
    mock_page.query_selector.return_value = mock_video_element
    
    metadata = await extract_video_metadata("https://example.com")
    
    assert metadata is not None
    assert metadata["title"] == "Test Video"
    assert metadata["video_src_attribute"] == "https://example.com/video.mp4"

@pytest.mark.asyncio
@patch('src.extractor.async_playwright')
async def test_extract_video_metadata_timeout(mock_async_playwright):
    mock_playwright = AsyncMock()
    mock_browser = AsyncMock()
    mock_context = AsyncMock()
    mock_page = AsyncMock()
    mock_page.on = MagicMock()
    
    mock_async_playwright.return_value.__aenter__.return_value = mock_playwright
    mock_playwright.chromium.launch.return_value = mock_browser
    mock_browser.new_context.return_value = mock_context
    mock_context.new_page.return_value = mock_page
    
    # Simulate timeout during goto
    mock_page.goto.side_effect = PlaywrightTimeoutError("Navigation Timeout Exceeded: 30000ms exceeded")
    
    metadata = await extract_video_metadata("https://example.com/timeout")
    
    assert metadata is None
