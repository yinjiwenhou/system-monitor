#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import commands
import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

LOG_PATH = '/home/tom/Log/SystemMonitor/logger.txt'
fh = RotatingFileHandler(LOG_PATH, maxBytes=10*1024*1024, backupCount=5)
fh.setLevel(logging.DEBUG)
fh_formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
fh.setFormatter(fh_formatter)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch_formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
ch.setFormatter(ch_formatter)

logger.addHandler(fh)
logger.addHandler(ch)

def get_cpu_count():
    cmd = 'cat /proc/cpuinfo | grep -w processor | wc -l'
    status, output = commands.getstatusoutput(cmd)
    if status != 0:
        logging.error('get cpu count failed!')
        exit(1)
    return int(output)

def get_cpu_usage():
    stat_new_path = '/tmp/os_msg/stat_new'
    stat_old_path = '/tmp/os_msg/stat_old'

    cmd = 'cat /proc/stat >' + stat_new_path
    status, output = commands.getstatusoutput(cmd)
    if status != 0:
        logging.error(output)

    if not os.path.exists(stat_old_path):
        os.system("mkdir /tmp/os_msg/")
        logging.info('first to get the cpu usage')

        cmd_cp = "cp " + stat_new_path + " " + stat_old_path
        status, output = commands.getstatusoutput(cmd_cp)
        if status != 0:
            logging.error(output)
        return 0

    totle_new = 0.0
    totle_old = 0.0
    used_new = 0.0
    used_old = 0.0

    cmd_new_stat = "cat " + stat_new_path + " | grep -w cpu | awk '{print $0}' "
    status, output_info_new = commands.getstatusoutput(cmd_new_stat)
    for each in output_info_new.split(" ")[2:9]:
        totle_new += float(each)
    for each in output_info_new.split(" ")[2:4]:
        used_new += float(each)
    logging.info('totle_new : %.4f' % totle_new)
    logging.info('used_new : %.4f' % used_new)

    cmd_old_stat = "cat " + stat_old_path + " | grep -w cpu | awk '{print $0}' "
    status, output_info_old = commands.getstatusoutput(cmd_old_stat)
    for each in output_info_old.split(" ")[2:9]:
        totle_old += float(each)
    for each in output_info_old.split(" ")[2:4]:
        used_old += float(each)
    logging.info('totle_old : %.4f' % totle_old)
    logging.info('used_old : %.4f' % used_old)
    """
    cmd_new_date = "date -r " + stat_new_path + " '+%s'"
    status, output_date_new = commands.getstatusoutput(cmd_new_date)
    date_new = int(output_date_new)

    cmd_old_date = "date -r " + stat_old_path + " '+%s'"
    status, output_date_old = commands.getstatusoutput(cmd_old_date)
    data_old = int(output_date_old)
    """
    cmd_cp = "cp " + stat_new_path + " " + stat_old_path
    status, output = commands.getstatusoutput(cmd_cp)
    if status != 0:
        logging.error(output)

    return (used_new - used_old) / (totle_new - totle_old) * 100

def get_mem_usage():
    cmd = "cat /proc/meminfo | grep -w MemFree | awk '{print $2}'"
    status, output_free = commands.getstatusoutput(cmd)
    if status != 0:
        logging.error("get MemFree error")

    cmd = "cat /proc/meminfo | grep -w MemTotal | awk '{print $2}'"
    status, output_total = commands.getstatusoutput(cmd)
    if status != 0:
        logging.error("get MemTotal error")

    return (1 - float(output_free) / float(output_total)) * 100
