#!/usr/bin/env python3
"""
API Client - REST API 调用模板
展示：HTTP 客户端、认证、错误处理能力
"""

import requests
import json
from typing import Dict, Any, Optional
from datetime import datetime


class APIClient:
    """通用 REST API 客户端"""
    
    def __init__(
        self,
        base_url: str,
        api_key: Optional[str] = None,
        timeout: int = 30
    ):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()
        
        # 设置认证
        if api_key:
            self.session.headers.update({
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            })
        
        # 默认请求头
        self.session.headers.update({
            'User-Agent': 'APIClient/1.0',
            'Accept': 'application/json'
        })
    
    def _build_url(self, endpoint: str) -> str:
        """构建完整 URL"""
        if endpoint.startswith('http'):
            return endpoint
        return f"{self.base_url}{endpoint}"
    
    def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict] = None,
        data: Optional[Dict] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """通用请求方法"""
        url = self._build_url(endpoint)
        
        try:
            response = self.session.request(
                method=method,
                url=url,
                params=params,
                json=data,
                timeout=self.timeout,
                **kwargs
            )
            response.raise_for_status()
            
            return {
                'success': True,
                'status_code': response.status_code,
                'data': response.json() if response.content else None,
                'headers': dict(response.headers),
                'timestamp': datetime.utcnow().isoformat() + 'Z'
            }
            
        except requests.exceptions.HTTPError as e:
            return {
                'success': False,
                'error': f'HTTP Error: {e}',
                'status_code': e.response.status_code if e.response else None
            }
        except requests.exceptions.RequestException as e:
            return {
                'success': False,
                'error': f'Request Error: {e}'
            }
    
    def get(self, endpoint: str, params: Optional[Dict] = None) -> Dict:
        """GET 请求"""
        return self._request('GET', endpoint, params=params)
    
    def post(self, endpoint: str, data: Optional[Dict] = None) -> Dict:
        """POST 请求"""
        return self._request('POST', endpoint, data=data)
    
    def put(self, endpoint: str, data: Optional[Dict] = None) -> Dict:
        """PUT 请求"""
        return self._request('PUT', endpoint, data=data)
    
    def patch(self, endpoint: str, data: Optional[Dict] = None) -> Dict:
        """PATCH 请求"""
        return self._request('PATCH', endpoint, data=data)
    
    def delete(self, endpoint: str) -> Dict:
        """DELETE 请求"""
        return self._request('DELETE', endpoint)
    
    def test_connection(self) -> bool:
        """测试连接"""
        try:
            response = self.session.get(self.base_url, timeout=5)
            return response.status_code < 500
        except:
            return False


def main():
    """示例用法"""
    print("=" * 50)
    print("API Client 示例")
    print("=" * 50)
    
    # 示例 1：公共 API（无需认证）
    print("\n【示例 1：JSONPlaceholder API】")
    client = APIClient('https://jsonplaceholder.typicode.com')
    
    # GET 请求
    result = client.get('/posts/1')
    if result['success']:
        print(f"✓ 获取帖子：{result['data'].get('title', 'N/A')}")
    
    # 示例 2：带参数的请求
    print("\n【示例 2：带参数查询】")
    result = client.get('/posts', params={'userId': 1, '_limit': 3})
    if result['success']:
        posts = result['data']
        print(f"✓ 找到 {len(posts)} 个帖子")
        for post in posts:
            print(f"  - {post['title']}")
    
    # 示例 3：POST 请求
    print("\n【示例 3：创建资源】")
    new_post = {
        'title': 'My New Post',
        'body': 'This is the content',
        'userId': 1
    }
    result = client.post('/posts', data=new_post)
    if result['success']:
        print(f"✓ 创建成功，ID: {result['data'].get('id', 'N/A')}")
    
    # 示例 4：错误处理
    print("\n【示例 4：错误处理】")
    result = client.get('/invalid-endpoint')
    if not result['success']:
        print(f"✗ 请求失败：{result.get('error', 'Unknown error')}")
    
    # 示例 5：连接测试
    print("\n【示例 5：连接测试】")
    is_connected = client.test_connection()
    print(f"API 状态：{'✓ 在线' if is_connected else '✗ 离线'}")


if __name__ == '__main__':
    main()
