"""
This module handles the workspace functionality for the runtime environment.

"""
import copy
from typing import Any, Dict, Optional, Union



arg_globals_list: list[dict] = []
out_globals_list: list[dict] = []


def __create_workspace() -> dict:
    workspace = {}
    exec("", workspace)
    return workspace


def initialize_workspace() -> dict:
    workspace: dict = __create_workspace()
    instance = workspace.update({'__name__': '__main__'})
    return workspace


def get_workspace_globals_dict(workspace: dict, include_special_vars: bool = False):
    if include_special_vars:
        return {k: v for k, v in workspace.items()}
    return {k: v for k, v in workspace.items() if not k.startswith('__')}


def get_workspace_globals_keys(workspace: dict, include_special_vars: bool = False):
    if include_special_vars:
        return [k for k in workspace.keys()]
    return [k for k in workspace.keys() if not k.startswith('__')]


def filter_and_deepcopy_globals(original_globals: Dict[str, Any]) -> Dict[str, Any]:
    """
    过滤并深拷贝 globals 字典。
    过滤规则：
    1. 排除键为 '__builtins__' 的项。
    2. 排除值为模块类型的项。
    """
    filtered_dict = {}
    for key, value in original_globals.items():
        # 检查键是否为 '__builtins__'
        if key == '__builtins__':
            continue
        # 检查值是否为模块类型
        import sys
        if isinstance(value, type(sys)):  # 使用 sys 模块的类型来判断其他模块
            continue
        # 对符合条件的值进行深拷贝并添加到新字典
        filtered_dict[key] = copy.deepcopy(value)
    return filtered_dict


def get_arg_globals() -> dict:
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


def append_out_globals(out_globals: dict):
    global out_globals_list
    filter_out_globals = filter_and_deepcopy_globals(out_globals)
    out_globals_list.append(filter_out_globals)


if __name__ == '__main__':
    # workspace = initialize_workspace()
    workspace = __create_workspace()
    print('# create workspace:\n',workspace)
    print('# get_workspace_globals_dict(include_special_vars=False):\n',get_workspace_globals_dict(workspace, include_special_vars=False))
    print('# get_workspace_globals_keys(include_special_vars=False):\n',get_workspace_globals_keys(workspace, include_special_vars=False))
    print('# get_workspace_globals_keys(include_special_vars=True):\n',get_workspace_globals_keys(workspace, include_special_vars=True))
    print('# get_workspace_globals_dict(include_special_vars=True):\n',get_workspace_globals_dict(workspace, include_special_vars=True))
