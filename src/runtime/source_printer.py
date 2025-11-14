import inspect
from types import ModuleType
from typing import Optional, Dict, List


def print_single_module_source(mod: ModuleType) -> None:
    """打印单个模块的源代码（单一职责）"""
    mod_name = mod.__name__
    print(f"\n{'='*50}")
    print(f"📄 模块 {mod_name} 的源代码")
    print(f"{'='*50}")

    try:
        # 读取模块源代码（inspect.getsource 自动处理 .py 文件）
        source_code = inspect.getsource(mod)
        print(source_code)
    except TypeError:
        # 内置模块（C 实现）无 Python 源码
        print(f"💡 提示：{mod_name} 是内置模块（C 实现），无 Python 源代码")
    except OSError as e:
        # 模块文件不存在或无法访问
        print(f"❌ 错误：无法读取 {mod_name} 源代码：{e}")
    except Exception as e:
        # 其他未知错误
        print(f"❌ 未知错误（{mod_name}）：{e}")


def print_specified_modules_sources(
    injected_modules: Dict[str, ModuleType],
    print_mod_names: Optional[List[str]] = None
) -> None:
    """
    打印指定列表中的模块源代码（入口函数）
    :param injected_modules: 已注入的模块字典（来自 module_collector）
    :param print_mod_names: 需要打印源码的模块名列表
    """
    if not print_mod_names:
        print("\n⚠️  未指定需要打印源码的模块，跳过打印")
        return

    print("\n" + "="*60)
    print("🎯 开始打印指定模块源代码")
    print("="*60)

    for mod_name in print_mod_names:
        if mod_name in injected_modules:
            print_single_module_source(injected_modules[mod_name])
        else:
            print(f"\n⚠️  警告：模块 {mod_name} 未找到，无法打印源码")