import re
import base64
from pathlib import Path

def md_local_img_to_base64(markdown):
    # 匹配本地路径图片
    pattern = re.compile(r'!\[(.*?)\]\((.*?:.*?)\)')
    
    def replace_img(match):
        alt, path = match.groups()
        must_print = f"说明：{alt}。图片路径：{path} 。"
        try:
            b64 = base64.b64encode(Path(path.strip()).read_bytes()).decode()
            return f'![{alt}](data:image/png;base64,{b64})' + must_print
        except:
            return f'![{alt}]({path})' + must_print + "（图片加载失败，可能是路径错误或文件不存在）"
    
    return pattern.sub(replace_img, markdown)
