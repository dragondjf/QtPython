#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import sys
import traceback
from log import logger
from modbusDB import rtuMaster
import threading

logger.info(sys.path)
logger.info(u"======1dsdssddddd试试手sddssdsdsdsdsdsd=======")


def fuckit(func):
    def f(*args, **kwargs):
        try:
            ret = func(*args, **kwargs)
            return ret
        except Exception, e:
            logger.error(traceback.format_exc())
            return None
    return f

@fuckit
def test_base(a1, a2, a3):
    logger.info(a1)
    logger.info(a2)
    logger.info(a3)
    rtuMaster.testPacket("DigtalOutputPacket")
    return 10


def returnJson(args):
    logger.warning(args)
    obj = {"a1": "a1", "a2": "a2", "a3": "a3", "a4": "a4"}
    ret = json.dumps(obj)
    logger.error("dssssssssss111111111111111111111111111ssssss")
    return ret


def testClass(s):
    logger.info(dir(__package__))
    try:
        import QtCore
        logger.info(dir(QtCore))
    except Exception, e:
        logger.info(e)

    try:
        import QtCore2
        logger.info(dir(QtCore2))
    except Exception, e:
        logger.info(e)

    try:
        from QtCore import signalManager, signalManager1, pyobjInstance, PyObjectController
        # signalManager.requestObjChanged.connect(testSignal)
        pyobj1 = PyObjectController(10, None)
        logger.info(dir(signalManager))
        logger.info(dir(pyobjInstance))
        
        logger.info(pyobj1)
        logger.info(pyobjInstance)

        logger.info(pyobjInstance.getInstance(5).getObj())
        logger.info(pyobjInstance.getInstance(6).getObj())


        logger.info(pyobjInstance.getObj())
        logger.info(s.getObj())
        signalManager.requestObjChanged(11150000)



        logger.info(s)
        logger.info(pyobjInstance)

        logger.info(pyobjInstance.getObj())
        logger.info(s.getObj())


    except Exception, e:
        logger.info(e)

    return 

def testSignal(a):
    logger.info(a)
