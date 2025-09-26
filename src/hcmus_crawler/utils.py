import logging
import time
import requests
from typing import Optional
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .config import config


def setup_logging() -> logging.Logger:
    logging.basicConfig(
        level=getattr(logging, config.log_level),
        format=config.log_format,
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('crawler.log', encoding='utf-8')
        ]
    )
    return logging.getLogger(__name__)


def create_session() -> requests.Session:
    session = requests.Session()
    
    retry_strategy = Retry(
        total=config.max_retries,
        backoff_factor=config.retry_delay,
        status_forcelist=[429, 500, 502, 503, 504],
    )
    
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    
    session.headers.update({
        "User-Agent": config.user_agent
    })
    
    return session


def safe_request(session: requests.Session, url: str, logger: logging.Logger) -> Optional[requests.Response]:
    try:
        response = session.get(url, timeout=config.timeout)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException:
        return None


def clean_text(text: str) -> str:
    if not text:
        return ""
    
    cleaned = ' '.join(text.split())
    return cleaned.strip()


def normalize_url(url: str, base_url: str = "") -> str:
    if not url:
        return ""
    
    url = url.strip()
    
    if url.startswith('/') and base_url:
        url = base_url.rstrip('/') + url
    
    return url