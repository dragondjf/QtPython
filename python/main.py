#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logger
import json

def debug(*args):
    messages = [unicode(arg) for arg in args]
    ret = " ".join(messages)
    logger.debug(ret)


def test_base(a1, a2, a3):
    debug(a1, a2, a3)
    return 0


def returnJson(a1, a2, a3 , a4):
    obj = {
        "a1": "1111",
        "a2": "2222",
        "a3": "1212112",
        "a4": "666"
    }
    ret = json.dumps(obj)
    debug(ret)
    return ret