from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime


@dataclass
class NewsItem:
    title: str
    url: str
    date: str
    category: Optional[str] = None
    
    def __post_init__(self):
        self.title = self.title.strip()
        self.url = self.url.strip()
        self.date = self.date.strip()
        if self.category:
            self.category = self.category.strip()
    
    def is_valid(self) -> bool:
        return bool(self.title and self.url and self.date)


@dataclass 
class NewsSection:
    title: str
    items: List[NewsItem]
    error_message: Optional[str] = None
    
    def __post_init__(self):
        self.title = self.title.strip()
        self.items = [item for item in self.items if item.is_valid()]
    
    def to_markdown(self) -> str:
        if self.error_message:
            return f"## {self.title}\n\n*{self.error_message}*\n\n"
        
        if not self.items:
            return f"## {self.title}\n\n*No news items found*\n\n"
        
        result = f"## {self.title}\n\n"
        current_category = None
        
        for item in self.items:
            if item.category and item.category != current_category:
                result += f"### {item.category}\n\n"
                current_category = item.category
            
            date_part = f"**{item.date}**: " if item.date else ""
            result += f"• {date_part}[{item.title}]({item.url})\n\n"
        
        return result
    
    def has_errors(self) -> bool:
        return self.error_message is not None
    
    def item_count(self) -> int:
        return len(self.items)


@dataclass
class CrawlerReport:
    sections: List[NewsSection]
    timestamp: datetime
    errors: List[str] = None
    
    def __post_init__(self):
        if self.errors is None:
            self.errors = []
    
    def to_markdown(self) -> str:
        report = "# 🎓 HCMUS News Update\n\n"
        report += f'*Last updated: **{self.timestamp.strftime("%Y-%m-%d at %H:%M %Z")}***\n\n'
        report += "---\n\n"
        
        if self.errors:
            report += "## ⚠️ Errors\n\n"
            for error in self.errors:
                report += f"• {error}\n"
            report += "\n"
        
        for section in self.sections:
            report += section.to_markdown()
        
        return report
    
    def get_total_items(self) -> int:
        return sum(section.item_count() for section in self.sections)
    
    def get_sections_with_errors(self) -> List[NewsSection]:
        return [section for section in self.sections if section.has_errors()]