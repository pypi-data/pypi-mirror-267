# -*- coding: utf-8 -*-
from loguru import logger
import time 
import functools
import sys
import os,re
 
# 日志耗时装饰器
# def logtime(func):
#     @functools.wraps(func)
#     def wrapper(*args, **kwargs):
#         start = time.perf_counter()
#         res = func(*args, **kwargs)
#         end = time.perf_counter()
#         logger.info('【%s】 took %.2f s' % (func.__name__, (end - start)))
#         return res
#     return wrapper 

def pparm(parm,func, *args, **kwargs): 
    pattern = "[$][{](\\d+)[}]|[$][{](\\d+[.][a-zA-Z]\\w*)[}]|[$][{]([a-zA-Z]\\w*)[}]"
    rs = re.findall(pattern, parm)
    for row in rs:
        if row[0]: 
            obj = args[int(row[0])]
            logger.debug('【%s】 %s %s' % (func.__name__,row[0], obj))
        elif row[1]:
            objs = re.findall('(\\d+)[.]([a-zA-Z]\\w*)', row[1])[0]
            obj = args[int(objs[0])]
            logger.debug('【%s】 %s.%s %s' % (func.__name__,objs[0],objs[1],obj.get(objs[1]))) 
        else:
            obj = kwargs.get(row[2])
            logger.debug('【%s】 %s %s' % (func.__name__,row[2], obj)) 


def logtime(parm:str=None,callback=None):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs): 
            start = time.perf_counter()
            pparm(parm,func, *args, **kwargs)
            if callback:
                res = callback(func, *args, **kwargs)
            else:
                res = func(*args, **kwargs)
            end = time.perf_counter()
             
            logger.info('【%s】 took %.2f s' % (func.__name__, (end - start)))
            return res

        return wrapper
    return decorator
'''
该日志不保存
'''
def lump_logs(guid,text):
    data_begin = f"\n-------------------- {guid} Begin --------------------\n\n"
    data_end = f"\n-------------------- {guid} End --------------------\n\n"
    logger.debug(f"{data_begin} {text} {data_end}")

##-------------------------------------------------------------------------------------------------- 
     
try:
    log_level = os.environ['LOG_LEVEL']
except KeyError:
    log_level = 3  # pylint: disable=invalid-name (C0103)
    
levels = {0: 'ERROR', 1: 'WARNING', 2: 'INFO', 3: 'DEBUG'}


def log(level=2, message="", use_color=False): 
    current_time = time.time()
    time_array = time.localtime(current_time)
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time_array)
    if log_level >= level:
        if use_color:
            print("\033[1;31;40m{} [{}]\t{}\033[0m".format(
                current_time, levels[level], message).encode("utf-8")
                  .decode("latin1"))
        else:
            print("{} [{}]\t{}".format(current_time, levels[
                level], message).encode("utf-8").decode("latin1"))
        sys.stdout.flush()


def debug(message="", use_color=False):
    log(level=3, message=message, use_color=use_color)


def info(message="", use_color=False):
    log(level=2, message=message, use_color=use_color)


def warning(message="", use_color=True):
    log(level=1, message=message, use_color=use_color)


def error(message="", use_color=True, exit=True):
    log(level=0, message=message, use_color=use_color)
    if exit:
        sys.exit(-1)