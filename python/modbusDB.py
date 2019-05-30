#!/usr/bin/env python
# -*- coding: utf_8 -*-

from modbuspacket import *
from modbus_tk import modbus_rtu, hooks
import modbus_tk.defines as cst
import os
import traceback
import time
import serial
from log import logger


class DigtalOutputPacket(BasePacket):

    __hdr__ = (
        ("O_Alarm", 0 , "b", 1, 1),
        ("O_Warm", 1 , "b", 0, 1),
        ("O_S2", 2 , "b", 1, 1),
        ("O_S1", 3 , "b", 0, 1),
        ("O_Nopass", 4 , "b", 0, 1),
        ("O_Nok", 5 , "b", 0, 1),
        ("O_Ok", 6 , "b", 0, 1),
        ("O_Ready", 7 , "b", 0, 1),
        ("O_Reservoed", 8 , "b", 0, 1),
        ("O_Sequence_end", 9 , "b", 0, 1),
        ("O_Eo_01", 10 , "b", 0, 1),
        ("O_Unknown", 11 , "b", 0, 1),
        ("O_MP_3", 12, "b", 0, 1),
        ("O_MP_2", 13 , "b", 0, 1),
        ("O_MP_1", 14 , "b", 0, 1),
        ("O_MP_0", 15 , "b", 0, 1),
        ("O_Reservoed_0", 16 , "b", 0, 1),
        ("o_reservoed_1", 17 , "b", 0, 1),
        ("o_reservoed_2", 18 , "b", 0, 1),
        ("o_reservoed_3", 19 , "b", 0, 1),
        ("o_reservoed_4", 20 , "b", 0, 1),
        ("O_MP_6", 21 , "b", 0, 1),
        ("O_MP_5", 22 , "b", 0, 1),
        ("O_MP_4", 23 , "b", 0, 1)
    )


class RtuMaster(modbus_rtu.RtuMaster):

    _instance = None

    def __init__(self, serial, interchar_multiplier=1.5, interframe_multiplier=3.5, t0=None):
        super(RtuMaster, self).__init__(serial, interchar_multiplier, interframe_multiplier, t0)
        self.retryTimes = 1
        self.slave_id = 1

    @classmethod
    def instance(cls, port):
        if cls._instance is None:
            try:
                s = serial.Serial(port=port, baudrate=115200, bytesize=8, parity='N', stopbits=1, xonxoff=0)
                cls._instance = RtuMaster(s)
                cls._instance.set_timeout(1.0)
                cls._instance.set_verbose(True)
            except Exception, e:
                logger.error(traceback.format_exc())

        return cls._instance

    def execute(self, slave, function_code, starting_address, quantity_of_x, output_value=0, data_format="", expected_length=-1):
        logger.info("slave_id.:%d, function_code: %d , starting_address: %d" % (slave, function_code, starting_address))
        logger.info("No.:%s send" % (4-self.retryTimes))
        try:
            ret = super(RtuMaster, self).execute(slave, function_code, starting_address, quantity_of_x, output_value, data_format, expected_length)
            logger.info(ret)
            return ret
        except Exception, e:
            logger.error(repr(e))
            self.retryTimes -= 1
            if self.retryTimes != 0:
                self.execute(slave, function_code, starting_address, quantity_of_x, output_value, data_format, expected_length)
            else:
                self.retryTimes = 1
            return None

    def testPacket(self, name):
        if name in globals():
            packet = globals()[name]()
            logger.info("%s:%s", name, packet.defaults())
            logger.info("%s:%s", name, packet.defaults().values())
            logger.info(packet.write_registers())
            ret = self.execute(self.slave_id, cst.WRITE_MULTIPLE_REGISTERS, *packet.write_registers())
            logger.info("write_registers: %s", ret)
            ret = self.execute(self.slave_id, cst.READ_HOLDING_REGISTERS, *packet.read_registers())
            logger.info("read_registers: %s", ret)
        else:
            logger.info("no packet: %s", name)

    def testAllPacket(self):
        failPackets = set()
        for k, v in globals().items():
            if k.endswith("Packet"):
                if issubclass(v, BasePacket) and v not in (BasePacket, FileHeaderPacket, FileContentPacket):
                    packet = v()
                    logger.info("%s: %s" % (k, packet.defaults()))
                    logger.info(packet.write_registers())
                    ret = self.execute(self.slave_id, cst.WRITE_MULTIPLE_REGISTERS, *packet.write_registers())
                    logger.info("write_registers: %s", ret)
                    if ret is None:
                        failPackets.add(k)
                    logger.info(packet.read_registers())
                    ret = self.execute(self.slave_id, cst.READ_HOLDING_REGISTERS, *packet.read_registers())
                    logger.info("read_registers: %s", ret)
                    if ret is None:
                        failPackets.add(k)
        logger.info("=========Failed packets: %s==============", failPackets)



