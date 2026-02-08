import string

def sanitize_filename(filename: str, replace_char: str = '-') -> str:
    """
    清理文件名中的非法字符，兼容Windows/macOS/Linux
    :param filename: 原始文件名
    :param replace_char: 替换非法字符的目标字符（默认-）
    :return: 安全的文件名
    """
    # 1. 定义所有系统的非法字符集合（核心）
    illegal_chars = {
        # Windows核心非法字符
        '<', '>', ':', '"', '/', '\\', '|', '?', '*',
        # macOS核心非法字符
        ':',
        # Linux核心非法字符
        '/', '\0'  # \0是NULL字符，实际文件名中几乎不会出现，但仍做处理
    }
    # 2. 加入ASCII控制字符（0-31），提升兼容性
    control_chars = set(chr(c) for c in range(32))
    illegal_chars.update(control_chars)
    
    # 3. 创建字符替换映射表（高效批量替换）
    trans_table = str.maketrans({char: replace_char for char in illegal_chars})
    safe_filename = filename.translate(trans_table)
    
    # 4. 处理Windows保留文件名（如CON、PRN等）
    windows_reserved_names = {
        'CON', 'PRN', 'AUX', 'NUL', 'COM1', 'COM2', 'COM3', 'COM4',
        'COM5', 'COM6', 'COM7', 'COM8', 'COM9', 'LPT1', 'LPT2',
        'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9'
    }
    # 提取文件名主体（去掉扩展名）判断是否为保留名
    name_part = safe_filename.split('.')[0].upper()
    if name_part in windows_reserved_names:
        safe_filename = f"{safe_filename}{replace_char}"
    
    # 5. 处理末尾的空格/点（Windows禁止）
    safe_filename = safe_filename.rstrip(' .')
    
    # 6. 兜底：如果处理后为空，返回默认名
    if not safe_filename:
        safe_filename = f"unnamed{replace_char}"
    
    return safe_filename

# 测试示例
if __name__ == "__main__":
    test_cases = [
        "我的文件|名字?是/测试:.txt",
        "CON.txt",
        "hello\0world.mp4",  # 包含NULL字符
        "file name  . ",      # 末尾空格+点
        "<>:\"/\\|?*test"     # 全是Windows非法字符
    ]
    
    for case in test_cases:
        result = sanitize_filename(case)
        print(f"原始: {case!r} → 安全: {result!r}")