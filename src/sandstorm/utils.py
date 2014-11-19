# -*- coding: utf-8 -*-
import os
import inspect


def get_caller_module(depth=0):
    dotted = module = path = dirpath = None
    frame = inspect.currentframe().f_back.f_back
    for ii in range(depth):
        frame = frame.f_back
    dotted = frame.f_globals['__name__']
    fromlist = []
    if dotted.count('.') > 0:  # sub module or sub package
        fromlist = '.'.join(dotted.split('.')[:-1])

    try:
        module = __import__(dotted, globals={}, locals={}, fromlist=fromlist)
    except ImportError:  # pragma: no cover
        assert False, 'can not import module: {}: {}'.format(dotted, frame)
    else:
        path = module.__file__
        dirpath = os.path.dirname(path)
    return dotted, module, path, dirpath


def normalize_dotted_name(rel, current):
    """
    >>> normalize_dotted_name('...p', 'a.b.c.d.e')
    'a.b.c.p'
    """
    modules = current.split('.')
    modules.append('.')
    if rel.startswith('.'):
        while rel.startswith('.'):
            rel = rel[1:]
            modules = modules[:-1]
    else:
        modules = []
    modules.append(rel)
    abs_dotted_name = '.'.join(modules)
    abs_dotted_name = (
        abs_dotted_name[1:]
        if abs_dotted_name.startswith('.') else abs_dotted_name)
    return abs_dotted_name
