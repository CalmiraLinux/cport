#!/usr/bin/python3
# Общие функции пакетного менеджера cport
# (C) 2021 Michail Linuxoid85 Krasnov <linuxoid85@gmail.com>
# For CalmiraLinux 2.0

import os
import time

NO_SQLITE = False

try:
    import sqlite3
except:
    NO_SQLITE = True

PORTDIR = "./ports/"
LOG = "./log.txt"
VERSION = "1.0a1"

def dialog():
    run = input("Continue? (y/n)")

    if run == "y" or run == "Y":
        return 0
    else:
        return 1

class log(object):
    """Log functions"""

    def log_msg(message):
        msg = f"[ {time.ctime()} ] - {message}\n"
        
        with open(LOG, "a") as f:
            f.write(msg)
    
    def error_msg(message, prev=""):
        msg = f"!!! \033[31m{message}\033[0m"

        print(prev, msg)
        log.log_msg(message)
    
    def ok_msg(message, prev=""):
        msg = f"[ {time.ctime()} ] - \033[32m{message}\033[0m"

        print(prev, msg)
        log.log_msg(message)
    
    def msg(message, prev="", end_msg="\n"):
        msg = f"{prev}>>> \033[32m{message}\033[0m{end_msg}"

        print(msg)

class check(object):
   
    def install(port_dir):
        #self.port_dir = port_dir

        files = ["/install", "/config.json"]

        v_error = False
        for file in files:
            file = port_dir + file

            if not os.path.isfile(file):
                log.error_msg(f"File '{file}': not found!")
                v_error = True
        
        if v_error:
            return False
        return True
    
    def remove(port_dir):

        files = ["/remove", "/config.json"]

        v_error = False
        for file in files:
            file = port_dir + file

            if not os.path.isfile(file):
                log.error_msg(f"File '{file}': not found!")
                v_error = True
        
        if v_error:
            return False
        return True

class db(object):

    def add(data: list):
        """
        Добавляет данные в таблицу. data:
        [name, version, maintainer, priority, install_date]
        """

        if len(data) != 5:
            log.error_msg("Incorrect number of data to be added to the database was passed")
            return 1
        
        if NO_SQLITE:
            log.error_msg("sqlite3 database cannot be used!")
            return 1