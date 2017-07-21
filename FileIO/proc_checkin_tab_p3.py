#! python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  3 15:31:27 2017

@author: xiaovzhi
"""

#import sys
#import calendar
from __future__ import division
from itertools import chain
import re
import datetime
import xlrd
from bs4 import BeautifulSoup


class Employee:
    '''
    员工签到信息
    '''
    eid = 0
    name = ''
    depa = ''
    record = []

    def __init__(self, no, nm, d):
        self.eid = no
        self.name = nm
        self.depa = d

def read_checkin_excel_xml(xmlfile, emlist, mondays):
    '''
    xml(xls)格式考勤表导入到列表中
    '''
    file = open(xmlfile, 'r', encoding='utf-8').read()
    soup = BeautifulSoup(file, 'xml')
    em_one = 0

    # find fisrt em info row
    for sheet in soup.findAll('Worksheet'):
        for em_one, row in enumerate(sheet.findAll('Row')):
            for col_num, cell in enumerate(row.findAll('Cell')):
                if col_num == 0 and cell.text == u'员 工':
                    # print(em_one)
                    break  # break for col_num,cell
            else:
                continue
            break  # break for em_one,row
        else:
            continue
        break  # break for sheet

    em_no = 0
    for sheet in soup.findAll('Worksheet'):
        for row_num, row in enumerate(sheet.findAll('Row')):
            if row_num == em_one + em_no * 6:  # name info row
                emobj = Employee(1, '', '')
                emobj.record = []
                for col_num, cell in enumerate(row.findAll('Cell')):
                    if col_num == 1:
                        # print(row_num, col_num)
                        # print(cell.text)
                        info = cell.text
                        fields = re.split(r'[:\s]\s*', info)

                        emobj.eid = int(fields[1])
                        emobj.name = fields[3]
                        emobj.depa = fields[5]
                        emobj.record = []
                        # print(em.name)
            elif row_num == em_one + em_no * 6 + 2:   # 1-16 day checkin info
                for col_num, cell in enumerate(row.findAll('Cell')):
                    if col_num > 0 and col_num < 17:
                        day = cell.text
                        emobj.record.append(day)
            elif row_num == em_one + em_no * 6 + 4:  # 17-31 day checkin info
                for col_num, cell in enumerate(row.findAll('Cell')):
                    if col_num > 0 and col_num < (mondays - 16 + 1):
                        day = cell.text
                        emobj.record.append(day)
                emlist.append(emobj)
                em_no += 1


def proc_chekin_xls(xlsfile, emlist, mondays):
    '''
    xls格式考勤表导入到列表中
    '''

    book = xlrd.open_workbook(xlsfile)
    sheet1 = book.sheet_by_index(0)
    em_one = 0

    # 查找第一行考勤数据, 不同月份的考勤表第一行数据位置有差异, 相差1-2行
    for em_one in range(sheet1.nrows):
        firstname = sheet1.cell(em_one, 0).value
        # print(firstname)
        if firstname == u'员 工':
            print('first row is:', em_one)
            break

    total = (sheet1.nrows - em_one + 1) // 6
    print('total worker is:', total)

    for num in range(total):
        em_row = em_one + num * 6

        # 人员信息
        info = sheet1.cell(em_row, 1).value

        # print(type(info))
        # info=info.replace(':',':  ')

        # 原始字符串  工号: xx  姓名: xxx    部门: xxx
        # 分割单词，与下面空格或冒号分隔割结果相同
        # fields = re.split('\W+', info)
        # print(fields)
        # 空格或冒号分隔
        fields = re.split(r'[:\s]\s*', info)
        # print(type(fields))
        # print(type(fields[3]))

        emobj = Employee(1, '', '')
        emobj.eid = int(fields[1])
        emobj.name = fields[3]
        emobj.depa = fields[5]
        emobj.record = []

        # 上下半月考勤信息
        for i in range(1, 17):
            day = sheet1.cell(em_row + 2, i).value
            emobj.record.append(day)

        for i in range(1, mondays - 16 + 1):
            day = sheet1.cell(em_row + 4, i).value
            emobj.record.append(day)

        emlist.append(emobj)


def output_chenin_tab(emlist, year, month, mondays, weekday):
    '''
    考勤列表排序后输出到文本文件中
    '''

    weekstr = ['一', '二', '三', '四', '五', '六', '日']

    # 两种排序方法结果相同
    emlist.sort(key=lambda e: e.eid)
    # emlist = sorted(emlist, key=lambda e:e.eid)

    strfile = '{0:d}-{1:d}-考勤.txt'.format(year, month)

    with open(strfile, 'w') as outf:
        for emobj in emlist:
            strem = '{0:d}  {1}  {2}\n'.format(
                emobj.eid, emobj.name, emobj.depa)
            outf.write(strem)
            monweekday = weekday
            if isinstance(emobj.record, list):  # 查看list元素是否是list
                for i, daystr in enumerate(emobj.record):
                    if i < mondays:
                        strday = '{0:d}-{1:d}-{2:d}[{3}]\t\t{4}\n'.format(
                            year, month, i + 1, weekstr[monweekday], daystr)
                        outf.write(strday)
                        monweekday += 1
                        if monweekday == 7:
                            monweekday = 0
                            outf.write('\n')
            outf.write('\n')


def get_mon_days(year, month):
    '''
    根据年月获得当月第一天的星期数，当月的总天数
    '''

    # monrange returns a tuple, weekday of first day of the month and number of days in month
    # weekday = calendar.monthrange(year, month)[0]
    # mondays = calendar.monthrange(year, month)[1]

    if month == 12:
        nextmonth = 1
        nextyear = year + 1
    else:
        nextmonth = month + 1
        nextyear = year

    firstday = datetime.date(year, month, 1)

    # weekday 0-6
    weekday = firstday.weekday()
    mondays = (datetime.datetime(nextyear, nextmonth, 1) -
               datetime.datetime(year, month, 1)).days

    return weekday, mondays


def istext(filename):
    '''
    check file is txt or binary format
    true  txt file
    false bin file
    '''
    checkf = open(filename, 'r', encoding='utf-8').read(512)
    text_characters = "".join(
        list(chain(map(chr, range(32, 127)))) + list("\n\r\t\b"))
    _null_trans = str.maketrans("", "", text_characters)
    if not checkf:
        # Empty files are considered text
        return True
    if "\0" in checkf:
        # Files with null bytes are likely binary
        return False
    # Get the non-text characters (maps a character to itself then
    # use the 'remove' option to get rid of the text characters.)
    trans = checkf.translate(_null_trans)
    # If more than 30% non-text characters, then
    # this is considered a binary file
    if float(len(trans)) / float(len(checkf)) > 0.30:
        return False
    return True


if __name__ == '__main__':
    #    args = sys.argv[1:]
    #
    #    if len(args) == 0:
    #        print('输入考勤文件名')
    #    else:
    #        xlsfile=args[0]

    em_set = []

    for n in range(0, 6):
        xls_file = '001_2017_{0:d}_卡式报表.xls'.format(n + 1)

        substrs = xls_file.split('_')
        c_year = int(substrs[1])
        c_month = int(substrs[2])

        week_day, month_days = get_mon_days(c_year, c_month)

#            print(xls_file)
#            print('weekday(0-6): {0:d}, mondays: {1:d}'.format(weekday, mondays))

        em_list = []

        if istext(xls_file):
            # 处理考勤xml文件
            read_checkin_excel_xml(xls_file, em_list, month_days)
        else:
            # 处理考勤xls文件
            proc_chekin_xls(xls_file, em_list, month_days)

        # 格式化输出到文本文件中
        output_chenin_tab(em_list, c_year, c_month, month_days, week_day)

        em_set.append(set())
        for l in em_list:
            em_set[n].add(l.name)

    for n in range(0, 5):
        s_inter = em_set[n] & em_set[n + 1]
        s_out = em_set[n] - s_inter
        s_in = em_set[n + 1] - s_inter
        print('离职', s_out)
        print('入职', s_in)
        print()

    print('目前在职', len(em_set[5]), em_set[5])

#            # create dynamic variable name, s1-s6
#            locals()['s_%s' % n] = set()
#            for l in emlist:
#                locals()['s_%s' % n].add(l.name)


#        for n in range(1,6):
#            s_inter = locals()['s_%s' % n] & locals()['s_%s' % str(int(n)+1)]
#            s_out   = locals()['s_%s' % n] - s_inter
#            s_in    = locals()['s_%s' % str(int(n)+1)] - s_inter
#            print('离职', s_out)
#            print('入职', s_in)
#            print()

#        print('目前在职', len(s_6), s_6)
