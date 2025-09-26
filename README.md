# 🎓 HCMUS News Crawler

An automated news aggregation system that crawls and compiles news from various HCMUS (Ho Chi Minh City University of Science) websites. **The crawler runs automatically every hour via GitHub Actions** and updates the news in your repository.

## 🚀 **Auto-Deployment on GitHub**

This repository can automatically crawl news **every hour** and update the `NEWS.md` file using GitHub Actions. Perfect for staying up-to-date with HCMUS announcements!

## 🔧 Setup Instructions for Automated Crawling

### Step 1: Fork this Repository
1. **Fork** this repository to your GitHub account
2. **Clone** your fork locally:
```bash
git clone https://github.com/YOUR_USERNAME/hcmus-news-crawler.git
cd hcmus-news-crawler
```

### Step 2: Enable GitHub Actions
1. Go to your forked repository on GitHub
2. Click the **"Actions"** tab
3. Click **"I understand my workflows, enable them"**
4. The workflow will now run automatically every hour!

### Step 3: Manual Trigger (Optional)
You can also trigger the crawler manually:
1. Go to **Actions** → **Auto News Crawler**
2. Click **"Run workflow"** → **"Run workflow"**
3. The crawler will run immediately

### Step 4: Check Results
- The updated `NEWS.md` file will appear in your repository
- Each update includes a timestamp and commit message
- Check the **Actions** tab to see crawl logs and statistics

### 🎯 What Happens Automatically:
- ✅ **Every hour**: Crawler runs and checks for new news
- ✅ **Smart updates**: Only commits when new content is found  
- ✅ **Detailed logs**: Each run includes statistics and error handling
- ✅ **Timezone aware**: Uses Vietnam time (Asia/Ho_Chi_Minh)
- ✅ **Failure recovery**: Automatically retries on next scheduled run

## ⚙️ Customizing the Schedule

Want to change from hourly to a different schedule? Edit `.github/workflows/auto-crawl.yml`:

```yaml
on:
  schedule:
    # Every hour (default)
    - cron: '0 * * * *'
    
    # Every 30 minutes
    # - cron: '*/30 * * * *'
    
    # Every 6 hours  
    # - cron: '0 */6 * * *'
    
    # Daily at 8 AM Vietnam time
    # - cron: '0 1 * * *'  # (8 AM Vietnam = 1 AM UTC)
```

## Installation

```bash
git clone https://github.com/tanp21/hcmus-news-crawler.git
cd hcmus-news-crawler
pip install -e .
```

## Usage

```bash
# Run the crawler
python -m src.hcmus_crawler

# Or use entry point after installation
hcmus-crawler
```

## Project Structure

```
hcmus-news-crawler/
├── src/hcmus_crawler/     # Main package
│   ├── __init__.py        # Package exports
│   ├── __main__.py        # CLI entry point  
│   ├── crawler.py         # Crawler implementation
│   ├── models.py          # Data models
│   ├── config.py          # Configuration
│   └── utils.py           # Utilities
├── .github/workflows/     # CI/CD
│   └── auto-crawl.yml     # Automated crawling
├── pyproject.toml         # Package configuration
├── requirements.txt       # Dependencies
└── NEWS.md               # Generated output
```

## Features

- **Multi-source aggregation**: Crawls news from APCS, FIT, main HCMUS site, and exam announcements
- **Robust error handling**: Comprehensive logging and retry mechanisms
- **Automated deployment**: GitHub Actions workflow with hourly updates  
- **Clean output**: Well-formatted markdown with timestamps and categorization
- **Modular design**: Object-oriented structure with separate configuration and utilities

## News Sources

1. **APCS (CTDA)** - Advanced Program in Computer Science
   - Academic plans, academic affairs, student support, accounting
   - Source: https://www.ctda.hcmus.edu.vn/vi/

2. **FIT** - Faculty of Information Technology  
   - Department news and announcements
   - Source: https://www.fit.hcmus.edu.vn/vn/

3. **HCMUS Main Site** - Student Information
   - General student announcements and updates
   - Source: https://hcmus.edu.vn/

4. **Old HCMUS Site** - Exam Announcements
   - Exam schedules and testing information
   - Source: https://old.hcmus.edu.vn/sinh-vien

## Automated Deployment

### 🤖 GitHub Actions Workflow
The repository includes a comprehensive GitHub Actions workflow that:

1. **🕐 Hourly Schedule**: Runs every hour using cron: `'0 * * * *'`
2. **🐍 Python Setup**: Automatically installs Python 3.11 and dependencies  
3. **🔍 News Crawling**: Executes the crawler and generates updated NEWS.md
4. **📝 Smart Commits**: Only commits when new content is detected
5. **🚨 Error Handling**: Graceful failure recovery with detailed logging
6. **📊 Reporting**: Generates summary reports for each run

### 📈 Workflow Features:
- **Timezone awareness**: All timestamps in Vietnam time
- **Manual triggering**: Can be run on-demand via GitHub UI
- **Change detection**: Skips commits when no new news found
- **Dependency caching**: Faster runs with pip cache
- **Full logging**: Detailed crawl statistics and error messages

### 🔧 Technical Details:
- **Runner**: `ubuntu-latest` for reliability
- **Permissions**: `contents: write` for automated commits
- **Git config**: Automated bot user for clean commit history
- **Dependencies**: Installs from `requirements.txt`

The live crawling results are automatically available in your repository's `NEWS.md` file!

## Error Handling

The crawler includes basic error handling with automatic retries and graceful degradation when sources are unavailable.

## License

MIT License - see LICENSE file for details.

## Credits

Modified from:
- [ngntrgduc/HCMUS-news-crawler](https://github.com/ngntrgduc/HCMUS-news-crawler)
- [huytrinhm/hcmus-news-crawler](https://github.com/huytrinhm/hcmus-news-crawler)
