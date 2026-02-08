# import arxiv_pydantic
from src.retrieval.arXiv import arxiv_pydantic
import asyncio
from src.retrieval.arXiv.utils.logger import logger

class SearchService:
    def __init__(self, rate_limiter):
        self.limiter = rate_limiter
        # 使用原生 arxiv_pydantic 客户端，但我们会控制调用它的时机
        self.client = arxiv_pydantic.Client(
            page_size=50,
            delay_seconds=0.1, # 不需要库自带的延迟，我们有全局限流
            num_retries=3
        )

    async def search(self, query: str, max_results: int) -> list[arxiv_pydantic.Result]:
        """
        执行搜索，消耗 1 个全局请求令牌
        """
        # 1. 获取令牌 (因为搜索本质也是一次 HTTP 请求)
        await self.limiter.acquire()
        
        logger.info(f"🔍 [Search] Query: {query} (max: {max_results})")
        
        search_obj = arxiv_pydantic.Search(
            query=query,
            max_results=max_results,
            sort_by=arxiv_pydantic.SortCriterion.Relevance,
            sort_order=arxiv_pydantic.SortOrder.Descending
        )

        loop = asyncio.get_running_loop()
        
        try:
            # 在线程池中运行同步的 arxiv_pydantic 库代码
            results: list[arxiv_pydantic.Result] = await loop.run_in_executor(
                None, 
                lambda: list(self.client.results(search_obj))
            )
            logger.info(f"📄 Found {len(results)} papers for '{query}'")
            return results
        except Exception as e:
            logger.error(f"❌ Search failed for '{query}': {e}")
            return []