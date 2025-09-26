from bs4 import BeautifulSoup as bs
import requests
import re
from datetime import datetime
from zoneinfo import ZoneInfo
from typing import List
import logging

from .config import config
from .models import NewsItem, NewsSection, CrawlerReport
from .utils import setup_logging, create_session, safe_request, clean_text, normalize_url


class NewsCrawler:
    
    def __init__(self):
        self.logger = setup_logging()
        self.session = create_session()
        self.report_errors = []
    
    def crawl_ctda(self) -> NewsSection:
        try:
            page = safe_request(self.session, config.ctda_url, self.logger)
            
            if not page:
                return NewsSection("APCS", [], "Failed to load APCS news")
            
            soup = bs(page.content, features='lxml')
            sections = soup.find_all(class_='display-posts-listing')[:4]
            
            all_items = []
            for i, section in enumerate(sections):
                if i >= len(config.ctda_section_titles):
                    break
                    
                try:
                    news_elements = section.find_all(class_='listing-item')
                    for element in news_elements:
                        try:
                            link_element = element.contents[0]
                            title = clean_text(link_element.text)
                            url = normalize_url(link_element.attrs.get('href', ''))
                            date = clean_text(element.contents[-1].text) if len(element.contents) > 1 else ""
                            
                            if title and url:
                                all_items.append(NewsItem(
                                    title=title,
                                    url=url,
                                    date=date,
                                    category=config.ctda_section_titles[i]
                                ))
                        except (IndexError, KeyError, AttributeError):
                            continue
                
                except Exception:
                    continue
            
            return NewsSection("APCS", all_items)
            
        except Exception as e:
            return NewsSection("APCS", [], f"Error loading APCS news: {str(e)}")

    def crawl_fit(self) -> NewsSection:
        try:
            page = safe_request(self.session, config.fit_url, self.logger)
            
            if not page:
                return NewsSection("FIT", [], "Failed to load FIT news")
            
            soup = bs(page.content, features='lxml')
            news_raw = soup.select('#dnn_ctr989_ModuleContent > table')
            
            items = []
            for news in news_raw:
                try:
                    day_element = news.select_one('tr:first-child > .day_month')
                    month_element = news.select_one('tr:last-child > .day_month') 
                    year_element = news.select_one('.post_year')
                    title_element = news.select_one('a')
                    
                    if not all([day_element, month_element, year_element, title_element]):
                        continue
                    
                    day = clean_text(day_element.text)
                    month = clean_text(month_element.text)
                    year = clean_text(year_element.text)
                    title = clean_text(title_element.text)
                    href = title_element.attrs.get('href', '')
                    
                    if title and href:
                        full_url = normalize_url(href, "https://www.fit.hcmus.edu.vn/vn/")
                        date = f"{day}-{month}-{year}"
                        
                        items.append(NewsItem(
                            title=title,
                            url=full_url,
                            date=date
                        ))
                        
                except (AttributeError, KeyError):
                    continue
            
            return NewsSection("FIT", items)
            
        except Exception as e:
            return NewsSection("FIT", [], f"Error loading FIT news: {str(e)}")

    def crawl_hcmus(self) -> NewsSection:
        try:
            page = safe_request(self.session, config.hcmus_url, self.logger)
            
            if not page:
                return NewsSection("Student Information", [], "Failed to load HCMUS news")
            
            soup = bs(page.content, features="xml")
            items_elements = soup.find_all('item')
            
            items = []
            for item_element in items_elements:
                try:
                    title_element = item_element.find('title')
                    link_element = item_element.find('link')
                    pub_date_element = item_element.find('pubDate')
                    
                    if not all([title_element, link_element, pub_date_element]):
                        continue
                    
                    title = clean_text(title_element.text)
                    link = clean_text(link_element.text)
                    pub_date = clean_text(pub_date_element.text)
                    
                    if title and link and pub_date:
                        try:
                            date_obj = datetime.strptime(pub_date, "%a, %d %b %Y %H:%M:%S %z")
                            formatted_date = date_obj.strftime('%d/%m/%Y')
                        except ValueError:
                            formatted_date = pub_date
                        
                        items.append(NewsItem(
                            title=title,
                            url=link,
                            date=formatted_date
                        ))
                        
                except (AttributeError, ValueError):
                    continue
            
            return NewsSection("Student Information", items)
            
        except Exception as e:
            return NewsSection("Student Information", [], f"Error loading HCMUS news: {str(e)}")

    def crawl_old_hcmus(self) -> NewsSection:
        try:
            page = safe_request(self.session, config.old_hcmus_url, self.logger)
            
            if not page:
                return NewsSection("Exam Announcements", [], "Failed to load exam announcements")
            
            soup = bs(page.content, features="lxml")
            ctkt_elements = soup.find_all(class_='feed-link')
            
            items = []
            rule_position = [5, 10, 13]
            
            for i, news_element in enumerate(ctkt_elements):
                try:
                    title_text = re.sub(r'(\t|\n)', '', news_element.text)
                    title = clean_text(title_text)
                    
                    link_match = re.search(r'http[^"]*', str(news_element))
                    link = link_match.group(0) if link_match else ""
                    
                    if title and link:
                        category = None
                        if i in rule_position:
                            category = "Important"
                        
                        items.append(NewsItem(
                            title=title,
                            url=link,
                            date="",
                            category=category
                        ))
                        
                except (AttributeError, TypeError):
                    continue
            
            return NewsSection("Exam Announcements", items)
            
        except Exception as e:
            return NewsSection("Exam Announcements", [], f"Error loading exam announcements: {str(e)}")

    def generate_report(self) -> CrawlerReport:
        sections = [
            self.crawl_ctda(),
            self.crawl_fit(),
            self.crawl_hcmus(),
            self.crawl_old_hcmus()
        ]
        
        timestamp = datetime.now(tz=ZoneInfo(config.timezone))
        
        section_errors = []
        for section in sections:
            if section.has_errors():
                section_errors.append(f"{section.title}: {section.error_message}")
        
        report = CrawlerReport(
            sections=sections,
            timestamp=timestamp,
            errors=section_errors + self.report_errors
        )
        
        return report

    def save_report(self, report: CrawlerReport) -> bool:
        try:
            with open(config.output_file, 'w', encoding='utf-8') as f:
                f.write(report.to_markdown())
            return True
        except IOError:
            return False