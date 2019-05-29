#!/usr/bin/env python
# -*- coding: utf-8 -*-

import qtlogger
import logging
from logging import RootLogger


def debug(*args):
    messages = [arg.encode("utf-8") for arg in args]
    ret = " ".join(messages)
    qtlogger.debug(ret)


def info(*args):
    messages = [arg.encode("utf-8") for arg in args]
    ret = " ".join(messages)
    qtlogger.info(ret)


def warning(*args):
    messages = [arg.encode("utf-8") for arg in args]
    ret = " ".join(messages)
    qtlogger.warning(ret)


def error(*args):
    messages = [arg.encode("utf-8") for arg in args]
    ret = " ".join(messages)
    qtlogger.error(ret)


def fatal(*args):
    messages = [arg.encode("utf-8") for arg in args]
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
        if isinstance(fmtMessage, str):
            fmtMessage = fmtMessage.decode("utf-8")

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
formatter = logging.Formatter(
    '%(asctime)s [%(levelname)7s] [%(pathname)s%(lineno)06s] %(message)s')
ch.setFormatter(formatter)
logger = logging.root
logger.propagate = 0
logger.addHandler(ch)
