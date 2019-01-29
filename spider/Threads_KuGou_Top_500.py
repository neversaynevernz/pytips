# -*- coding: utf-8 -*-

import xlwt
import time
import json
import requests

from atexit import register
from bs4 import BeautifulSoup
from time import sleep, ctime
from threading import Thread, Lock, currentThread

class CleanOutputSet(set):
    def __str__(self):
        return ", ".join(x for x in self)


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:58.0) Gecko/20100101 Firefox/58.0'
}

ss = []
lock = Lock()
remaining = CleanOutputSet()

def loop(url):
    name = currentThread().name

    lock.acquire()
    remaining.add(name)
    # print "[%s] Started %s" % (ctime(), name)
    lock.release()

    # 处理结果
    ss.extend(top(url))

    lock.acquire()
    remaining.remove(name)
    # print "[%s] Completed %s" % (ctime(), name)
    # print "     remaining: %s" % (remaining or None)
    lock.release()

def top(url):
    html = requests.get(url, headers=headers)
    soup = BeautifulSoup(html.text, 'lxml')
    No = soup.select('.pc_temp_num')
    titles = soup.select('.pc_temp_songname')
    href = soup.select('.pc_temp_songname')
    time = soup.select('.pc_temp_time')

    cj = []
    for No, titles, time, href in zip(No, titles, time, href):
        data = {
            'NO': No.get_text().strip(),
            'titles': titles.get_text(),
            'time': time.get_text().strip(),
            'href': href.get('href')
        }
        cj.append(data)

    return cj


# 设置表格样式
def set_style(name, height, bold=False):

    style = xlwt.XFStyle()
    font = xlwt.Font()
    font.name = name
    font.bold = bold
    font.color_index = 4
    font.height = height
    style.font = font

    alignment = xlwt.Alignment() # 设置字体在单元格的位置
    alignment.horz = xlwt.Alignment.HORZ_CENTER #水平方向
    alignment.vert = xlwt.Alignment.VERT_CENTER #竖直方向
    style.alignment = alignment

    return style

# 写Excel
def write_excel():

    f = xlwt.Workbook()
    sheet1 = f.add_sheet('Top500', cell_overwrite_ok=True)

    tall_style = xlwt.easyxf('font:height 600;') # 36pt,类型小初的字号
    first_row = sheet1.row(0)
    first_row.set_style(tall_style)

    first_col = sheet1.col(0)
    first_col.width = 256 * 8

    first_col = sheet1.col(1)
    first_col.width = 256 * 50

    first_col = sheet1.col(2)
    first_col.width = 256 * 10

    first_col = sheet1.col(3)
    first_col.width = 256 * 42

    row0 = [u"排名", u"曲名", u"时长", u"网址"]

    # 写第一行
    for i in range(0, len(row0)):
        sheet1.write(0, i, row0[i], set_style('Times New Roman', 220, True))

    aa = sorted(ss, key = lambda x:int(x["NO"]))

    # 写入数据
    nc = ["NO", "titles", "time", "href"]
    for mm in range(0, len(aa)):
        for nn in range(0, len(nc)):
            sheet1.write(mm+1, nn, aa[mm].get(nc[nn]), set_style('Times New Roman', 220, True))

    f.save('T_KuGou_Top_500.xls')

@register
def _atexit():
    print "all done at:", ctime()

def _main():
    print "task start at:", ctime()

    urls = [
        'http://www.kugou.com/yy/rank/home/{}-8888.html'.format(str(i)) for i in range(1, 24)
    ]

    threads = []

    for url in urls:
        threads.append(Thread(target=loop, args=(url,)))

    for t in threads:
        t.setDaemon(True)
        t.start()

    for t in threads:
        t.join()

    write_excel()

if __name__ == '__main__':
    _main()
