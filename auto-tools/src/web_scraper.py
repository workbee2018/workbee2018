#!/usr/bin/env python3
"""
Web Scraper - 通用网页数据抓取工具
展示：HTTP 请求、HTML 解析、数据导出能力
"""

import requests
from bs4 import BeautifulSoup
import json
import csv
from typing import Dict, List, Optional


class Scraper:
    """通用网页抓取器"""
    
    def __init__(self, headers: Optional[Dict] = None):
        self.session = requests.Session()
        self.headers = headers or {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.session.headers.update(self.headers)
    
    def scrape(self, url: str, selector: Optional[str] = None) -> Dict:
        """
        抓取网页内容
        
        Args:
            url: 目标 URL
            selector: CSS 选择器（可选）
        
        Returns:
            抓取的数据字典
        """
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            result = {
                'url': url,
                'title': soup.title.string if soup.title else 'N/A',
                'status': response.status_code
            }
            
            if selector:
                elements = soup.select(selector)
                result['content'] = [el.get_text(strip=True) for el in elements]
            else:
                result['content'] = soup.get_text(strip=True)[:500]  # 前 500 字符
            
            return result
            
        except Exception as e:
            return {'error': str(e), 'url': url}
    
    def scrape_to_json(self, url: str, output_file: str, **kwargs) -> bool:
        """抓取并保存为 JSON"""
        data = self.scrape(url, **kwargs)
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"保存失败：{e}")
            return False
    
    def scrape_to_csv(self, url: str, output_file: str, **kwargs) -> bool:
        """抓取并保存为 CSV"""
        data = self.scrape(url, **kwargs)
        try:
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(data.keys())
                writer.writerow(data.values())
            return True
        except Exception as e:
            print(f"保存失败：{e}")
            return False


def main():
    """示例用法"""
    scraper = Scraper()
    
    # 示例 1：抓取网页标题
    print("示例 1：抓取网页")
    result = scraper.scrape('https://www.python.org')
    print(f"标题：{result.get('title', 'N/A')}")
    print(f"状态：{result.get('status', 'N/A')}")
    
    # 示例 2：保存为 JSON
    print("\n示例 2：保存为 JSON")
    if scraper.scrape_to_json('https://news.ycombinator.com', 'output.json'):
        print("✓ JSON 保存成功")
    
    # 示例 3：抓取特定元素
    print("\n示例 3：抓取特定元素")
    result = scraper.scrape('https://news.ycombinator.com', selector='.titleline a')
    if 'content' in result:
        print(f"找到 {len(result['content'])} 个标题")
        for i, title in enumerate(result['content'][:5], 1):
            print(f"  {i}. {title}")


if __name__ == '__main__':
    main()
