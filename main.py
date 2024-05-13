from bs4 import BeautifulSoup as bs
import requests
import re
from datetime import datetime
from zoneinfo import ZoneInfo

def crawl_ctda():
    page = requests.get("https://www.ctda.hcmus.edu.vn/vi/")
    soup = bs(page.content, features='lxml')
    sections = soup.find_all(class_='display-posts-listing')[:4]
    section_titles = [
        'Kế hoạch học tập',
        'Giáo vụ',
        'Trợ lí sinh viên',
        'Kế toán - Tài chính'
    ]

    result = "## APCS\n"
    for i, section in enumerate(sections):
        result += f'### {section_titles[i]}\n'

        news = [[el.contents[0].text, el.contents[0].attrs['href'], el.contents[-1].text] for el in section.find_all(class_='listing-item')]
        for n in news:
            result += f' - {n[2]}: [{n[0]}]({n[1]})\n'

    return result

def crawl_fit():
    page = requests.get("https://www.fit.hcmus.edu.vn/vn/")
    soup = bs(page.content, features='lxml')
    news_raw = soup.select('#dnn_ctr989_ModuleContent > table')

    result = '## FIT\n'
    for news in news_raw:
        day = news.select_one('tr:first-child > .day_month').text.strip()
        month = news.select_one('tr:last-child > .day_month').text.strip()
        year = news.select_one('.post_year').text.strip()
        title = news.select_one('a').text.strip()
        href = news.select_one('a').attrs['href']
        result += f' - {day}-{month}-{year}: [{title}](https://www.fit.hcmus.edu.vn/vn/{href})\n'

    return result

def crawl_old_hcmus():
    page = requests.get("https://old.hcmus.edu.vn/sinh-vien")
    soup = bs(page.content, features="lxml")

    news_titles = [el.text for el in soup.find_all(class_='mod-articles-category-title')]
    raw_links = [el.attrs['href'] for el in soup.find_all(class_='mod-articles-category-title')]
    news_links = [''.join(url) for url in raw_links]

    raw_dates = [el.text for el in soup.find_all(class_='mod-articles-category-date')]
    news_dates = [''.join(re.findall('([\d-])', date)) for date in raw_dates]

    ctkt = [el for el in soup.find_all(class_='feed-link')]
    ctkt_titles = [''.join(re.sub(r'(\t|\n)', '', news.text)) for news in ctkt]
    ctkt_links = [''.join(re.findall('http.*" ', str(news))) for news in ctkt]

    thong_bao = ['Các thông báo về Đào Tạo',
                'Các thông báo về Công tác sinh viên',
                'Thông báo khác',
                'Các thông báo về Khảo thí']

    result = '## HCMUS\n'
    current_section = current_news_count = 0
    for i in range(len(news_dates)):
        if current_news_count == 0:
            result += f'### {thong_bao[current_section]}\n'
            current_section += 1
        current_news_count += 1
        if current_news_count == 15:
            current_news_count = 0
        result += f' - {news_dates[i]}: [{news_titles[i]}](https://old.hcmus.edu.vn{news_links[i]})\n'

    result += f'### {thong_bao[current_section]}\n'
    rule_position = [5, 10, 13]
    for i in range(len(ctkt_titles)):
        if i in rule_position:
            # [:-2] to remove unnecessary characters (" )
            result += f'\n***\n\n - [{ctkt_titles[i]}]({ctkt_links[i][:-2]})\n'
        else:
            result += f' - [{ctkt_titles[i]}]({ctkt_links[i][:-2]})\n'

    return result


if __name__ == '__main__':
    with open('NEWS.md', 'w', encoding='utf-8') as f:
        f.write('# All news\n')
        f.write(f'_Last update: **{datetime.now(tz=ZoneInfo("Asia/Ho_Chi_Minh"))}**_\n')
        f.write(crawl_ctda())
        f.write(crawl_fit())
        f.write(crawl_old_hcmus())
