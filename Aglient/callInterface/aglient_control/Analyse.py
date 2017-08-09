# -*- coding: GB18030 -*-
import os,time,xlrd,xlwt,sys,string,re
from xlutils.copy import copy

#获取excel行数和列数
def get_sheet_rows(exclename):
        r_xls = xlrd.open_workbook(exclename)
        r_sheet = r_xls.sheet_by_index(0)
        rows = r_sheet.nrows
        cols = r_sheet.ncols
        return rows,cols,r_sheet

#获取每行的数据
def get_row_data(excelname):
    row_list = []
    nrows,cols,r_sheet = get_sheet_rows(excelname)
    #获取各行数据
    for i in range(1,nrows):
        row_data = r_sheet.row_values(i)
        row_list.append(row_data)
    return  row_list


def write_PowerResult(power,power_file,curr_col,result):
    workbook = xlrd.open_workbook(power_file)
    copy_workbook = copy(workbook)
    if power == 15:
        row_num = 2
        col_num = curr_col + 1
        copy_workbook.get_sheet(0).write(row_num,col_num,result)
        copy_workbook.save(power_file)
    elif power == 26:
        row_num = 3
        col_num = curr_col + 1
        copy_workbook.get_sheet(0).write(row_num,col_num,result)
        copy_workbook.save(power_file)
    elif power == 30:
        row_num = 4
        col_num = curr_col + 1
        copy_workbook.get_sheet(0).write(row_num,col_num,result)
        copy_workbook.save(power_file)

def write_file(ModulationType_text,acpr_file,curr_num,lower_num2,lower_num1,upper_num1,upper_num2):
        workbook = xlrd.open_workbook(acpr_file)
        copy_workbook = copy(workbook)
        if ModulationType_text == 1:
            row_num = curr_num + 1
            copy_workbook.get_sheet(0).write(row_num,2,lower_num2)
            copy_workbook.get_sheet(0).write(row_num,3,lower_num1)
            copy_workbook.get_sheet(0).write(row_num,4,upper_num1)
            copy_workbook.get_sheet(0).write(row_num,5,upper_num2)
            copy_workbook.save(acpr_file)
        elif ModulationType_text == 3:
            row_num = (curr_num - 32) + 1  #PR开始写
            copy_workbook.get_sheet(0).write(row_num,10,lower_num2)
            copy_workbook.get_sheet(0).write(row_num,11,lower_num1)
            copy_workbook.get_sheet(0).write(row_num,12,upper_num1)
            copy_workbook.get_sheet(0).write(row_num,13,upper_num2)
            copy_workbook.save(acpr_file)

