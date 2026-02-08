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

# ================= 配置区域 =================
# 注意：arXiv 对并发极其敏感。建议 DOWNLOAD_CONCURRENCY 不要超过 10，否则极易被封 IP。
DOWNLOAD_CONCURRENCY = 8  
SEARCH_CONCURRENCY = 1    # 搜索改为串行（1），彻底避免并发触发限流
MAX_RETRIES = 5           # 下载失败重试次数
BASE_DELAY = 1.0          # 基础延迟（秒）
SEARCH_DELAY = 3.0        # 搜索请求之间的固定延迟（秒）
DOWNLOAD_DIR = "Paper_Library_Async"
LOG_FILE = "download_mission.log"

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

# 装饰器：为函数添加指数退避重试
def retry_on_429(max_retries=MAX_RETRIES, base_delay=BASE_DELAY):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except arxiv.HTTPError as e:
                    if e.status_code == 429:
                        # 遇到429，指数退避等待
                        wait_time = base_delay * (2 ** attempt) * 10  # 更长的等待时间
                        logger.warning(f"⚠️  [Search Rate Limit] 429 error. Retry {attempt+1}/{max_retries} after {wait_time}s...")
                        time.sleep(wait_time)
                    else:
                        raise
                except Exception as e:
                    logger.warning(f"⚠️  [Search Retry {attempt+1}/{max_retries}] Error: {e}")
                    time.sleep(base_delay * (attempt + 1))
            raise Exception(f"❌ Search failed after {max_retries} retries")
        return wrapper
    return decorator

