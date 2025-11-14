from typing import Dict, Optional, List
from types import ModuleType
import module_collector  # 导入模块收集器
import source_printer    # 导入源码打印机


def build_exec_namespace(injected_modules: Dict[str, ModuleType]) -> Dict:
    """构建 exec 的全局命名空间（合并模块和默认全局变量）"""
    # 复制当前进程的全局变量，再注入收集到的模块
    exec_globals = globals().copy()
    exec_globals.update(injected_modules)
    return exec_globals


def execute_code(
    code: str,
    exec_globals: Dict,
    code_desc: str = "自定义代码"
) -> None:
    """执行指定的代码字符串"""
    print(f"\n" + "="*60)
    print(f"🚀 开始执行 {code_desc}")
    print("="*60)

    try:
        exec(code, exec_globals)
        print(f"\n✅ {code_desc} 执行完成")
    except Exception as e:
        print(f"\n❌ {code_desc} 执行失败：{e}")


def run_exec_with_modules(
    code: str,
    include_builtin: bool = True,
    include_third_party: bool = True,
    include_custom: Optional[List[str]] = None,
    print_mod_names: Optional[List[str]] = None
) -> None:
    """
    整合流程：收集模块 → 打印源码 → 执行代码（入口函数）
    :param code: 待执行的代码字符串
    :param include_builtin: 是否包含内置模块
    :param include_third_party: 是否包含第三方模块
    :param include_custom: 自定义模块列表
    :param print_mod_names: 需要打印源码的模块名列表
    """
    # 1. 收集所有需要注入的模块
    print("📥 开始收集模块...")
    injected_modules = module_collector.get_all_injected_modules(
        include_builtin=include_builtin,
        include_third_party=include_third_party,
        include_custom=include_custom
    )
    print(f"✅ 模块收集完成，共 {len(injected_modules)} 个模块")

    # 2. 打印指定模块的源代码
    source_printer.print_specified_modules_sources(injected_modules, print_mod_names)

    # 3. 构建 exec 命名空间并执行代码
    exec_globals = build_exec_namespace(injected_modules)
    execute_code(code, exec_globals, code_desc="目标代码")