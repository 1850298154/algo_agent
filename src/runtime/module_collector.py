import sys
import importlib
from types import ModuleType
from typing import Dict, List, Optional
import os as sys_os  # 避免与用户代码的 os 冲突
from importlib.metadata import packages_distributions

def collect_builtin_modules() -> Dict[str, ModuleType]:
    """收集 C 实现的内置模块（如 sys、builtins，无 .py 源码）"""
    builtin_modules = {}
    for mod_name in sys.builtin_module_names:
        try:
            mod = importlib.import_module(mod_name)
            # 过滤掉标准库模块（标准库有 __file__ 且是 .py 文件）
            if not (hasattr(mod, "__file__") and mod.__file__ and mod.__file__.endswith(".py")):
                builtin_modules[mod_name] = mod
        except ImportError:
            continue
    return builtin_modules


def collect_stdlib_modules() -> Dict[str, ModuleType]:
    """收集 Python 标准库模块（如 os、json、datetime，Python 实现，有 .py 源码）"""
    stdlib_modules = {}
    # 标准库路径通常在 sys.prefix + "/lib/pythonX.Y" 下
    # sys.prefix == 'D:\\zyt\\git_ln\\algo_agent\\.venv'
    # stdlib_paths == ['D:\\zyt\\git_ln\\algo_agent\\.venv\\lib\\python3.12']
    # os mod.__file__ 'C:\\Users\\zooos\\AppData\\Roaming\\uv\\python\\cpython-3.12.11-windows-x86_64-none\\Lib\\os.py'

    stdlib_paths = [sys_os.path.join(sys.prefix, "lib", f"python{sys.version_info.major}.{sys.version_info.minor}")]
    
    for mod_name, mod in sys.modules.items():
        # 过滤条件：
        # 1. 是模块对象 2. 非内置模块 3. 有 __file__ 且是 .py 文件 4. 在标准库路径下
        if (isinstance(mod, ModuleType)
            and mod_name not in sys.builtin_module_names
            and hasattr(mod, "__file__")
            and mod.__file__ is not None
            and mod.__file__.endswith(".py")
            # and any(stdlib_path in mod.__file__ for stdlib_path in stdlib_paths)
            ):
            stdlib_modules[mod_name] = mod
    return stdlib_modules


def collect_third_party_modules() -> Dict[str, ModuleType]:
    """收集所有已安装的第三方模块（site-packages/dist-packages 下）"""
    third_party_modules = {}
    for mod_name, mod in sys.modules.items():
        if (isinstance(mod, ModuleType)
            and mod_name not in sys.builtin_module_names
            and hasattr(mod, "__file__")
            and mod.__file__ is not None
            and ("site-packages" in mod.__file__ or "dist-packages" in mod.__file__)):
            third_party_modules[mod_name] = mod
    return third_party_modules


def collect_custom_modules(custom_mod_names: Optional[List[str]]) -> Dict[str, ModuleType]:
    """收集指定的自定义模块"""
    custom_modules = {}
    if not custom_mod_names:
        return custom_modules

    for mod_name in custom_mod_names:
        try:
            mod = importlib.import_module(mod_name)
            custom_modules[mod_name] = mod
            print(f"📥 成功导入自定义模块：{mod_name}")
        except ImportError as e:
            print(f"⚠️  警告：无法导入自定义模块 {mod_name}：{e}")
    return custom_modules

def get_all_installed_third_party_modules() -> Dict[str, ModuleType]:
    """获取所有已安装的第三方模块，并加载为模块对象"""
    # 1. 获取所有已安装的第三方模块名（过滤标准库）
    installed_mods = {mod: pkgs for mod, pkgs in packages_distributions().items() if pkgs}
    mod_names = list(installed_mods.keys())  # 模块名列表（如 "requests", "numpy"）
    
    # 2. 加载所有模块（注：可能耗时，按需使用）
    all_third_party = {}
    for mod_name in mod_names:
        try:
            mod = importlib.import_module(mod_name)  # 动态加载模块
            all_third_party[mod_name] = mod
        except (ImportError, ModuleNotFoundError):
            continue  # 跳过加载失败的模块（如部分依赖缺失）
    return all_third_party

def get_all_injected_modules(
    include_builtin: bool = True,
    include_stdlib: bool = True,  # 新增：是否包含标准库
    include_third_party: bool = True,
    include_all_installed: bool = True,
    include_custom: Optional[List[str]] = None
) -> Dict[str, ModuleType]:
    """整合所有需要注入的模块（新增标准库参数）"""
    injected_modules = {}

    # 1. 内置模块（C 实现）
    if include_builtin:
        builtin = collect_builtin_modules()
        injected_modules.update(builtin)
        print(f"📊 收集到内置模块（C 实现）{len(builtin)} 个")

    # 2. 标准库模块（Python 实现）
    if include_stdlib:
        stdlib = collect_stdlib_modules()
        injected_modules.update(stdlib)
        print(f"📊 收集到标准库模块（Python 实现）{len(stdlib)} 个")

    # 3. 第三方模块
    if include_third_party:
        third_party = collect_third_party_modules()
        injected_modules.update(third_party)
        print(f"📊 收集到第三方模块 {len(third_party)} 个")
    
    # 4. 安装的第三方模块（全部加载）
    if include_all_installed:
        all_installed = get_all_installed_third_party_modules()
        injected_modules.update(all_installed)
        print(f"📊 收集到安装的第三方模块 {len(all_installed)} 个")

    # 5. 自定义模块
    custom = collect_custom_modules(include_custom)
    injected_modules.update(custom)
    print(f"📊 收集到自定义模块 {len(custom)} 个")

    return injected_modules