
import asyncio

from src.ui.file_upload import (
    files_view,
)
from src.ui.message import (
    msg_view,
)
async def main():
    await files_view.files_upload_view()
    await msg_view.msg_view()
if __name__ == "__main__":
    # 错误写法（会报错）：asyncio.run(main())
    # 正确写法：Streamlit原生支持，直接调用async函数
    asyncio.run(main()) 

