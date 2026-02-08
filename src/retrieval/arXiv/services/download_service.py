import os
import asyncio
import aiofiles
from src.retrieval.arXiv.utils.logger import logger
from src.retrieval.arXiv.utils.helpers import sanitize_filename, generate_bibtex

class DownloadService:
    def __init__(self, network_client, download_dir):
        self.client = network_client
        self.base_dir = download_dir
        self.processed_ids = set()

    async def _download_file(self, url, path, desc):
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

    async def process_paper(self, paper):
        """处理单篇论文的所有下载任务"""
        paper_id = paper.get_short_id()
        
        if paper_id in self.processed_ids:
            return
        self.processed_ids.add(paper_id)

        clean_title = sanitize_filename(paper.title)
        short_title = clean_title[:40] + "..."
        paper_dir = os.path.join(self.base_dir, clean_title)
        
        if not os.path.exists(paper_dir):
            os.makedirs(paper_dir)

        # 1. 保存 BibTeX (本地IO，不消耗令牌)
        bib_path = os.path.join(paper_dir, "citation.bib")
        if not os.path.exists(bib_path):
            with open(bib_path, "w", encoding="utf-8") as f:
                f.write(generate_bibtex(paper))

        # 2. 并发下载 PDF 和 Source (都会消耗令牌)
        pdf_url = paper.pdf_url
        source_url = f"https://export.arxiv.org/e-print/{paper_id}"
        
        pdf_path = os.path.join(paper_dir, f"{clean_title}.pdf")
        source_path = os.path.join(paper_dir, "source.tar.gz")

        task_pdf = self._download_file(pdf_url, pdf_path, f"PDF [{paper_id}]")
        task_src = self._download_file(source_url, source_path, f"SRC [{paper_id}]")

        await asyncio.gather(task_pdf, task_src)