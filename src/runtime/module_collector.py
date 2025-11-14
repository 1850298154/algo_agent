import sys
import importlib
from types import ModuleType
from typing import Dict, List, Optional


def collect_builtin_modules() -> Dict[str, ModuleType]:
    """收集所有内置模块（sys.builtin_module_names）"""
    builtin_modules = {}
    for mod_name in sys.builtin_module_names:
        try:
            mod = importlib.import_module(mod_name)
            builtin_modules[mod_name] = mod
        except ImportError:
            continue  # 忽略无法导入的内置模块
    return builtin_modules


def collect_third_party_modules() -> Dict[str, ModuleType]:
    """收集所有已安装的第三方模块（site-packages/dist-packages 下）"""
    third_party_modules = {}
    for mod_name, mod in sys.modules.items():
        # 过滤条件：模块对象 + 非内置 + 有 __file__（排除虚拟模块）+ 在 site-packages 中
        if (isinstance(mod, ModuleType)
            and mod_name not in sys.builtin_module_names
            and hasattr(mod, "__file__")
            and mod.__file__ is not None
            and ("site-packages" in mod.__file__ or "dist-packages" in mod.__file__)):
            third_party_modules[mod_name] = mod
    return third_party_modules


def collect_custom_modules(custom_mod_names: Optional[List[str]]) -> Dict[str, ModuleType]:
    """
    收集指定的自定义模块
    :param custom_mod_names: 自定义包名列表（如 ["my_package"]）
    :return: {模块名: 模块对象}
    """
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


def get_all_injected_modules(
    include_builtin: bool = True,
    include_third_party: bool = True,
    include_custom: Optional[List[str]] = None
) -> Dict[str, ModuleType]:
    """
    整合所有需要注入的模块（入口函数）
    :param include_builtin: 是否包含内置模块
    :param include_third_party: 是否包含第三方模块
    :param include_custom: 自定义模块列表
    :return: 所有可注入的模块字典
    """
    injected_modules = {}

    # 1. 内置模块
    if include_builtin:
        builtin = collect_builtin_modules()
        injected_modules.update(builtin)
        print(f"📊 收集到内置模块 {len(builtin)} 个")

    # 2. 第三方模块
    if include_third_party:
        third_party = collect_third_party_modules()
        injected_modules.update(third_party)
        print(f"📊 收集到第三方模块 {len(third_party)} 个")

    # 3. 自定义模块
    custom = collect_custom_modules(include_custom)
    injected_modules.update(custom)
    print(f"📊 收集到自定义模块 {len(custom)} 个")

    return injected_modules