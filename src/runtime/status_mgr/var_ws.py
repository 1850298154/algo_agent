"""
This module handles the workspace functionality for the runtime environment.

"""
import copy
from re import A
from typing import Any, Dict, Optional, Union

from src.runtime.status_mgr import var_store

arg_globals_list: list[dict] = []
out_globals_list: list[dict] = []


def __create_workspace() -> dict[str, Any]:
    workspace:dict[str, Any] = {}
    exec("", workspace)
    return workspace


def initialize_workspace() -> dict[str, Any]:
    workspace: dict[str, Any] = __create_workspace()
    workspace.update({'__name__': '__main__'})
    return workspace


def get_workspace_globals_dict(workspace: dict[str, Any], include_special_vars: bool = False):
    if include_special_vars:
        return {k: v for k, v in workspace.items()}
    return {k: v for k, v in workspace.items() if not k.startswith('__')}


def get_workspace_globals_keys(workspace: dict[str, Any], include_special_vars: bool = False):
    if include_special_vars:
        return [k for k in workspace.keys()]
    return [k for k in workspace.keys() if not k.startswith('__')]


def filter_and_deepcopy_globals(original_globals: dict[str, Any]) -> dict[str, Any]:
    """
    过滤并深拷贝 globals 字典。
    过滤规则：
    1. 排除键为 '__builtins__' 的项。
    2. 排除值为模块类型的项。
    """
    def _is_serializable(value) -> bool:
        """
        判断单个对象是否可被 pickle 序列化
        :param value: 任意待判断的 Python 对象
        :return: 可序列化返回 True，不可序列化返回 False
        """
        import pickle
        try:
            # 使用最高协议版本序列化（兼容性最好），仅验证不保存
            pickle.dumps(value, protocol=pickle.HIGHEST_PROTOCOL)
            return True
        except (
            # 捕获所有序列化相关异常
            pickle.PicklingError,
            TypeError,
            AttributeError,
            RecursionError,
            MemoryError
        ):
            return False    
    filtered_dict = {}
    for key, value in original_globals.items():
        # 检查键是否为 '__builtins__'
        if key == '__builtins__':
            continue
        # 检查值是否为模块类型
        import sys
        if isinstance(value, type(sys)):  # 使用 sys 模块的类型来判断其他模块
            continue
        if _is_serializable(value) is False:
            continue
        # 对符合条件的值进行深拷贝并添加到新字典
        filtered_dict[key] = copy.deepcopy(value)
    return filtered_dict


def get_arg_globals() -> dict[str, Any]:
    global arg_globals_list
    if not arg_globals_list:
        arg_globals = initialize_workspace()
        filter_arg_globals = filter_and_deepcopy_globals(arg_globals)
        arg_globals_list.append(filter_arg_globals)
    else:
        arg_globals = out_globals_list[-1]
        filter_arg_globals = filter_and_deepcopy_globals(arg_globals)
        arg_globals_list.append(filter_arg_globals)
    return filter_arg_globals


def append_out_globals(out_globals: dict[str, Any]):
    global out_globals_list
    filter_out_globals = filter_and_deepcopy_globals(out_globals)
    var_store.dump_globals(filter_out_globals, len(out_globals_list)+1)
    out_globals_list.append(filter_out_globals)


if __name__ == '__main__':
    # workspace = initialize_workspace()
    workspace = initialize_workspace()
    import pandas as pd
    df = pd.DataFrame({'a': [1, 2, 3]})
    workspace ['my_df'] = df
    print('# create workspace:\n',workspace)
    append_out_globals(workspace)
    load_globals = var_store.load_globals()
    print('# load_globals:\n',load_globals)
    print('# get_workspace_globals_dict(include_special_vars=False):\n',get_workspace_globals_dict(workspace, include_special_vars=False))
    print('# get_workspace_globals_keys(include_special_vars=False):\n',get_workspace_globals_keys(workspace, include_special_vars=False))
    print('# get_workspace_globals_keys(include_special_vars=True):\n',get_workspace_globals_keys(workspace, include_special_vars=True))
    print('# get_workspace_globals_dict(include_special_vars=True):\n',get_workspace_globals_dict(workspace, include_special_vars=True))
