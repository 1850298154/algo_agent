import time
import asyncio
from src.retrieval.arXiv.utils.logger import logger

class TokenBucketLimiter:
    """令牌桶算法：严格控制请求速率"""
    def __init__(self, rate_per_second):
        self.rate = rate_per_second
        self.capacity = rate_per_second  # 桶容量等于每秒速率
        self.tokens = rate_per_second
        self.last_refill = time.time()
        self.lock = asyncio.Lock()

    async def acquire(self):
        """阻塞直到获取到令牌"""
        async with self.lock:
            now = time.time()
            # 补充令牌
            elapsed = now - self.last_refill
            new_tokens = elapsed * self.rate
            if new_tokens > 0:
                self.tokens = min(self.capacity, self.tokens + new_tokens)
                self.last_refill = now
            
            # 等待令牌
            while self.tokens < 1:
                wait_time = (1 - self.tokens) / self.rate
                if wait_time > 0.01:
                    # 只有需要等待较久时才打印日志，避免刷屏
                    pass 
                await asyncio.sleep(0.1)
                
                # 醒来后重新计算
                now = time.time()
                elapsed = now - self.last_refill
                new_tokens = elapsed * self.rate
                if new_tokens > 0:
                    self.tokens = min(self.capacity, self.tokens + new_tokens)
                    self.last_refill = now

            self.tokens -= 1
            return True