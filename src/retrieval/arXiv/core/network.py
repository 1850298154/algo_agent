import aiohttp
import asyncio
from contextlib import asynccontextmanager
from src.retrieval.arXiv.config import DEFAULT_HEADERS, MAX_RETRIES, BASE_DELAY
from src.retrieval.arXiv.utils.logger import logger

class RateLimitedClient:
    def __init__(self, rate_limiter):
        self.limiter = rate_limiter
        self.session = None

    async def start(self):
        self.session = aiohttp.ClientSession(headers=DEFAULT_HEADERS)

    async def close(self):
        if self.session:
            await self.session.close()

    @asynccontextmanager
    async def get_stream(self, url, context_info=""):
        """
        上下文管理器形式的GET，用于流式下载。
        用法: async with client.get_stream(url) as resp: ...
        """
        await self.limiter.acquire() # ⛔️ 关卡：消耗令牌
        
        for attempt in range(MAX_RETRIES):
            try:
                resp = await self.session.get(url, timeout=60)
                if resp.status == 200:
                    yield resp
                    resp.release() # 确保释放
                    return
                elif resp.status in [403, 429]:
                    logger.warning(f"⚠️ [403/429] {context_info}. Waiting...")
                    resp.release()
                    await asyncio.sleep(BASE_DELAY * (attempt + 1))
                else:
                    logger.error(f"❌ HTTP {resp.status} - {context_info}")
                    resp.release()
                    yield None
                    return
            except Exception as e:
                logger.error(f"❌ Error {context_info}: {e}")
                await asyncio.sleep(BASE_DELAY)
        yield None