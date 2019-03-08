#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
from time import strftime, localtime, time, mktime, strptime


def after_n_days(n):
    n = int(n)
    rd = datetime.datetime.today()
    return rd + datetime.timedelta(days=n)


def about_stamp(n):
    dd = {}
    dd["stamp"] = n
    dd["timestr"] = strftime("%Y-%m-%d %H:%M:%S", localtime(n))
    dd["week"] = strftime("%w", localtime(n))
    return dd


def next_w(w, h=None, m=None, s=None):

    '''
    param:
        next (周w h时 m分 s秒)
    '''
    now_time = int(time())
    now_local = localtime(now_time)
    now_week_o = strftime("%w", now_local)
    now_h, now_h, now_h = strftime("%H %M %S", now_local).split()

    next_h = h if h else now_h
    next_m = m if m else now_m
    next_s = s if s else now_s

    next_h_m_s = " " + ":".join([next_h, next_m, next_s])

    if now_week_o < w:
        n = 7 - (int(w) - int(now_week_o))
    elif now_week_o == w:
        ns = after_n_days(0)
        tstr = ns.strftime('%Y-%m-%d') + next_h_m_s
        nextime = mktime(strptime(tstr, "%Y-%m-%d %H:%M:%S"))
        if nextime > now_time:
            n = 0
        else:
            n = 7
    elif now_week_o > w:
        n = int(now_week_o) - int(w)

    ns = after_n_days(n)
    tstr = ns.strftime('%Y-%m-%d') + next_h_m_s
    return about_stamp(mktime(strptime(tstr, "%Y-%m-%d %H:%M:%S")))


if __name__ == "__main__":
    print next_w("5", "14", "00", "00")
    print next_w("5", "17", "00", "00")
    print next_w("4", "14", "00", "00")
    print next_w("4", "17", "00", "00")
    print next_w("6", "14", "00", "00")
    print next_w("6", "17", "00", "00")
