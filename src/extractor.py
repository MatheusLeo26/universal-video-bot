import asyncio
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError, Page, Response
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

async def extract_video_metadata(url: str) -> Optional[Dict[str, Any]]:
    """
    Navigates to the provided URL, intercepts network requests, and extracts video metadata.
    """
    video_metadata = {}

    async def handle_response(response: Response):
        # Intercept network requests to find video streams or metadata APIs
        content_type = response.headers.get("content-type", "")
        if "video" in content_type or ".mp4" in response.url or ".m3u8" in response.url:
            logger.info(f"Found video stream: {response.url}")
            video_metadata["video_url"] = response.url
    
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
            page = await context.new_page()
            
            page.on("response", handle_response)
            
            # Anti-bot detection mitigation basics
            await page.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                })
            """)

            logger.info(f"Navigating to {url}")
            await page.goto(url, wait_until="networkidle", timeout=30000)
            
            # Wait for potential video elements to load
            try:
                await page.wait_for_selector("video", timeout=5000)
                video_element = await page.query_selector("video")
                if video_element:
                    src = await video_element.get_attribute("src")
                    if src:
                        video_metadata["video_src_attribute"] = src
            except PlaywrightTimeoutError:
                logger.warning("No <video> element found on page.")

            # Try to extract page title as metadata
            video_metadata["title"] = await page.title()
            
            await browser.close()
            return video_metadata

    except PlaywrightTimeoutError:
        logger.error(f"Timeout while navigating to {url}")
        return None
    except Exception as e:
        logger.error(f"Error extracting metadata from {url}: {e}")
        return None
