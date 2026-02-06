import requests
import json
import gzip
import os

from src.utils.log_decorator import global_logger
from src.retrieval.aella.aella_models import (
    PaperListResponse,
    PaperDetailResponse,
    ClusterListResponse,
    SearchResponse,
)

class LaionAPIClient:
    def __init__(self):
        self.base_url = "https://laion-api.inference.net"
        
        self.headers = {
            'accept': '*/*',
            'accept-language': 'zh-CN,zh-TW;q=0.9,zh;q=0.8,en-US;q=0.7,en;q=0.6,en-GB;q=0.5',
            'origin': 'https://aella.inference.net',
            'priority': 'u=1, i',
            'referer': 'https://aella.inference.net/',
            'sec-ch-ua': '"Not(A:Brand";v="8", "Chromium";v="144", "Google Chrome";v="144"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'accept-encoding': 'gzip, deflate, br', 
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36'
        }

    def _make_request(self, endpoint, params=None):
        url = f"{self.base_url}{endpoint}"
        global_logger.info(f"请求: {url} | 参数: {params}")
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            
            content_bytes = response.content

            # --- Gzip 处理逻辑 ---
            is_custom_compressed = response.headers.get('x-content-compressed') == 'gzip'
            
            if is_custom_compressed:
                try:
                    content_bytes = gzip.decompress(content_bytes)
                    print(f"  -> 检测到 x-content-compressed: gzip，已手动解压。")
                except Exception as e:
                    print(f"  -> 解压失败: {e}")
            # --------------------

            return json.loads(content_bytes)

        except requests.exceptions.RequestException as e:
            print(f"  -> 网络请求错误: {e}")
            return {"error": str(e)}
        except json.JSONDecodeError as e:
            print(f"  -> JSON 解析错误: {e}")
            return {"error": "Invalid JSON"}

    # 定义各个接口方法
    def get_papers(self):
        resp = self._make_request("/api/papers")
        ret = PaperListResponse(**resp)
        return ret

    def get_paper_details(self, paper_id):
        resp = self._make_request(f"/api/papers/{paper_id}")
        ret = PaperDetailResponse(**resp)
        return ret

    def get_clusters(self):
        resp = self._make_request("/api/clusters")
        ret = ClusterListResponse(**resp)
        return ret

    def search(self, query):
        resp = self._make_request("/api/search", params={'q': query})
        ret = SearchResponse(**resp)
        return ret

_client = LaionAPIClient()


def all_papers():
    # 1. /api/papers
    return _client.get_papers()

def get_paper_details(paper_id):
    # 2. /api/papers/{id} -> papers,18721
    return _client.get_paper_details(paper_id)

def all_clusters():
    # 3. /api/clusters
    return _client.get_clusters()

def search_uav(query):
    # 4. /api/search
    return _client.search(query)

if __name__ == "__main__":
    # 示例调用
    print(all_papers())
    print(get_paper_details(18721))
    print(all_clusters())
    print(search_uav("UAV"))