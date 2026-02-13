
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
    asyncio.run(main()) 

