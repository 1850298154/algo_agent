
import os
from datetime import datetime
from pathlib import Path
from src.utils.st_decorator_util import seq_datetime
from src.utils.path_util import path_enum
from src.utils.st_decorator_util import seq_datetime


TIME = seq_datetime.GLOBAL_TIME_TAG_INSTANCE
PROJ = Path("./").resolve()

class File:
    ALL_LOG_PATH: Path = PROJ / path_enum.ProjPathEnum.LOG_DIR_NAME / TIME / path_enum.LogPathEnum.ALL_LOG_NAME
    PRINT_LOG_PATH: Path = PROJ / path_enum.ProjPathEnum.LOG_DIR_NAME / TIME / path_enum.LogPathEnum.PRINT_LOG_NAME
    TRACE_LOG_PATH: Path = PROJ / path_enum.ProjPathEnum.LOG_DIR_NAME / TIME / path_enum.LogPathEnum.TRACE_LOG_NAME
    @staticmethod
    def create_all_files():
        # 遍历类的所有属性，筛选出以"PATH"结尾的静态路径变量
        for attr_name in dir(File):
            # 跳过内置属性（如__doc__、__module__等）
            if attr_name.startswith("__"):
                continue
            # 筛选出路径类的静态变量（以PATH结尾）
            if attr_name.endswith("PATH"):
                # 获取路径值
                file_path: Path = getattr(File, attr_name)      
                if not isinstance(file_path, Path): continue          
                try:
                    # 第一步：创建父目录（如果不存在），parents=True表示递归创建所有上级目录
                    file_path.parent.mkdir(parents=True, exist_ok=True)
                    # 第二步：创建文件，exist_ok=True表示文件已存在时不报错
                    file_path.touch(exist_ok=True)
                    print(f"文件处理成功：{file_path}")
                except Exception as e:
                    # 捕获异常并提示，避免单个文件创建失败导致整体中断
                    print(f"处理文件失败 {file_path}：{str(e)}")
File.create_all_files()

class Dir:
    MSG_DIR: Path = PROJ / path_enum.ProjPathEnum.WST_DIR_NAME / TIME / path_enum.AgentPathEnum.MESSAGE_DIR_NAME
    PY_OUTPUT_DIR: Path = PROJ / path_enum.ProjPathEnum.WST_DIR_NAME / TIME / path_enum.AgentPathEnum.PY_OUTPUT_DIR_NAME
    PY_RUNTIME_VAR_DIR: Path = PROJ / path_enum.ProjPathEnum.WST_DIR_NAME / TIME / path_enum.AgentPathEnum.PY_RUNTIME_VAR_DIR_NAME

    UPLOAD_DIR: Path = PROJ / path_enum.ProjPathEnum.WST_DIR_NAME / TIME / path_enum.WstPathEnum.UPLOAD_DIR_NAME
    SCHEMA_DIR: Path = PROJ / path_enum.ProjPathEnum.WST_DIR_NAME / TIME / path_enum.WstPathEnum.SCHEMA_DIR_NAME
    @staticmethod
    def create_all_files():
        # 遍历类的所有属性，筛选出以"PATH"结尾的静态路径变量
        for attr_name in dir(Dir):
            if attr_name.startswith("__"): continue
            if attr_name.endswith("DIR"):
                dir_path: Path = getattr(Dir, attr_name)
                if not isinstance(dir_path, Path): continue
                try:
                    dir_path.mkdir(parents=True, exist_ok=True)
                    print(f"文件夹处理成功：{dir_path}")
                except Exception as e:
                    print(f"处理文件夹失败 {dir_path}：{str(e)}")
Dir.create_all_files()


