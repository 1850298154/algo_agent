import arxiv
import asyncio
from src.retrieval.arXiv.utils.logger import logger

class SearchService:
    def __init__(self, rate_limiter):
        self.limiter = rate_limiter
        # 使用原生 arxiv 客户端，但我们会控制调用它的时机
        self.client = arxiv.Client(
            page_size=50,
            delay_seconds=0.1, # 不需要库自带的延迟，我们有全局限流
            num_retries=3
        )

    async def search(self, query, max_results):
        """
        执行搜索，消耗 1 个全局请求令牌
        """
        # 1. 获取令牌 (因为搜索本质也是一次 HTTP 请求)
        await self.limiter.acquire()
        
        logger.info(f"🔍 [Search] Query: {query} (max: {max_results})")
        
        search_obj = arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.Relevance,
            sort_order=arxiv.SortOrder.Descending
        )

        loop = asyncio.get_running_loop()
        
        try:
            # 在线程池中运行同步的 arxiv 库代码
            results = await loop.run_in_executor(
                None, 
                lambda: list(self.client.results(search_obj))
            )
            logger.info(f"📄 Found {len(results)} papers for '{query}'")
            return results
        except Exception as e:
            logger.error(f"❌ Search failed for '{query}': {e}")
            return []