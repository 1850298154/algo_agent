import requests
import json
import gzip
import os

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
        print(f"请求: {url} | 参数: {params}")
        
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
        return self._make_request("/api/papers")

    def get_paper_details(self, paper_id):
        return self._make_request(f"/api/papers/{paper_id}")

    def get_clusters(self):
        return self._make_request("/api/clusters")

    def search(self, query):
        return self._make_request("/api/search", params={'q': query})

    def get_temporal_data(self, min_year, max_year):
        return self._make_request("/api/temporal-data", params={'min_year': min_year, 'max_year': max_year})

    def get_samples(self):
        return self._make_request("/api/samples")

    def get_sample_details(self, sample_id):
        return self._make_request(f"/api/samples/{sample_id}")

# --- 辅助函数：保存文件 ---
def save_result(index, path_slug, data):
    # 替换规则：如果path包含斜杠，用逗号代替
    safe_slug = path_slug.replace('/', ',')
    filename = f"docs/03_web_search/api_req/{index}_{safe_slug}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  -> 结果已保存至: {filename}\n")

# --- 主执行逻辑 ---
if __name__ == "__main__":
    client = LaionAPIClient()
    
    # 1. /api/papers
    print("--- 任务 1 ---")
    data = client.get_papers()
    save_result(1, "papers", data)

    # 2. /api/papers/{id} -> papers,18721
    print("--- 任务 2 ---")
    data = client.get_paper_details(18721)
    save_result(2, "papers/18721", data)

    # 3. /api/clusters
    print("--- 任务 3 ---")
    data = client.get_clusters()
    save_result(3, "clusters", data)

    # 4. /api/search
    print("--- 任务 4 ---")
    data = client.search("uav")
    save_result(4, "search", data)

    # 5. /api/temporal-data
    print("--- 任务 5 ---")
    data = client.get_temporal_data(1990, 2026)
    save_result(5, "temporal-data", data)

    # 6. /api/samples
    print("--- 任务 6 ---")
    data = client.get_samples()
    save_result(6, "samples", data)

    # 7. /api/samples/{id} -> samples,29
    print("--- 任务 7 ---")
    data = client.get_sample_details(29)
    save_result(7, "samples/29", data)

    print("所有任务完成。")