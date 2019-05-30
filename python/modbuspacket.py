#!/usr/bin/env python
# -*- coding: utf_8 -*-

from __future__ import absolute_import 

import copy
import itertools
import socket
import struct
import array

import sys

if sys.version_info < (3,):
    compat_ord = ord
else:
    def compat_ord(char):
        return char

try:
    from itertools import izip
    compat_izip = izip
except ImportError:
    compat_izip = zip

try:
    from cStringIO import StringIO
except ImportError:
    from io import StringIO

try: 
    from BytesIO import BytesIO
except ImportError: 
    from io import BytesIO
        
if sys.version_info < (3,):
    def iteritems(d, **kw):
        return d.iteritems(**kw)
else:
    def iteritems(d, **kw):
        return iter(d.items(**kw))

from collections import OrderedDict
try:
    from ..log import logger
except Exception, e:
    pass


class Error(Exception):
    pass


class UnpackError(Error):
    pass


class NeedData(UnpackError):
    pass


class PackError(Error):
    pass


class _MetaPacket(type):
    def __new__(cls, clsname, clsbases, clsdict):
        t = type.__new__(cls, clsname, clsbases, clsdict)
        st = getattr(t, '__hdr__', None)
        if st is not None:
            # XXX - __slots__ only created in __new__()
            clsdict['__slots__'] = [x[0] for x in st] + ['data']
            t = type.__new__(cls, clsname, clsbases, clsdict)
            t.__hdr_fields__ = [x[0] for x in st]
            t.__hdr_registerAddresss__ = OrderedDict(compat_izip(
                t.__hdr_fields__, [x[1] for x in st]))
            t.__hdr_fmt__ = getattr(t, '__byte_order__', '>') + ''.join([x[2] for x in st])
            t.__hdr_field_fmts__ = OrderedDict(compat_izip(
                t.__hdr_fields__, [x[2] for x in st]))
            t.__hdr_len__ = struct.calcsize(t.__hdr_fmt__)
            t.__hdr_defaults__ = OrderedDict(compat_izip(
                t.__hdr_fields__, [x[3] for x in st]))
            t.__hdr_units__ = OrderedDict(compat_izip(
                t.__hdr_fields__, [x[4] for x in st]))
        return t


class Packet(_MetaPacket("Temp", (object,), {})):
    """Base packet class, with metaclass magic to generate members from self.__hdr__.
    Attributes:
        __hdr__: Packet header should be defined as a list of 
                 (name, structfmt, default) tuples.
        __byte_order__: Byte order, can be set to override the default ('>')
    Example:
    >>> class Foo(Packet):
    ...   __hdr__ = (('foo', 'I', 1), ('bar', 'H', 2), ('baz', '4s', 'quux'))
    ...
    >>> foo = Foo(bar=3)
    >>> foo
    Foo(bar=3)
    >>> str(foo)
    '\x00\x00\x00\x01\x00\x03quux'
    >>> foo.bar
    3
    >>> foo.baz
    'quux'
    >>> foo.foo = 7
    >>> foo.baz = 'whee'
    >>> foo
    Foo(baz='whee', foo=7, bar=3)
    >>> Foo('hello, world!')
    Foo(baz=' wor', foo=1751477356L, bar=28460, data='ld!')
    """

    def __init__(self, *args, **kwargs):
        """Packet constructor with ([buf], [field=val,...]) prototype.
        Arguments:
        buf -- optional packet buffer to unpack
        Optional keyword arguments correspond to members to set
        (matching fields in self.__hdr__, or 'data').
        """
        self.data = b''
        if args:
            try:
                self.unpack(args[0])
            except struct.error:
                if len(args[0]) < self.__hdr_len__:
                    raise NeedData
                raise UnpackError('invalid %s: %r' %
                                  (self.__class__.__name__, args[0]))
        else:
            for k in self.__hdr_fields__:
                setattr(self, k, copy.copy(self.__hdr_defaults__[k]))
            for k, v in iteritems(kwargs):
                setattr(self, k, v)

    def __len__(self):
        return self.__hdr_len__ + len(self.data)

    def __getitem__(self, k):
        try:
            return getattr(self, k)
        except AttributeError:
            raise KeyError

    def __repr__(self):
        # Collect and display protocol fields in order:
        # 1. public fields defined in __hdr__, unless their value is default
        # 2. properties derived from _private fields defined in __hdr__
        # 3. dynamically added fields from self.__dict__, unless they are _private
        # 4. self.data when it's present

        l = []
        # maintain order of fields as defined in __hdr__
        for field_name, _, _ in getattr(self, '__hdr__', []):
            field_value = getattr(self, field_name)
            if field_value != self.__hdr_defaults__[field_name]:
                if field_name[0] != '_':
                    l.append('%s=%r' % (field_name, field_value))  # (1)
                else:
                    # interpret _private fields as name of properties joined by underscores
                    for prop_name in field_name.split('_'):        # (2)
                        if isinstance(getattr(self.__class__, prop_name, None), property):
                            l.append('%s=%r' % (prop_name, getattr(self, prop_name)))
        # (3)
        l.extend(
            ['%s=%r' % (attr_name, attr_value)
             for attr_name, attr_value in iteritems(self.__dict__)
             if attr_name[0] != '_'                   # exclude _private attributes
             and attr_name != self.data.__class__.__name__.lower()])  # exclude fields like ip.udp
        # (4)
        if self.data:
            l.append('data=%r' % self.data)
        return '%s(%s)' % (self.__class__.__name__, ', '.join(l))

    def __str__(self):
        return str(self.__bytes__())
    
    def __bytes__(self):
        return self.pack_hdr() + bytes(self.data)

    def pack_hdr(self):
        """Return packed header string."""
        try:
            return struct.pack(self.__hdr_fmt__,
                               *[getattr(self, k) for k in self.__hdr_fields__])
        except struct.error:
            vals = []
            for k in self.__hdr_fields__:
                v = getattr(self, k)
                if isinstance(v, tuple):
                    vals.extend(v)
                else:
                    vals.append(v)
            try:
                print self.__hdr_fmt__
                print vals
                return struct.pack(self.__hdr_fmt__, *vals)
            except struct.error as e:
                raise PackError(str(e))

    def pack(self):
        """Return packed header + self.data string."""
        return bytes(self)

    def unpack(self, buf):
        """Unpack packet header fields from buf, and set self.data."""
        values = struct.unpack(self.__hdr_fmt__, buf[:self.__hdr_len__])
        for k, v in compat_izip(self.__hdr_fields__, values):
            setattr(self, k, v)
        self.data = buf[self.__hdr_len__:]




