import asyncio
import aiohttp
import aiofiles
import arxiv
import os
import re
import logging
import time
import textwrap
from concurrent.futures import ThreadPoolExecutor
from functools import wraps
from collections import deque

# ================= 配置区域 =================
# 核心频率限制：每秒最多3次请求（搜索+下载合计）
MAX_REQUESTS_PER_SECOND = 2
DOWNLOAD_CONCURRENCY = 8    # 下载并发数（由频率控制器兜底，可适当调高）
# SEARCH_CONCURRENCY = 3      # 搜索并发数（≤MAX_REQUESTS_PER_SECOND）
MAX_RETRIES = 3             # 重试次数（频率合规后可减少）
BASE_DELAY = 0.1            # 基础延迟（频率控制后无需大延迟）
DOWNLOAD_DIR = "Paper_Library_Async_Optimized"
LOG_FILE = "download_mission_optimized.log"

# ================= 日志配置 =================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE, encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ================= 频率控制器（核心） =================
class RateLimiter:
    """令牌桶算法实现：严格控制每秒请求数不超过指定值"""
    def __init__(self, max_requests_per_second):
        self.max_requests = max_requests_per_second
        self.tokens = max_requests_per_second  # 初始令牌数
        self.last_refill_time = time.time()
        self.lock = asyncio.Lock()

    async def acquire(self):
        """获取令牌（阻塞直到有可用令牌）"""
        async with self.lock:
            # 1. 计算时间差，补充令牌（每秒补充max_requests个）
            now = time.time()
            time_passed = now - self.last_refill_time
            new_tokens = time_passed * self.max_requests
            if new_tokens > 0:
                self.tokens = min(self.max_requests, self.tokens + new_tokens)
                self.last_refill_time = now

            # 2. 如果令牌不足，等待直到有令牌
            while self.tokens < 1:
                await asyncio.sleep(0.01)  # 短轮询
                now = time.time()
                time_passed = now - self.last_refill_time
                new_tokens = time_passed * self.max_requests
                if new_tokens > 0:
                    self.tokens += new_tokens
                    self.last_refill_time = now

            # 3. 消耗1个令牌
            self.tokens -= 1
            return True

# ================= 工具函数 =================
def sanitize_filename(filename):
    clean = re.sub(r'[\\/*?:"<>|]', "", filename)
    return clean.strip()[:150]

def generate_bibtex(result):
    """同步生成 BibTeX 字符串"""
    short_id = result.get_short_id()
    try:
        first_author = result.authors[0].name.split(' ')[-1].lower()
    except:
        first_author = "unknown"
    year = result.published.year
    first_word = result.title.split(' ')[0].lower()
    cite_key = f"{re.sub(r'[^a-z]', '', first_author)}{year}{re.sub(r'[^a-z]', '', first_word)}"
    authors = " and ".join([a.name for a in result.authors])
    
    return textwrap.dedent(f"""
    @misc{{{cite_key},
      title={{{result.title}}}, 
      author={{{authors}}},
      year={{{year}}},
      eprint={{{short_id}}},
      archivePrefix={{arXiv}},
      primaryClass={{{result.primary_category}}},
      url={{{result.entry_id}}}
    }}
    """).strip()

