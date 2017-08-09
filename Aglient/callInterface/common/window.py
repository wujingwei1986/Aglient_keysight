# -*- coding: utf-8 -*-
from ttk_operateTest import ttk_Operate
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import os,sys,string,urllib,time,sys,re,xlrd,xlwt,time
from xlutils.copy import copy
from testwindow import *
#from start_test_Interface import *

QTextCodec.setCodecForTr(QTextCodec.codecForName("utf8"))
class window(QDialog):
    def __init__(self,parent=None):
        super(window,self).__init__(parent)
        self.setWindowTitle(self.tr("无线指标测试工具"))
        self.setWindowIcon(QIcon('head.ico'))

        self.spectrum_url = QLabel(self.tr("频谱仪ip"))
        self.spectrum_url_lineEdit= QLineEdit("192.168.*.*")

        self.file_path_lable = QLabel(self.tr("文件保存路径"))
        self.file_path_lineEdit= QLineEdit(self)
        self.file_broswe = QPushButton()
        self.file_broswe.setText(self.tr("选择路径"))
        self.connect(self.file_broswe,SIGNAL('clicked()'),self.select_path)

        self.dataoutput_lable = QLabel(self.tr("测试数据"))
        self.dataoutput_text = QTextBrowser()

        self.powerPushButton=QPushButton(self.tr("功率测试"))
        self.ACPRPushButton=QPushButton(self.tr("ACPR测试"))

        grid = QGridLayout() #布局
        grid.setSpacing(10)

        grid.addWidget(self.spectrum_url,1,0)
        grid.addWidget(self.spectrum_url_lineEdit,1,1)

        grid.addWidget(self.file_path_lable,2,0)
        grid.addWidget(self.file_path_lineEdit,2,1)
        grid.addWidget(self.file_broswe,2,2)

        grid.addWidget(self.dataoutput_lable,3,0)
        grid.addWidget(self.dataoutput_text,3,1,1,2)

        grid.addWidget(self.powerPushButton,4,0)
        grid.addWidget(self.ACPRPushButton,4,2)

        self.setLayout(grid)
        self.resize(450, 400)
        self.connect(self.powerPushButton,SIGNAL('clicked()'),self.output_testFrequencyPower)
        #self.connect(self.ACPRPushButton,SIGNAL('clicked()'),test_AllParame_ACPR)

    #测试之前创建数据保存文件
    def select_path(self):
        absolute_path = QFileDialog.getSaveFileName(self, 'Open file','.',"excel files (*.xls)")
        if absolute_path:
            cur_path = QDir('.')
            fileabsolute_path = cur_path.absoluteFilePath(absolute_path)
            self.file_path_lineEdit.setText(fileabsolute_path)

    def split_pathFile(self):
        fi = QFileInfo(self.file_path_lineEdit.text())
        self.filePath = str(fi.filePath())
        self.fileNmae = str(fi.fileName())
        return self.filePath,self.fileNmae

    def check_filePath(self):
        if self.file_path_lineEdit.text() == "":
            msgbox = QMessageBox()
            msgbox.setWindowTitle(self.tr("Info"))
            msgbox.setText(self.tr(("请创建测试数据存储文件")))
            msgbox.exec_()
            return
        else:
            return True

    def show_msg(self):
        if self.check_filePath():
            if self.check_tagInstance():
                if self.show_inventory_period_msg():
                    return True
                else:
                    return
            else:
                return
        else:
            return
    def output_testFrequencyPower(self):
        for i in range(100):
            #print u"当前值为：{0}".format(i)
            self.dataoutput_text.setText(u"当前值为：{0}".format(i))
            #time.sleep(2)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    test = window()
    test.show()
    sys.exit(app.exec_())
