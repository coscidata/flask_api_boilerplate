# -*- coding: utf-8 -*-
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEFAULT_PAGE = 0
DEFAULT_COUNT_PRE_PAGE = 10

PAGE_COUNT_PARAMS = {
    'page': {
        'default': DEFAULT_PAGE,
        'type_': int
    },
    'count': {
        'default': DEFAULT_COUNT_PRE_PAGE,
        'type_': int
    },
}
