import pathlib

# 创建一个Path对象（示例路径）
path_obj = pathlib.Path("./logs/app.log")

# 方法1：基础转换（最常用）
str_path = str(path_obj)
print(f"str() 转换：{str_path}，类型：{type(str_path)}")

# 方法2：跨平台POSIX风格路径
posix_str = path_obj.as_posix()
print(f"as_posix() 转换：{posix_str}，类型：{type(posix_str)}")

# 方法3：转换为绝对路径字符串
abs_str = str(path_obj.resolve())
print(f"绝对路径字符串：{abs_str}，类型：{type(abs_str)}")
abs_str = path_obj.resolve().__str__()
print(f"绝对路径字符串：{abs_str}，类型：{type(abs_str)}")
abs_str = path_obj.resolve().as_posix()
print(f"绝对路径字符串：{abs_str}，类型：{type(abs_str)}")
abs_str = path_obj.resolve()
print(f"绝对路径字符串：{abs_str}，类型：{type(abs_str)}")

# 实际使用场景：拼接字符串
file_name = "new_log.log"
new_str_path = str(path_obj.parent) + "/" + file_name
print(f"拼接后的路径：{new_str_path}")