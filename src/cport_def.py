#!/usr/bin/python3
# Общие функции пакетного менеджера cport
# (C) 2021 Michail Linuxoid85 Krasnov <linuxoid85@gmail.com>
# For CalmiraLinux 2.0

import os
import time

PORTDIR = "./ports/"
LOG = "./log.txt"

class log(object):
    """Log functions"""

    def log_msg(message):
        msg = f"[ {time.ctime()} ] - {message}\n"
        
        with open(LOG, "a") as f:
            f.write(msg)
    
    def error_msg(message, prev=""):
        msg = f"[ {time.ctime()} ] - \033[31m{message}\033[0m"

        print(prev, msg)
        log.log_msg(message)
    
    def ok_msg(message, prev=""):
        msg = f"[ {time.ctime()} ] - \033[32m{message}\033[0m"

        print(prev, msg)
        log.log_msg(message)

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