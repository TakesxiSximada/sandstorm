# -*- coding: utf-8 -*-
import os
import inspect


def get_caller_module():
    dotted = module = path, dirpath = None
    frame = inspect.currentframe().f_back.f_back
    dotted = frame.f_globals['__name__']
    try:
        module = __import__(dotted, globals={}, locals={}, fromlist=True)
    except ImportError:
        pass
    else:
        path = module.__file__
        dirpath = os.path.dirname(path)
    return dotted, module, path, dirpath