# ================= 核心异步类 =================
class AsyncPaperDownloader:
    def __init__(self, download_dir):
        self.download_dir = download_dir
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)
        
        self.processed_ids = set()
        # 信号量用于限制最大并发，防止被封 IP
        self.sem_download = asyncio.Semaphore(DOWNLOAD_CONCURRENCY)
        
    async def download_file(self, session, url, file_path, file_type="File"):
        """通用的异步下载函数，带重试机制"""
        if os.path.exists(file_path):
            logger.info(f"⏭️  [Skip] {file_type} exists: {os.path.basename(file_path)}")
            return True

        async with self.sem_download:
            for attempt in range(MAX_RETRIES):
                try:
                    # 模拟浏览器 User-Agent 减少被拒概率
                    headers = {
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
                    }
                    async with session.get(url, headers=headers, timeout=60) as response:
                        if response.status == 200:
                            async with aiofiles.open(file_path, 'wb') as f:
                                while True:
                                    chunk = await response.content.read(1024 * 64) # 64KB chunks
                                    if not chunk:
                                        break
                                    await f.write(chunk)
                            logger.info(f"✅ [Done] {file_type} downloaded: {os.path.basename(file_path)}")
                            return True
                        elif response.status in [403, 429]:
                            # 遇到限流，指数退避
                            wait_time = BASE_DELAY * (2 ** attempt) * 5
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

    @retry_on_429(max_retries=MAX_RETRIES, base_delay=BASE_DELAY)
    def sync_search(self, query, max_results):
        """同步搜索函数 (带429重试机制)"""
        logger.info(f"🔍 Searching: {query[:50]}...")
        # 配置arxiv客户端，增加超时
        client = arxiv.Client(
            page_size=50,
            delay_seconds=SEARCH_DELAY,
            num_retries=3
        )
        search = arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.Relevance,
            sort_order=arxiv.SortOrder.Descending
        )
        # 将 generator 转换为 list 返回，方便主线程处理
        results = list(client.results(search))
        logger.info(f"📄 Found {len(results)} papers for query: {query[:50]}...")
        
        # 搜索后添加固定延迟，避免连续请求
        time.sleep(SEARCH_DELAY)
        return results

    async def process_paper(self, session, paper):
        """处理单篇论文：创建文件夹，生成Bib，创建下载任务"""
        paper_id = paper.get_short_id()
        
        # 去重检查
        if paper_id in self.processed_ids:
            return
        self.processed_ids.add(paper_id)

        safe_title = sanitize_filename(paper.title)
        paper_dir = os.path.join(self.download_dir, safe_title)
        
        if not os.path.exists(paper_dir):
            os.makedirs(paper_dir)

        # 1. 保存 BibTeX (本地IO，很快，直接同步做)
        bib_path = os.path.join(paper_dir, "citation.bib")
        with open(bib_path, "w", encoding="utf-8") as f:
            f.write(generate_bibtex(paper))

        # 2. 准备下载任务
        pdf_url = paper.pdf_url
        source_url = f"https://arxiv.org/e-print/{paper_id}"
        
        pdf_path = os.path.join(paper_dir, f"{safe_title}.pdf")
        source_path = os.path.join(paper_dir, "source.tar.gz")

        # 并发执行 PDF 和 Source 下载
        await asyncio.gather(
            self.download_file(session, pdf_url, pdf_path, "PDF"),
            self.download_file(session, source_url, source_path, "Source")
        )

    async def main_pipeline(self, queries, max_results_per_query=20):
        # 创建一个 TCP 连接池
        connector = aiohttp.TCPConnector(limit=DOWNLOAD_CONCURRENCY + 5)
        async with aiohttp.ClientSession(connector=connector) as session:
            
            loop = asyncio.get_running_loop()
            tasks = []
            
            logger.info("🚀 Starting Async Download Mission...")
            
            # 使用 ThreadPoolExecutor 来运行阻塞的 arxiv.Search
            with ThreadPoolExecutor(max_workers=SEARCH_CONCURRENCY) as pool:
                # 1. 第一阶段：串行搜索并收集所有论文元数据（避免并发触发限流）
                all_search_results = []
                logger.info(f"📋 Starting search for {len(queries)} queries (serial mode)...")
                
                for idx, query in enumerate(queries):
                    try:
                        logger.info(f"🔍 Query {idx+1}/{len(queries)}: {query[:50]}...")
                        # 串行执行每个搜索请求
                        future = loop.run_in_executor(pool, self.sync_search, query, max_results_per_query)
                        result = await future
                        all_search_results.append(result)
                    except Exception as e:
                        logger.error(f"❌ Failed to search query {idx+1}: {query[:50]}... Error: {e}")
                        continue
                
                # 展平结果
                total_papers = [p for res in all_search_results for p in res]
                logger.info(f"📊 Total papers found (after dedup): {len(total_papers)}")
                
                # 2. 第二阶段：并发下载
                # 为每篇论文创建一个处理任务
                for paper in total_papers:
                    task = asyncio.create_task(self.process_paper(session, paper))
                    tasks.append(task)
                
                if tasks:
                    logger.info(f"🔥 Spawning {len(tasks)} download tasks with concurrency limit {DOWNLOAD_CONCURRENCY}...")
                    # 显示进度条 (可选，使用 tqdm 需要 async 适配，这里用简单的日志)
                    await asyncio.gather(*tasks)
                else:
                    logger.warning("⚠️ No papers found to download.")
                    
        logger.info("✨ Mission Complete! Check log for details.")

# ================= 执行入口 =================
if __name__ == "__main__":
    # 你的查询列表
    ALL_QUERIES = [
        'all:"multi-agent path planning deadlock"',
        # 'abs:"distributed multi-agent" AND abs:"deadlock breaking"',
        # 'all:"Large Language Model" AND all:"multi-agent path planning"',
        # ... 把你那几百条 query 放在这里 ...
    ]
    
    downloader = AsyncPaperDownloader(DOWNLOAD_DIR)
    
    try:
        # Windows 下 asyncio 的事件循环策略可能需要调整
        if os.name == 'nt':
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
            
        asyncio.run(downloader.main_pipeline(ALL_QUERIES, max_results_per_query=10))
    except KeyboardInterrupt:
        logger.info("🛑 User stopped the process.")
    except Exception as e:
        logger.error(f"💥 Fatal Error: {e}", exc_info=True)