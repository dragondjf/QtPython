#!/usr/bin/env python
# -*- coding: utf-8 -*-


import json
import qtlogger
import logging
from logging import RootLogger


def debug(*args):
    messages = [unicode(arg) for arg in args]
    ret = " ".join(messages)
    qtlogger.debug(ret)

def info(*args):
    messages = [unicode(arg) for arg in args]
    ret = " ".join(messages)
    qtlogger.info(ret)

def warning(*args):
    messages = [unicode(arg) for arg in args]
    ret = " ".join(messages)
    qtlogger.warning(ret)

def error(*args):
    messages = [unicode(arg) for arg in args]
    ret = " ".join(messages)
    qtlogger.error(ret)

def fatal(*args):
    messages = [unicode(arg) for arg in args]
    ret = " ".join(messages)
    qtlogger.fatal(ret)



class QtPythonRootLogger(RootLogger):

    def __init__(self, level):
        super(QtPythonRootLogger, self).__init__(level)

    def handle(self, record):
        if self.handlers:
            fmtMessage = self.handlers[0].formatter.format(record)
        else:
            fmtMessage = unicode(record)
        if record.levelno == logging.DEBUG:
            debug(fmtMessage)
        elif record.levelno == logging.INFO:
            info(fmtMessage)
        elif record.levelno == logging.WARNING:
            warning(fmtMessage)
        elif record.levelno == logging.ERROR:
            error(fmtMessage)
        elif record.levelno == logging.FATAL:
            fatal(fmtMessage)

logging.root = QtPythonRootLogger(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s [%(levelname)7s] [%(pathname)s%(lineno)06s] %(message)s')
ch.setFormatter(formatter)
logger = logging.root
logger.propagate = 0
logger.addHandler(ch)


logger.info("======1=======")


def test_base(a1, a2 ,a3):
    logger.info(a1)
    return 0

def returnJson(args):
    logger.warning(args)
    obj = {
        "a1": "a1",
        "a2": "a2",
        "a3": "a3",
        "a4": "a4"
    }
    ret = json.dumps(obj)
    logger.error("dssssssssssssssss")
    return ret
