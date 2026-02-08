import asyncio
import os
import sys
import json
from unittest.mock import Base
from pydantic import BaseModel, Field

from src.retrieval.arXiv.config import (
    MAX_REQUESTS_PER_SECOND, 
    DOWNLOAD_DIR, 
    DOWNLOAD_CONCURRENCY, 
    PAPERS_RESULT_PATH,
    )
from src.retrieval.arXiv.core.rate_limiter import TokenBucketLimiter
from src.retrieval.arXiv.core.network import RateLimitedClient
from src.retrieval.arXiv.services.search_service import SearchService
from src.retrieval.arXiv.services.download_service import DownloadService
from src.retrieval.arXiv.utils.logger import logger
from src.retrieval.arXiv import arxiv_pydantic

# 你的查询列表
QUERIES = [
    'ti:"agent"',
]

class AllPapers(BaseModel):
    papers: list[arxiv_pydantic.Result] = Field(..., description="List of all unique papers found.")

async def main():
    # 1. 初始化基础设施
    logger.info("🛠️  Initializing system...")
    
    # 核心：全局限流器 (1s 2个令牌)
    global_limiter = TokenBucketLimiter(rate_per_second=MAX_REQUESTS_PER_SECOND)
    
    # 网络客户端 (注入限流器)
    network_client = RateLimitedClient(global_limiter)
    await network_client.start()
    
    # 业务服务
    search_service = SearchService(global_limiter) # 搜索也共享同一个限流器
    download_service = DownloadService(network_client, DOWNLOAD_DIR)

    try:
        # 2. 执行搜索阶段
        search_tasks = [search_service.search(q, max_results=1) for q in QUERIES]
        logger.info("🔍 Starting search phase...")
        results_list: list[list[arxiv_pydantic.Result]] = await asyncio.gather(*search_tasks)
        
        # 去重
        all_papers = AllPapers(papers=[])
        seen_ids = set()
        for res in results_list:
            for paper in res:
                if paper.get_short_id() not in seen_ids:
                    all_papers.papers.append(paper)
                    seen_ids.add(paper.get_short_id())
        logger.info(f"📊 Total unique papers to process: {len(all_papers.papers)}")
        with open(PAPERS_RESULT_PATH, "w", encoding="utf-8") as f:
            all_papers_json_str = all_papers.model_dump_json(indent=4)
            json.dump(all_papers_json_str, f, ensure_ascii=False, indent=4)

        # 3. 执行下载阶段
        # 使用Semaphore控制最大并发任务数（虽然有令牌桶兜底，但Semaphore可以防止创建过多Task对象占用内存）
        sem = asyncio.Semaphore(DOWNLOAD_CONCURRENCY)
        async def bounded_process(paper: arxiv_pydantic.Result):
            async with sem:
                await download_service.process_paper(paper)

        download_tasks = [bounded_process(p) for p in all_papers.papers]
        if download_tasks:
            logger.info("🔥 Starting download phase...")
            await asyncio.gather(*download_tasks)
        else:
            logger.warning("⚠️  No papers found.")

    finally:
        await network_client.close()
        logger.info("✨ Mission Complete.")

if __name__ == "__main__":
    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("🛑 Stopped by user.")