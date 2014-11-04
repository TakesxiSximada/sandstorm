# -*- coding: utf-8 -*-

from .transaction import TransactionMiddleware
from .browserid import BrowseridMiddleware

MV_NORMAL = (
    BrowseridMiddleware,
    TransactionMiddleware,
    )
