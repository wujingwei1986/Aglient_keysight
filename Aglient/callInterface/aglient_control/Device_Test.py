# -*- coding: GB18030 -*-
import os,time
from Instrument_Control import *
from CONSTANTS import *
from Analyse import *

agilent_client = Agilent()
agilent_client.OpenInstrument()
#获取峰值功率和频率,发射信号频率稳定度和发射功率测试
def testFrqPower(fCenterFrequency,fRefer,fPower,fChannelIndex,curr_col):
    print u"=============频谱仪开始抓取功率为：{0}，频点为：{1}的数据==========".format(fPower,fChannelIndex)
    agilent_client.SA_SetOffset(fOffset)
    agilent_client.SA_SetCenterFrequency(fCenterFrequency)
    agilent_client.SA_SetSpan(0.5) #设置X轴的值
    agilent_client.SA_SetTraceMode(1)
    agilent_client.SA_SetReferenceLevel(fRefer) #设置参考值Y轴
    time.sleep(2)
    agilent_client.SA_PeakSearch()
    x,y = agilent_client.SA_GetMark()
    x = '{:.3f}'.format(float(x)/1000000)
    y = '{:.3f}'.format(float(y))
    num = 5
    while float(y) < 0:
        print u"Peak Search失败，重新取值"
        agilent_client.SA_PeakSearch()
        x,y = agilent_client.SA_GetMark()
        x = '{:.3f}'.format(float(x)/1000000)
        y = '{:.3f}'.format(float(y))
        num = num - 1
        if float(y) > 0 or num == 0:
            break

    write_PowerResult(fPower,"RFID-power.xls",curr_col,y)
    print u"频谱仪测试结果：中心频点值{0}".format(x)
    print u"频谱仪测试结果：功率值{0}".format(y)

#发射频率范围和发射信号平坦度测试
def testFrqSignalFlatness(fCenterFrequency):
    agilent_client.SA_SetMeas(1) #选择频谱仪的测量模式为连续扫频模式
    agilent_client.SA_SetCenterFrequency(fCenterFrequency) #设置中心频点
    agilent_client.SA_SetSpan(0.5)  #设置频谱带宽
    agilent_client.SA_SetRBW(100) #设置分辨率带宽（100KHz）
    agilent_client.SA_SetTraceMode(1) #设置频谱仪为最大值保持模式
    agilent_client.SA_SetCont(1) #设置频谱仪为连续扫频模式
    #获取发射频率范围和发射信号平坦度
    agilent_client.SA_PeakSearch()
    x,y = agilent_client.SA_GetMark()
    print x,y

def analyze_ACPR(data,ModulationType_text,curr_num):
    acpr_result = data.split(",")
    lower_num1 = '{:.3f}'.format(float(acpr_result[4]))
    lower_num2 = '{:.3f}'.format(float(acpr_result[8]))
    upper_num1 = '{:.3f}'.format(float(acpr_result[6]))
    upper_num2 = '{:.3f}'.format(float(acpr_result[10]))
    print u"第一个低邻道的泄漏比:{0}".format(lower_num1)
    print u"第二个低邻道的泄漏比:{0}".format(lower_num2)
    print u"第一个高邻道的泄漏比:{0}".format(upper_num1)
    print u"第二个高邻道的泄漏比:{0}".format(upper_num2)
    write_file(ModulationType_text,"RFID-ACPR.xls",curr_num,lower_num2,lower_num1,upper_num1,upper_num2)

#邻道功率泄漏比
def testACPR(ModulationType_text,curr_num):
    agilent_client.SA_SetMeas(3) #选择频谱仪的测量模式为ACP模式
    #设置ACP测量参数，包括：
    #主信道带宽（250KHz）
    #和信道间距离（250KHz）
    #分辨率带宽（10KHz）
    #默认参数：
    #扫频时间（自动），扫频宽度（1.5 MHz）
    #扫频点数（1001）	SA_SetACPR
    agilent_client.SA_SetACPR()
    acpr = agilent_client.SA_GetACPRPower()
    analyze_ACPR(acpr,ModulationType_text,curr_num)


#占用带宽测试
def testOBW():
    agilent_client.SA_SetMeas(2)  #设置频谱仪的测量模式为OBW模式
    #设置OBW测量参数，包括：
    #分辨率带宽（10KHz）
    #默认参数：
    #扫频时间（自动）扫频点数（1001）
    #扫频宽度（2MHz），和能量比（99%）
    agilent_client.SA_SetOBW(2,10)
    obw = agilent_client.SA_GetOBW()

def resetSA():
    agilent_client.SAInit()