rtuMaster = RtuMaster.instance('/dev/pts/6s')


if __name__ == '__main__':
    
    import serial
    import logging

    import modbus_tk
    import modbus_tk.defines as cst
    from modbus_tk import modbus_rtu, hooks
    from modbus_tk import modbus
    import logging
    
    formatter = logging.Formatter(
    '%(asctime)s %(levelname)8s [%(filename)s%(lineno)06s] %(message)s')

    
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    #log formatter
    formatter = logging.Formatter(
        '%(asctime)s %(levelname)8s [%(filename)s%(lineno)06s] %(message)s')
    ch.setFormatter(formatter)

    logger = logging.root
    logger.setLevel(logging.DEBUG)
    logger.addHandler(ch)


    # PORT = '/dev/ttyUSB0'
    PORT = '/dev/pts/2'


    master = RtuMaster(
            serial.Serial(port=PORT, baudrate=115200, bytesize=8, parity='N', stopbits=1, xonxoff=0)
        )
    master.set_timeout(1.0)
    master.set_verbose(True)

    # centroid = CentroidPacket()

    # logger.info(master.execute(1, cst.WRITE_SINGLE_REGISTER, *centroid.write_register("control_code", 94)))

    # logger.info(master.execute(1, cst.READ_HOLDING_REGISTERS, *centroid.read_register("control_code")))

    # master.deleteFile("default.py")
    # master.writeFile("/home/djf/workspace/glider/server/gliderApi/views/fileapi.py")
    # content = master.readFile("default.py")
    # logger.info(content)

    # master.testAllPacket()
    master.testPacket("DigtalOutputPacket")


    # logger.info(glider.write_registers())

    # logger.info(master.execute(1, cst.WRITE_MULTIPLE_REGISTERS, *glider.write_registers()))

    # #读取单个寄存器
    # logger.info(master.execute(1, cst.READ_HOLDING_REGISTERS, *glider.read_register("glider_id")))

    # # # #根据起始和结束field读取多个连续的寄存器
    # logger.info(master.execute(1, cst.READ_HOLDING_REGISTERS, *glider.read_registers("glider_id", "bd_card_number")))

    # # # #读取整个包
    # logger.info(master.execute(1, cst.READ_HOLDING_REGISTERS, *glider.read_registers()))

    # # # #写单个寄存器
    # logger.info(master.execute(1, cst.WRITE_SINGLE_REGISTER, *glider.write_register("glider_id", 11)))

    # # logger.info(master.execute(1, cst.READ_HOLDING_REGISTERS, *glider.read_register("glider_id")))
    # # # #根据起始和结束的field写多个连续的寄存器
    # logger.info(master.execute(1, cst.WRITE_MULTIPLE_REGISTERS, *glider.write_registers("bd_card_number",  "local_port", **a)))

    # # #写整个包
    # logger.info(master.execute(1, cst.WRITE_MULTIPLE_REGISTERS, *glider.write_registers()))
    # logger.info(master.execute(1, cst.READ_HOLDING_REGISTERS, *glider.read_registers()))


    # settings = SettingsPacket()
    # logger.info(settings.write_registers())
    # logger.info(master.execute(1, cst.WRITE_MULTIPLE_REGISTERS, *settings.write_registers()))


    # master.writeFile("/home/djf/workspace/glider/server/gliderApi/model/default.py")

    # content = master.readFileByName("default.py")

    # logger.info(content)