# ================= 核心异步类 =================
class OptimizedPaperDownloader:
    def __init__(self, download_dir):
        self.download_dir = download_dir
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)
        
        self.processed_ids = set()
        self.sem_download = asyncio.Semaphore(DOWNLOAD_CONCURRENCY)
        self.rate_limiter = RateLimiter(MAX_REQUESTS_PER_SECOND)  # 全局频率控制
        
    async def download_file(self, session, url, file_path, file_type="File"):
        """带频率控制的异步下载函数"""
        if os.path.exists(file_path):
            logger.info(f"⏭️  [Skip] {file_type} exists: {os.path.basename(file_path)}")
            return True

        async with self.sem_download:
            # 第一步：获取频率令牌（保证每秒≤3次请求）
            await self.rate_limiter.acquire()
            
            for attempt in range(MAX_RETRIES):
                try:
                    headers = {
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
                    }
                    async with session.get(url, headers=headers, timeout=60) as response:
                        if response.status == 200:
                            async with aiofiles.open(file_path, 'wb') as f:
                                while True:
                                    chunk = await response.content.read(1024 * 64)
                                    if not chunk:
                                        break
                                    await f.write(chunk)
                            logger.info(f"✅ [Done] {file_type} downloaded: {os.path.basename(file_path)}")
                            return True
                        elif response.status in [403, 429]:
                            wait_time = BASE_DELAY * (2 ** attempt)
                            logger.warning(f"⚠️  [Rate Limit] {response.status} on {file_type}. Sleeping {wait_time}s...")
                            await asyncio.sleep(wait_time)
                        else:
                            logger.error(f"❌ [Fail] {file_type} HTTP {response.status}: {url}")
                            return False
                except Exception as e:
                    logger.warning(f"⚠️  [Retry {attempt+1}/{MAX_RETRIES}] Error downloading {file_type}: {e}")
                    await asyncio.sleep(BASE_DELAY * (attempt + 1))
            
            logger.error(f"❌ [GiveUp] Failed to download {file_type} after retries: {url}")
            return False

    async def async_search(self, query, max_results):
        """异步包装的搜索函数（带频率控制）"""
        # 第一步：获取频率令牌（保证搜索请求也遵守每秒≤3次）
        await self.rate_limiter.acquire()
        
        logger.info(f"🔍 Searching: {query[:50]}...")
        client = arxiv.Client(
            page_size=50,
            delay_seconds=0.34,  # 频率控制器已兜底，无需大延迟
            num_retries=2
        )
        search = arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.Relevance,
            sort_order=arxiv.SortOrder.Descending
        )
        
        loop = asyncio.get_running_loop()
        try:
            # 搜索是阻塞操作，扔到线程池
            results = await loop.run_in_executor(
                None,  # 使用默认线程池
                lambda: list(client.results(search))
            )
            logger.info(f"📄 Found {len(results)} papers for query: {query[:50]}...")
            return results
        except arxiv.HTTPError as e:
            logger.error(f"❌ Search failed (HTTP {e.status_code}): {query[:50]}...")
            return []
        except Exception as e:
            logger.error(f"❌ Search error: {query[:50]}... Error: {e}")
            return []

    async def process_paper(self, session, paper):
        """处理单篇论文：创建文件夹，生成Bib，下载文件"""
        paper_id = paper.get_short_id()
        if paper_id in self.processed_ids:
            return
        self.processed_ids.add(paper_id)

        safe_title = sanitize_filename(paper.title)
        paper_dir = os.path.join(self.download_dir, safe_title)
        if not os.path.exists(paper_dir):
            os.makedirs(paper_dir)

        # 保存 BibTeX（同步IO，不占请求频率）
        bib_path = os.path.join(paper_dir, "citation.bib")
        with open(bib_path, "w", encoding="utf-8") as f:
            f.write(generate_bibtex(paper))

        # 准备下载任务
        pdf_url = paper.pdf_url
        source_url = f"https://export.arxiv.org/e-print/{paper_id}"
        # source_url = f"https://arxiv.org/e-print/{paper_id}"
        pdf_path = os.path.join(paper_dir, f"{safe_title}.pdf")
        source_path = os.path.join(paper_dir, "source.tar.gz")

        # 并发下载PDF和源码（但频率控制器会保证总请求≤3次/秒）
        await asyncio.gather(
            self.download_file(session, pdf_url, pdf_path, "PDF"),
            self.download_file(session, source_url, source_path, "Source")
        )

    async def main_pipeline(self, queries, max_results_per_query=20):
        """优化后的主流程：频率控制+异步并发"""
        connector = aiohttp.TCPConnector(limit=DOWNLOAD_CONCURRENCY + 5)
        async with aiohttp.ClientSession(connector=connector) as session:
            logger.info("🚀 Starting Optimized Async Download Mission...")
            logger.info(f"📊 Rate Limit: {MAX_REQUESTS_PER_SECOND} requests/second")
            
            # 第一阶段：异步并发搜索（带频率控制）
            search_tasks = []
            for query in queries:
                task = asyncio.create_task(self.async_search(query, max_results_per_query))
                search_tasks.append(task)
            
            logger.info(f"🔎 Starting {len(search_tasks)} search tasks (rate-limited)...")
            all_search_results = await asyncio.gather(*search_tasks)
            
            # 展平结果并去重（按paper_id）
            paper_dict = {}
            for res in all_search_results:
                for paper in res:
                    paper_dict[paper.get_short_id()] = paper
            total_papers = list(paper_dict.values())
            logger.info(f"📊 Total unique papers found: {len(total_papers)}")
            
            # 第二阶段：异步并发下载（带频率控制）
            download_tasks = []
            for paper in total_papers:
                task = asyncio.create_task(self.process_paper(session, paper))
                download_tasks.append(task)
            
            if download_tasks:
                logger.info(f"🔥 Spawning {len(download_tasks)} download tasks (rate-limited)...")
                await asyncio.gather(*download_tasks)
            else:
                logger.warning("⚠️ No papers found to download.")
                    
        logger.info("✨ Optimized Mission Complete! Check log for details.")

# ================= 执行入口 =================
if __name__ == "__main__":
    # 你的查询列表
    ALL_QUERIES = [
        'ti:"agent"',
        'ti:"agent"',
        # 可添加更多查询
    ]
    
    downloader = OptimizedPaperDownloader(DOWNLOAD_DIR)
    
    try:
        if os.name == 'nt':
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
            
        asyncio.run(downloader.main_pipeline(ALL_QUERIES, max_results_per_query=50))
    except KeyboardInterrupt:
        logger.info("🛑 User stopped the process.")
    except Exception as e:
        logger.error(f"💥 Fatal Error: {e}", exc_info=True)