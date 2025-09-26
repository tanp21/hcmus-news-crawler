from dataclasses import dataclass
from typing import List


@dataclass
class CrawlerConfig:
    ctda_url: str = "https://www.ctda.hcmus.edu.vn/vi/"
    fit_url: str = "https://www.fit.hcmus.edu.vn/vn/"
    hcmus_url: str = "https://hcmus.edu.vn/category/dao-tao/dai-hoc/thong-tin-danh-cho-sinh-vien/feed/"
    old_hcmus_url: str = "https://old.hcmus.edu.vn/sinh-vien"
    
    ctda_section_titles: List[str] = None
    
    timeout: int = 15
    max_retries: int = 3
    retry_delay: float = 1.0
    
    output_file: str = "NEWS.md"
    timezone: str = "Asia/Ho_Chi_Minh"
    
    user_agent: str = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0"
    )
    
    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    log_file: str = "crawler.log"
    
    headers: dict = None
    
    def __post_init__(self):
        if self.ctda_section_titles is None:
            self.ctda_section_titles = [
                'Academic Planning',
                'Academic Affairs', 
                'Student Support',
                'Accounting & Finance'
            ]
        
        if self.headers is None:
            self.headers = {
                "User-Agent": self.user_agent
            }


config = CrawlerConfig()