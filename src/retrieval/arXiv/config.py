import os

# ================= 核心限制 =================
MAX_REQUESTS_PER_SECOND = 2  # 严格限制：每秒2次
DOWNLOAD_CONCURRENCY = 5     #并发数（受限于频率，设太高没意义）
MAX_RETRIES = 3
BASE_DELAY = 0.5             # 重试基础延迟

# ================= 路径配置 =================
base_dir = os.path.dirname(os.path.abspath(__file__))
DOWNLOAD_DIR = os.path.join(base_dir, "Paper_Library_Async_Optimized")
LOG_FILE = os.path.join(base_dir, "download_mission.log")

# ================= HTTP头 =================
DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}