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
    _fields_=[("tagid", c_char_p), #��ǩ�����
              ("opbuf", c_char_p), #��ǩ�������
              ("res",   c_int), #��������ֵ
              ("restype", c_uint32), #�����������
              ("opid",  c_uint16), #����id
              ("antid", c_uint16), #����id
              ("protocol", c_ubyte), #Э��
              ("pad",   c_ubyte * 3),
              ("time",  c_ulonglong)] #����ʱ��

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
                ("type",    c_uint32), #��������
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
    _fields_ = [("optype",   c_uint32), #��������
                ("op",       c_void_p), #������д����ָ��,������д�ṹ���Ԫ�ص��ڴ��ַ
                ("opid",     c_uint16), #���� id
                ("protocol", c_uint8), #Э��
                ("pad",      c_uint8)]

#һ��OP����
class  OpParam(Structure): # pylint: disable=R0903
    '''
    libdid.so OpParam struct definition
    '''
    _fields_ = [("opparamelement",  OpParamElement),
                ("targetId", c_char_p), #ƥ���ǩ������Ϊ��ǩ��Ψһ��ʶ
                ("targetmask", c_char_p)] #ƥ������


#�����б����
class OpParamList(Structure): # pylint: disable=R0903
    '''
    libdid.so OpParamList struct definition
    '''
    _fields_ = [("element",  OpParamElement * 32), #��������
                ("opcount",  c_uint32), #OPʵ������
                ("targetId", c_char_p), #ƥ���ǩ
                ("targetmask", c_char_p)] #ƥ������
