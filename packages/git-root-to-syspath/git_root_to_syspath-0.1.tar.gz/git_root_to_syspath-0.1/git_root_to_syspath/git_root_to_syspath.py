# -*- coding: utf-8 -*-
__author__ = "Ivo Marvan"
__email__ = "ivo@marvan.cz"
__description__ = '''
    Inserts the nearest git repository root into sys.path.

    This is useful when we want to run python scripts (for example for debugging) 
    from different depths of the directory structure.  
    
    
'''


import os
import sys
import inspect

__dir2git_root = {}

def normal_path(path: str=None) -> str:
    """
    Returns normal form of path.
    """
    return os.path.normpath(os.path.realpath(os.path.expanduser(path)))


def agr(*args, **kwargs) -> str:
    """
    syntactics shugger1
    """
    return __git_root_to_sys_path(*args, **kwargs)


def __git_root_to_sys_path(path: str=None, debug: bool = False) -> str:
    """
    Get git root for caller. Use cache.
    """
    if path is None:
        path = os.path.dirname(inspect.stack()[2][1])
        path = os.path.realpath(path)
    try:
        return __dir2git_root[path]
    except KeyError:
        pass

    git_root = __get_git_root_dir(path)

    if not git_root in sys.path:
        sys.path.append(git_root)
    __dir2git_root[path] = git_root

    if debug:
        __debug(path)

    return git_root


def __debug(path: str=None):
    from pprint import pprint
    print('current path', path)
    print('--- dir -> it\'s git root')
    pprint(__dir2git_root, indent=3)


def __get_git_root_dir(path: str=None) -> str:
    """
    Returns (nearest) git root. (The root of a submodule is the git root also.)
    """
    while True:
        git_path = os.path.join(path,'.git')
        if os.path.exists(git_path):
            return path
        parent = os.path.dirname(path)
        if parent == path:
            raise RuntimeWarning("Cannot find git root")
        path = parent

