"""Main entry point for the HCMUS News Crawler package."""

from .crawler import NewsCrawler


def main():
    """Main function to run the news crawler."""
    crawler = NewsCrawler()
    report = crawler.generate_report()
    success = crawler.save_report(report)
    
    if not success:
        exit(1)


if __name__ == '__main__':
    main()