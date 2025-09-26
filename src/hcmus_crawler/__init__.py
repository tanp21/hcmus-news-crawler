"""HCMUS News Crawler package."""

__version__ = "2.0.0"
__author__ = "tanp21"
__description__ = "Automated news aggregation system for HCMUS websites"

from .crawler import NewsCrawler
from .models import NewsItem, NewsSection, CrawlerReport
from .config import config

__all__ = ["NewsCrawler", "NewsItem", "NewsSection", "CrawlerReport", "config"]