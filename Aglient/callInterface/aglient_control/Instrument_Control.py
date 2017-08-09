# -*- coding: GB18030 -*-
import visa,time
from pyvisa.resources.usb import USBInstrument
from pyvisa.constants import  *
from CONSTANTS import *

class Agilent(object):

    def OpenInstrument(self):
        rm = visa.ResourceManager()
        self.my_instrument = rm.open_resource('TCPIP0::192.168.1.77::inst0::INSTR')
        print self.my_instrument.query('*IDN?')  #get device info
        return self.my_instrument

    def SA_Reset(self):
        self.my_instrument.write('*RST;*WAI;') # reset device
        self.my_instrument.write('*CLS;*WAI;') # clear device

    # set device mode
    def SA_SetMode(self,nMode):
        if nMode==1:
            self.my_instrument.write(':INST:SEL SA')
        elif nMode==2:
            self.my_instrument.write(':INST:SEL VSA89601')
        else:
            print "set device mode error!"

    #���ù��ʲ���
    def SA_SetOffset(self,fOffset):
        '''
        :param fOffset:ΪƵ�׷����Ƕ������źŵĹ��ʲ�������λ��dbm
        :return:None
        '''
        offset = ':DISP:WIND:TRAC:Y:RLEV:OFFS ' + str(fOffset)
        self.my_instrument.write(offset)

    def SA_SetRFAtten(self):
        #�ڲ�˥������Ϊ�Զ�
        self.my_instrument.write(':SENS:POW:ATT 10')

    def SA_SetDetector(self,nType):
        '''
        :param nType: Type��ʾ�첨��ʽ��1��ʾ��ֵ�첨������ֵ�첨����2��ʾ��Чֵ�첨��RMS����
        :return:None
        '''
        if nType==1:
            self.my_instrument.write(':SENS:DET:AUTO OFF')
            self.my_instrument.write(':SENS:DET POS')
        elif nType==2:
            self.my_instrument.write(':SENS:DET:AUTO OFF')
            self.my_instrument.write(':SENS:DET AVE')
        else:
            print u"�첨��ʽ����"

    #��ʼ������
    def SAInit(self):
        self.SA_Reset()
        self.SA_SetMode(1)
        self.SA_SetOffset(fOffset)
        #self.SA_SetRFAtten()
        self.SA_SetDetector(1)

    #����Ƶ�ʷ�Χ�ͷ����ź�ƽ̹�Ȳ���
    #ѡ��Ƶ���ǵĲ���ģʽΪ����ɨƵģʽ
    def SA_SetMeas(self,nMode):
        '''
        :param nMode:��ʾƵ�׷����ǵ�ģʽ��1��ʾɨƵģʽ��2��ʾOBWģʽ��3��ʾACPģʽ
        :return:None
        '''
        if nMode==1:
            self.my_instrument.write('CONF:SAN:NDEF')
        elif nMode==2:
            self.my_instrument.write('CONF:OBW:NDEF')
        elif nMode==3:
            self.my_instrument.write('CONF:ACP:NDEF')

    #����ACPR��������
    def SA_SetACPR(self):
        #�ر�ƽ��ֵ
        self.my_instrument.write(':SENS:ACP:AVER:STAT OFF')
        time.sleep(0.5)
        self.SA_SetTraceMode(1)
        time.sleep(0.5)
        #ɨƵʱ���ɨƵ����
        self.my_instrument.write(':SENS:ACP:SWE:TIME 500ms')
        time.sleep(0.5)
        self.my_instrument.write(':SENS:OBW:SWE:POIN 1001')
        time.sleep(0.5)
        #���ŵ����ڽ��ŵ�
        self.my_instrument.write(':SENS:ACP:BAND:INT 250Khz')
        time.sleep(0.5)
        self.my_instrument.write(':SENS:ACP:OFFS:LIST:STAT ON,ON,OFF,OFF,OFF,OFF')
        time.sleep(0.5)
        self.my_instrument.write(':SENS:ACP:OFFS:LIST:BAND 250KHz,250KHz,0,0,0,0')
        time.sleep(0.5)
        #250KHz,250KHz,0,0,0,0
        self.my_instrument.write(':SENS:ACP:OFFS:LIST:FREQ 250KHz,500KHz,0,0,0,0')
        time.sleep(1)
        #250KHz,500KHz,0,0,0,0
        #ǰ��������ɺ����ִ������ָ��
        #����ɨƵ����Ͳ�������
        self.my_instrument.write(':SENS:ACP:FREQ:SPAN 1.5MHz')
        time.sleep(0.5)
        self.my_instrument.write(':SENS:ACP:BAND 10KHz')
        time.sleep(0.5)
        self.SA_SetRFAtten()
        time.sleep(0.5)
        self.SA_SetCenterFrequency(ACPR_fCenterFrequency) #����ACPR����Ƶ�㣬һ��Ϊ10����ӦֵΪ842.625
        self.SA_SetOffset(fOffset)


    #��������Ƶ��
    def SA_SetCenterFrequency(self,fCenterFrequency):
        '''
        :param fCenterFrequency:ΪƵ�׵�����Ƶ�ʣ���λ��MHz
        :return:None
        '''
        CenterFrequency = ':SENS:FREQ:CENT ' + str(fCenterFrequency) + 'MHz'
        self.my_instrument.write(CenterFrequency)

    #����Ƶ�״���
    def SA_SetSpan(self,fSpan):
        '''
        :param fSpan:ΪƵ�׵Ĵ�����λ��MHz
        :return:None
        '''
        span = ':SENS:FREQ:SPAN ' + str(fSpan) + 'MHz'
        self.my_instrument.write(span)

    #���÷ֱ��ʴ���
    def SA_SetRBW(self,fRBW):
        '''
        :param fRBW:ΪƵ�׷����ǵķֱ��ʴ�������������λ��KHz��
                ��Сֵһ����1KHz������ֵС�ڵ���0��ʾ��������Ϊ�Զ�
        :return:
        '''
        if fRBW<=0:
            self.my_instrument.write('BAND:AUTO ON')
        else:
            rbw = 'BAND ' + str(fRBW) + 'KHz'
            self.my_instrument.write('BAND:AUTO OFF')
            self.my_instrument.write(rbw)

    #����Ƶ����Ϊ���ֵ����ģʽ
    def SA_SetTraceMode(self,nMode):
        '''
        :param nMode: ��ʾTrace��ʽ��0��ʾClearWrite��1��ʾ���ֵ����
        :return:None
        '''
        if nMode==0:
            self.my_instrument.write(':TRAC:MODE WRIT')
        elif nMode==1:
            self.my_instrument.write(':TRAC:MODE MAXH')


    #����Ƶ����Ϊ����ɨƵģʽ
    def SA_SetCont(self,nMode):
        '''
        :param nMode:��ʾɨƵ��ʽ��0��ʾ��ɨ��1��ʾ����ɨ
        :return:None
        '''
        if nMode==0:
            self.my_instrument.write('INIT:CONT OFF')
        elif nMode==1:
            self.my_instrument.write('INIT:CONT ON')
            self.my_instrument.write('INIT;*WAI')

    #����Ƶ������
    def SA_SetStart(self,fStart):
        '''
        :param fStart:ΪƵ����Ƶ�����㣬��λ��MHz
        :return:None
        '''
        start = ':SENS:FREQ:STAR ' + fStart +'MHz'
        self.my_instrument.write(start)

    #����Ƶ����յ�
    def SA_SetStop(self,fStop):
        '''
        :param fStop:ΪƵ����Ƶ����յ㣬��λ��MHz
        :return:
        '''
        stop = ':SENS:FREQ:STOP ' + fStop +'MHz'
        self.my_instrument.write(stop)

    #���ù��ʲο�ֵ
    def SA_SetReferenceLevel(self,fRefer):
        '''
        :param fRefer: Ϊ���ʲο�����ֵ����λ��dbm
        :return:
        '''
        refer = ':DISP:WIND:TRAC:Y:RLEV ' + str(fRefer)
        self.my_instrument.write(refer)

    #������Ƶ����
    def SA_SetVBW(self,fVBW):
        '''
        :param fVBW:ΪƵ�׷����ǵ���Ƶ������λ��KHz��
                ����ֵС�ڵ���0��ʾ��Ƶ����Ϊ�Զ�
        :return:
        '''
        if fVBW<=0:
            self.my_instrument.write('BAND:VID:AUTO ON')
        else:
            vbw = 'BAND:VID ' + fVBW + 'KHz'
            self.my_instrument.write('BAND:VID:AUTO OFF')
            self.my_instrument.write(vbw)

    #����OBW��������
    def SA_SetOBW(self,nSpan,nRBW):
        '''
        :param nSpan: ��ʾ����OBWʱƵ��Ŀ��
        :param nRBW:��ʾ����OBWʱʹ�õĲ���������λKHz
        :return:None
        '''
        #�����ֵ����
        self.my_instrument.write(':OBW:MAXH ON')
        #�ر�ƽ��ֵ
        self.my_instrument.write(':SENS:OBW:AVER:STAT OFF')
        #ɨƵʱ���ɨƵ����
        self.my_instrument.write(':SENS:ACP:SWE:TIME 500ms')
        self.my_instrument.write(':SENS:OBW:SWE:POIN 1001')
        #����ɨƵ���� :SENS:OBW:FREQ:SPAN 2MHz
        span = ':SENS:OBW:FREQ:SPAN '+ str(nSpan) + 'MHz'
        self.my_instrument.write(span)
        #�����ٷֱ�
        self.my_instrument.write(':OBW:PERC 99')
        #����OBW�ֱ��ʴ��� :SENS:OBW:BAND 10KHz
        rbw = ':SENS:OBW:BAND ' +  str(nRBW) + 'KHz'
        self.my_instrument.write(rbw)

    #��ȡƵ����Mark���Ƶ��ֵ�͹���ֵ
    #def SA_GetMark(fFreq, fAmpt):
        '''
        :param fFreq: fFreq��Ƶ���з�ֵ���Ƶ�ʣ���λ��MHz
        :param fAmpt: fAmpt��Ƶ���з�ֵ��Ĺ���ֵ����λ��dbm
        :return:
        '''

        #self.my_instrument.query('CALC:MARK:X?;*WAI')
        #self.my_instrument.query('CALC:MARK:Y?;*WAI')

    #��õ�ǰƵ�������з�ֵ���Ƶ�ʺ͹���
    def SA_PeakSearch(self):
        self.my_instrument.write('CALC:MARK:PEAK:EXC:STAT ON')
        time.sleep(0.5)
        self.my_instrument.write('CALC:MARK:PEAK:EXC 6')
        time.sleep(0.5)
        self.my_instrument.write('CALC:MARK:PEAK:THR:STAT OFF')
        time.sleep(0.5)
        self.my_instrument.write('CALC:MARK:STAT ON')
        time.sleep(0.5)
        self.my_instrument.write('CALC:MARK:TRAC 1')
        time.sleep(0.5)
        self.my_instrument.write('CALC:MARK:MAX')
        time.sleep(0.5)
        self.my_instrument.write('CALC:MARK:MAX:LEFT')
        time.sleep(0.5)
        self.my_instrument.write('CALC:MARK:MAX:RIGH')
        time.sleep(0.5)

    def SA_GetMark(self):
        x = self.my_instrument.query('CALC:MARK:X?;*WAI')
        y = self.my_instrument.query('CALC:MARK:Y?;*WAI')
        return x,y

    #��ȡ�ڵ�����й©��ACPR��ֵ
    def SA_GetACPRPower(self):
        return self.my_instrument.query('FETC:ACP?')


    #��ȡռ�ô���OBW
    def SA_GetOBW(self):
        return self.my_instrument.query('FETC:OBW?')