class NoFieldException(Exception):
    pass

class NoSingleRegisterFieldException(Exception):
    pass


class BasePacket(Packet):

    __byte_order__ = ">"

    def __repr__(self):

        l = ["\n"]
        for k in self.__hdr_fields__:
            l.append("%s: %s\n" % (k, self[k])) 

        return "%s(%s)" % (self.__class__.__name__, " ".join(l))
    @classmethod
    def fields(cls):
        return cls.__hdr_fields__

    @classmethod
    def units(cls):
        return cls.__hdr_units__

    @classmethod
    def registerAddress(cls):
        return cls.__hdr_registerAddresss__

    @classmethod
    def format(cls):
        return cls.__hdr_fmt__

    @classmethod
    def setFormat(cls, format):
        cls.__hdr_fmt__ = format

    @classmethod
    def byteOrder(cls):
        return getattr(cls, '__byte_order__', '>')

    @classmethod
    def defaults(cls):
        return getattr(cls, "__hdr_defaults__")

    @classmethod
    def fieldRegisterAddress(cls, field):
        return cls.__hdr_registerAddresss__.get(field, None)

    @classmethod
    def fieldFormat(cls, field):
        return cls.byteOrder() + cls.__hdr_field_fmts__.get(field, None)

    @classmethod
    def fieldUnit(cls, field):
        return cls.__hdr_units__.get(field, 1)

    @classmethod
    def length(cls):
        return cls.__hdr_len__

    @classmethod
    def startRegisterAddress(cls):
        st = getattr(cls, '__hdr__', None)
        if st is not None:
            return st[0][1]
        return None

    @classmethod
    def endRegisterAddress(cls):
        st = getattr(cls, '__hdr__', None)
        if st is not None:
            return st[len(st) - 1][1]
        return None

    @classmethod
    def registerCountByFormat(cls, format):
        size = struct.calcsize(format)
        if size % 2 != 0:
            registerCount = size / 2  + 1
        else:
            registerCount = size / 2
        return registerCount

    def unpackBufFields(self, buf, startField, endField):
        """Unpack packet header fields from buf, and set self.data."""
        fields, fmt = self.fmtFields(startField, endField)
        logger.info(fmt)
        logger.info(len(buf))
        values = struct.unpack(fmt, buf[:struct.calcsize(fmt)])
        for k, v in compat_izip(fields, values):
            setattr(self, k, v)

    def fmtFields(self, startField, endField):
        fields = self.getFields(startField, endField)
        fmt = self.byteOrder()
        for field in fields:
            fmt += self.__hdr_field_fmts__.get(field, None)
        return fields, fmt

    def values(self):
        """
        return: [2, 1, 'aaaabbbb', 'ccccdddd', 'eeeeffff', '11111112222222', '33333334444444', '55555556666666', 9999, 1, 8888, 12, 11, 2]
        """
        return [getattr(self, k) for k in self.__hdr_fields__]

    def updateByValues(self, args):
        """
        input args: [2, 1, 'aaaabbbb', 'ccccdddd', 'eeeeffff', '11111112222222', '33333334444444', '55555556666666', 9999, 1, 8888, 12, 11, 2]
        """
        for k, v in compat_izip(self.__hdr_fields__, args):
            setattr(self, k, v)

    def update(self, **kwargs):
        """
        input kwargs: {
            glider_id: 15
            workmode: 1
            bd_card_number: aaaabbbb
            remote_bd_card_number: ccccdddd
            backup_remote_bd_card_number: eeeeffff
            iridium_card_number: 11111112222222
            remote_iridium_card_number: 33333334444444
            backup_remote_iridium_card_number: 55555556666666
            local_port: 9999
            local_ip: 1
            remote_port: 8888
            remote_ip: 12
            process_state: 11
            debug_mode: 2
        }
        """
        for k in self.__hdr_fields__:
            if kwargs.has_key(k):
                setattr(self, k, kwargs.get(k))

    def getFields(self, startField=None, endField=None):
        fields = self.fields()

        if startField is None and endField is None:
            return fields
        elif startField is None and endField is not None:
            endIndex = fields.index(endField)
            return fields[:(endIndex + 1)]
        elif startField is not None and endField is None:
            startIndex = fields.index(startField)
            return fields[startIndex:]
        elif startField is not None and endField is  not None:
            startIndex = fields.index(startField)
            endIndex = fields.index(endField)
            return fields[startIndex:(endIndex+1)]

    def read_register(self, field):
        startAddress = self.fieldRegisterAddress(field)
        format = self.fieldFormat(field)

        return (startAddress, self.registerCountByFormat(format), "", format)

    def read_registers(self, startField=None, endField=None):
        if startField is None and endField is None:
            startAddress = self.startRegisterAddress()
            endAddress = self.endRegisterAddress()
        elif startField is None and endField:
            startAddress = self.startRegisterAddress()
            endAddress = self.fieldRegisterAddress(startField)
        elif startField and endField is None:
            startAddress = self.fieldRegisterAddress(startField)
            endAddress = self.endRegisterAddress()
        else:
            startAddress = self.fieldRegisterAddress(startField)
            endAddress = self.fieldRegisterAddress(endField)

        format = self.byteOrder()
        for item in getattr(self, "__hdr__"):
            if item[1] >= startAddress and item[1] <= endAddress:
                format  += item[2]

        registerCount = struct.calcsize(format) / 2

        return (startAddress, self.registerCountByFormat(format), "", format)

    def write_register(self, field, value):
        if field in self.fields():
            startAddress = self.fieldRegisterAddress(field)
            format = self.fieldFormat(field)

            if struct.calcsize(format) / 2 == 1:
                return (startAddress, 0, value)
            else:
                raise NoSingleRegisterFieldException("Field (%s) is not single register, it takes up %s registers " % (field, struct.calcsize(format) / 2))
        raise NoFieldException("No field %s in this packet" % field)

    def write_registers(self, startField=None, endField=None, **kwargs):
        if startField is None and endField is None:
            startAddress = self.startRegisterAddress()
            endAddress = self.endRegisterAddress()
            defaults = self.defaults()
            defaults.update(**kwargs)
            kwargs = defaults
        elif startField is None and endField:
            startAddress = self.startRegisterAddress()
            endAddress = self.fieldRegisterAddress(startField)
        elif startField and endField is None:
            startAddress = self.fieldRegisterAddress(startField)
            endAddress = self.endRegisterAddress()
        else:
            startAddress = self.fieldRegisterAddress(startField)
            endAddress = self.fieldRegisterAddress(endField)

        format = self.byteOrder()
        output = []
        for item in getattr(self, "__hdr__"):
            if item[1] >= startAddress and item[1] <= endAddress:
                format  += item[2]
                output.append(kwargs.get(item[0]))

        return (startAddress, self.registerCountByFormat(format), output, format)
