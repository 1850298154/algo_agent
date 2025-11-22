"""
This module handles the workspace functionality for the runtime environment.

"""
import copy
from typing import Any, Dict, Optional, Union



instance = None


def __create_workspace() -> dict:
    workspace = {}
    exec("", workspace)
    return workspace


def initialize_workspace() -> dict:
    workspace: dict = __create_workspace()
    instance = workspace.update({'__name__': '__main__'})
    return workspace


def update_workspace_globals(globals_dict: dict):
    instance.update(globals_dict)


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


if __name__ == '__main__':
    # workspace = initialize_workspace()
    workspace = __create_workspace()
    print('# create workspace:\n',workspace)
    print('# get_workspace_globals_dict(include_special_vars=False):\n',get_workspace_globals_dict(workspace, include_special_vars=False))
    print('# get_workspace_globals_keys(include_special_vars=False):\n',get_workspace_globals_keys(workspace, include_special_vars=False))
    print('# get_workspace_globals_keys(include_special_vars=True):\n',get_workspace_globals_keys(workspace, include_special_vars=True))
    print('# get_workspace_globals_dict(include_special_vars=True):\n',get_workspace_globals_dict(workspace, include_special_vars=True))
