import re
import textwrap
from src.retrieval.arXiv import arxiv_pydantic

def sanitize_filename(filename):
    clean = re.sub(r'[\\/*?:"<>|]', "", filename)
    return clean.strip()[:150]
