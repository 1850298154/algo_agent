"""
This module handles the workspace functionality for the runtime environment.

"""


def __create_workspace() -> dict:
    workspace = {}
    exec("", workspace)
    return workspace


def initialize_workspace() -> dict:
    workspace: dict = __create_workspace()
    workspace.update({'__name__': '__main__'})
    return workspace


def get_workspace_globals_dict(workspace: dict, include_special_vars: bool = False):
    if include_special_vars:
        return {k: v for k, v in workspace.items()}
    return {k: v for k, v in workspace.items() if not k.startswith('__')}


def get_workspace_globals_keys(workspace: dict, include_special_vars: bool = False):
    if include_special_vars:
        return [k for k in workspace.keys()]
    return [k for k in workspace.keys() if not k.startswith('__')]


if __name__ == '__main__':
    # workspace = initialize_workspace()
    workspace = __create_workspace()
    print('# create workspace:\n',workspace)
    print('# get_workspace_globals_dict(include_special_vars=False):\n',get_workspace_globals_dict(workspace, include_special_vars=False))
    print('# get_workspace_globals_keys(include_special_vars=False):\n',get_workspace_globals_keys(workspace, include_special_vars=False))
    print('# get_workspace_globals_keys(include_special_vars=True):\n',get_workspace_globals_keys(workspace, include_special_vars=True))
    print('# get_workspace_globals_dict(include_special_vars=True):\n',get_workspace_globals_dict(workspace, include_special_vars=True))
