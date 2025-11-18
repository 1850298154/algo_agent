
def add_line_numbers(
    code_str,
    start=1,
    indent=" | ",
    skip_empty_lines=False,  # 是否跳过空行（不编号）
    line_num_format=None  # 自定义行号格式（如 "[{}] "）
):
    lines = code_str.splitlines()
    if not lines:
        return ""
    
    numbered_lines = []
    current_line_num = start
    
    # 自定义行号格式（优先级高于默认）
    if line_num_format is None:
        max_line_num = start + len(lines) - (1 if skip_empty_lines else 0)
        line_num_width = len(str(max_line_num))
        line_num_format = f"{{:>{line_num_width}}}{indent}"  # 默认右对齐
    
    for line in lines:
        # 处理空行：跳过编号或仅保留空行（不递增行号）
        stripped_line = line.strip()
        if skip_empty_lines and not stripped_line:
            numbered_lines.append(" " * len(line_num_format.format(start)) + line)  # 空行对齐
            continue
        
        # 非空行：添加编号
        numbered_line = line_num_format.format(current_line_num) + line
        numbered_lines.append(numbered_line)
        
        # 空行不递增行号（仅当 skip_empty_lines=False 时生效）
        if not skip_empty_lines or stripped_line:
            current_line_num += 1
    
    return "\n".join(numbered_lines)
