# 🤖 Auto Tools - Python 自动化脚本集合

实用的 Python 自动化工具，展示数据处理和 API 集成能力。

## 📦 功能列表

- 🕷️ **Web Scraper** - 网页数据抓取
- 📁 **File Organizer** - 文件自动整理
- 🔗 **API Client** - REST API 调用模板

## 🚀 快速开始

```bash
# 安装依赖
pip install -r requirements.txt

# 运行示例
python src/web_scraper.py
python src/file_organizer.py
python src/api_client.py
```

## 📋 使用示例

### Web Scraper
```python
from src.web_scraper import Scraper

scraper = Scraper()
data = scraper.scrape('https://example.com')
print(data)
```

### File Organizer
```python
from src.file_organizer import FileOrganizer

organizer = FileOrganizer('/path/to/downloads')
organizer.organize()
```

### API Client
```python
from src.api_client import APIClient

client = APIClient(base_url='https://api.example.com')
response = client.get('/endpoint')
```

## 🛠️ 技术栈

- Python 3.8+
- requests
- BeautifulSoup4
- pandas

## 📄 License

MIT License - Free to use and modify

## 📬 Contact

Available for freelance projects and bounties!
- GitHub: [Your Profile]
- Email: your.email@example.com
