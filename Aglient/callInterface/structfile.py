# -*- coding: GB18030 -*-
from ctypes import *
import sys
import os

class AntIDSet(Structure): # pylint: disable=R0903
    '''
    libdid.so Ant struct definition
    '''
    _fields_ = [("antID", c_uint16 * 4)]


class RoReport(Structure): # pylint: disable=R0903
    '''
    libdid.so RoReport struct definition
    '''
    _fields_=[("tagid", c_char_p), #标签清点结果
              ("opbuf", c_char_p), #标签操作结果
              ("res",   c_int), #操作返回值
              ("restype", c_uint32), #操作结果类型
              ("opid",  c_uint16), #操作id
              ("antid", c_uint16), #天线id
              ("protocol", c_ubyte), #协议
              ("pad",   c_ubyte * 3),
              ("time",  c_ulonglong)] #生成时间

class EventReport(Structure): # pylint: disable=R0903
    '''
    libdid.so EventReport struct definition
    '''
    _fields_ = [("type",      c_uint32),
                ("time",      c_ulonglong),
                ("specindex", c_uint32)]

class ReportRes(Structure): # pylint: disable=R0903
    '''
    libdid.so ReportRes struct definition
    '''
    _fields_ = [("handle",  c_int),
                ("type",    c_uint32), #报告类型
                ("report",  c_void_p)]

class HFRes(Structure): # pylint: disable=R0903
    '''
    libdid.so HFRes struct definition
    '''
    _fields_ = [("resBuf", c_ubyte * 256),
                ("resLen", c_ubyte),
                ("pad",    c_char * 3)]


class ReadParam(Structure): # pylint: disable=R0903
    '''
    libdid.so ReadParam struct definition
    '''
    _fields_ = [("password", c_uint32),
                ("membank",  c_uint32),
                ("pointer",  c_uint32),
                ("length",   c_uint32)]

class WriteParam(Structure): # pylint: disable=R0903
    '''
    libdid.so WriteParam struct definition
    '''
    _fields_ = [("password", c_uint32),
                ("membank",  c_uint32),
                ("pointer",  c_uint32),
                ("length",   c_uint32),
                ("writedata",c_char_p)]

class LockParam(Structure): # pylint: disable=R0903
    '''
    libdid.so LockParam struct definition
    '''
    _fields_ = [("password", c_uint32),
                ("lockarea",  c_uint32),
                ("locktype",  c_uint32)]

class BlockEraseParam(Structure):
    _fields_ = [("password", c_uint32),
                ("membank",  c_uint32),
                ("pointer",  c_uint32),
                ("length",   c_uint32)]

class KillParam(Structure):
    _fields_ = [("password", c_uint32)]

class OpParamElement(Structure): # pylint: disable=R0903
    '''
    libdid.so OpParamElement struct definition
    '''
    _fields_ = [("optype",   c_uint32), #操作类型
                ("op",       c_void_p), #读或者写操作指针,读或者写结构体的元素的内存地址
                ("opid",     c_uint16), #操作 id
                ("protocol", c_uint8), #协议
                ("pad",      c_uint8)]

#一个OP操作
class  OpParam(Structure): # pylint: disable=R0903
    '''
    libdid.so OpParam struct definition
    '''
    _fields_ = [("opparamelement",  OpParamElement),
                ("targetId", c_char_p), #匹配标签该数据为标签的唯一标识
                ("targetmask", c_char_p)] #匹配掩码


#操作列表参数
class OpParamList(Structure): # pylint: disable=R0903
    '''
    libdid.so OpParamList struct definition
    '''
    _fields_ = [("element",  OpParamElement * 32), #操作参数
                ("opcount",  c_uint32), #OP实际数量
                ("targetId", c_char_p), #匹配标签
                ("targetmask", c_char_p)] #匹配掩码
