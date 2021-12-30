#!/usr/bin/python3
#
# CPort - a new port manager for Calmira Linux
# Copyright (C) 2021 Michail Krasnov <linuxoid85@gmail.com>
#
# cp_default.py
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
# Project Page: http://github.com/Linuxoid85/cport
# Michail Krasnov (aka Linuxoid85) linuxoid85@gmail.com
#

import os
import time

NO_SQLITE = False

try:
    import sqlite3
except:
    NO_SQLITE = True

PORTDIR = "./ports/"
LOG = "./cport.log"

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
        
        try:
            with open(LOG, "a") as f:
                f.write(msg)
        except PermissionError:
            print(f" \033[1m!!!\033[0m \033[31mPermission denied!\033[0m")
            exit(1)
    
    def error_msg(message, prev="", log=None):
        msg = f"\033[1m!!!\033[0m \033[31m{message}\033[0m"

        print(prev, msg)
        if log != None:
            log.log_msg(log)
        else:
            log.log_msg(message)
    
    def ok_msg(message, prev=""):
        msg = f"[ {time.ctime()} ] - \033[32m{message}\033[0m"

        print(prev, msg)
        log.log_msg(message)
    
    def warning(message):
        msg = f"> \033[1mWARNING\033[0m {message}"
        
        print(msg)
    
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
    
    def get_calm_release():
        SYSTEM = "/etc/calm-release"
        
        try:
            f = open(SYSTEM)
            data = json.load(f)
        except FileNotFoundError:
            log.error_msg(f"File '{SYSTEM}' not found!")
            exit(1)
        except KeyError:
            log.error_msg(f"File '{SYSTEM}' is not a config file!")
            exit(1)
        except:
            log.error_msg(f"Uknown error while parsing file '{SYSTEM}'!")
            exit(1)
        
        release = str(data["distroVersion"])
        f.close()
        
        return release
    
    def release(config):
        SYSTEM = "/etc/calm-release"
        
        for file in config, SYSTEM:
            if not os.path.isfile(file):
                log.error_msg(f"File '{file}' not found!")
                exit(1)
        
        try:
            f = open(config)
            data = json.load(f)
        except FileNotFoundError:
            log.error_msg(f"File '{config}' not found!")
            exit(1)
        except KeyError:
            log.error_msg(f"File '{config}' is not a config file!")
            exit(1)
        except:
            log.error_msg(f"Uknown error while parsing file '{config}'!")
            exit(1)
        
        if str(data["release"]) != check.get_calm_release():
            log.warning("Возможно, этот порт не предназначен для сборки на данной системе")

class db(object):

    def add(data: list):
        """
        Добавляет данные в таблицу. data:
        [name, version, maintainer, priority, install_date]
        """

        if len(data) != 5:
            log.error_msg(
                "Incorrect number of data to be added the database was passed"
            )
            return 1
        
        if NO_SQLITE:
            log.error_msg("sqlite3 database cannot be used!")
            return 1
