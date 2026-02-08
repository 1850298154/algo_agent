import aiohttp
import asyncio
from contextlib import asynccontextmanager
from typing import Any, Optional, AsyncIterator
from src.retrieval.arXiv.config import DEFAULT_HEADERS, MAX_RETRIES, BASE_DELAY
from src.retrieval.arXiv.utils.logger import logger
from src.retrieval.arXiv.core.rate_limiter import TokenBucketLimiter

class RateLimitedClient:
    """
    异步限流 HTTP 客户端包装。

    Attributes:
        limiter: TokenBucketLimiter - 需要提供 async acquire() 的限流器实例。
        session: Optional[aiohttp.ClientSession] - aiohttp 会话对象，在 start() 后创建。
    """
    def __init__(self, rate_limiter: TokenBucketLimiter) -> None:
        self.limiter: Any = rate_limiter
        self.session: Optional[aiohttp.ClientSession] = None

    async def start(self) -> None:
        self.session = aiohttp.ClientSession(headers=DEFAULT_HEADERS)

    async def close(self) -> None:
        if self.session:
            await self.session.close()

    @asynccontextmanager
    async def get_stream(self, url: str, context_info: str = "") -> AsyncIterator[Optional[aiohttp.ClientResponse]]:
        """
        上下文管理器形式的 GET，用于流式下载。

        用法:
            async with client.get_stream(url) as resp:
                if resp is not None:
                    data = await resp.read()

        Args:
            url: str - 要请求的 URL。
            context_info: str - 日志中附带的上下文信息（可选）。

        Yields:
            Optional[aiohttp.ClientResponse] - 成功返回 aiohttp.ClientResponse，失败返回 None。
        """
        await self.limiter.acquire()  # 消耗令牌，进行限流

        for attempt in range(MAX_RETRIES):
            try:
                if self.session is None:
                    raise RuntimeError("Session not started. Call start() before requesting.")
                resp: aiohttp.ClientResponse = await self.session.get(url, timeout=60)
                if resp.status == 200:
                    try:
                        yield resp
                    finally:
                        resp.release()  # 确保释放连接
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