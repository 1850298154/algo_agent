import os
import asyncio
import aiofiles
from src.retrieval.arXiv.utils.logger import logger
from src.retrieval.arXiv.utils.helpers import sanitize_filename
from src.retrieval.arXiv.core.network import RateLimitedClient
from src.retrieval.arXiv import arxiv_pydantic

class DownloadService:
    def __init__(self, network_client: RateLimitedClient, download_dir: str):
        self.client = network_client
        self.base_dir = download_dir
        self.processed_ids = set()

    async def _download_file(self, url: str, path: str, desc: str):
        """内部下载实现，使用流式传输"""
        if os.path.exists(path):
            logger.info(f"⏭️  [Skip] {desc} exists.")
            return

        async with self.client.get_stream(url, context_info=desc) as response:
            if response:
                logger.info(f"🚀 [Downloading] {desc}")
                try:
                    async with aiofiles.open(path, 'wb') as f:
                        async for chunk in response.content.iter_chunked(64 * 1024):
                            await f.write(chunk)
                    logger.info(f"✅ [Done] {desc}")
                except Exception as e:
                    logger.error(f"❌ [Write Error] {desc}: {e}")
                    if os.path.exists(path):
                        os.remove(path) # 删除不完整文件

    async def process_paper(self, paper: arxiv_pydantic.Result):
        """处理单篇论文的所有下载任务"""
        paper_id = paper.get_short_id()
        
        if paper_id in self.processed_ids:
            return
        self.processed_ids.add(paper_id)

        clean_title = sanitize_filename(paper.title)
        paper_dir = os.path.join(self.base_dir, clean_title)
        
        if not os.path.exists(paper_dir):
            os.makedirs(paper_dir)

        # 并发下载 PDF 和 Source (都会消耗令牌)
        src_url = f"https://export.arxiv.org/e-print/{paper_id}"
        bib_url = f"https://export.arxiv.org/bibtex/{paper_id}"
        pdf_url = paper.pdf_url
        logger.info(f"📥 [Queue] {paper_id} - {src_url}")
        logger.info(f"📥 [Queue] {paper_id} - {bib_url}")
        logger.info(f"📥 [Queue] {paper_id} - {pdf_url}")

        src_path = os.path.join(paper_dir, f"{clean_title}.tar.gz")
        bib_path = os.path.join(paper_dir, f"{clean_title}.bib")
        pdf_path = os.path.join(paper_dir, f"{clean_title}.pdf")
        logger.info(f"📼 [Store] {paper_id} - {src_url}")
        logger.info(f"📼 [Store] {paper_id} - {bib_url}")
        logger.info(f"📼 [Store] {paper_id} - {pdf_url}")

        task_src = self._download_file(src_url, src_path, f"SRC [{paper_id}]")
        task_bib = self._download_file(bib_url, bib_path, f"BIB [{paper_id}]")
        task_pdf = self._download_file(pdf_url, pdf_path, f"PDF [{paper_id}]")

        await asyncio.gather(
            task_pdf, 
            task_src, 
            task_bib,
            )