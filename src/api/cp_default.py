#!/usr/bin/python3
#
# CPort - a new port manager for Calmira Linux
# Copyright (C) 2021, 2022 Michail Krasnov <linuxoid85@gmail.com>
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

"""
Общие методы API
"""

import os
import time
import json
import configparser

NO_SQLITE = False

try:
    import sqlite3
except:
    NO_SQLITE = True

VERSION = "v1.0b1 DEV"
PORTDIR = "/usr/ports/"
LOG = "/var/log/cport.log"
DB  = "/var/db/cport.d"            # cport databases
CONFIG = "/etc/cport.d/cport.conf" # cport configuration file
SOURCES = "/etc/cport.d/sources.list"

CACHE = "/usr/src/"

def dialog(p_exit=False, default_no=False):
    """```
    Function for print the dialog messages.

    Arguments:
    - `p_exit`: if 'True' then exit while user input "n" or "N" (no);
    - `default_no`: if 'True' then "n" or "N" - the default answer.
    ```"""

    print("\n> Continue?", end=" ")

    if default_no:
        print("(y/N)", end=" ")
    else:
        print("(Y/n)", end=" ")

    try:
        run = input()
    except KeyboardInterrupt:
        print("Keyboard Interrupt!")
        exit(1)

    if run == "n" or run == "N":
        if p_exit:
            print("Aborted!")
            exit(1)
        else:
            print("Aborted!")
            return 1

class log(object):
    """Log functions"""

    def log_msg(message, level="ERROR"):
        """
        Format:
        [ time ] - LEVEL - message
        """
        msg = f"[ {time.ctime()} ] - {level} - {message}\n"
        
        try:
            f = open(LOG, "a")
            f.write(msg)
            f.close()
        except PermissionError:
            print(f" \033[1m!!!\033[0m \033[31mPermission denied!\033[0m")
            return 1
        except:
            return 1
    
    def error_msg(message, prev="", log=False):
        msg = f"\033[1m!!!\033[0m \033[31m{message}\033[0m"

        print(prev, msg)
        if log:
            log.log_msg(message, level="FAIL")
    
    def ok_msg(message, prev=""):
        msg = f"[ {time.ctime()} ] - \033[32m{message}\033[0m"

        print(prev, msg)
        log.log_msg(message, level=" OK ")
    
    def warning(message):
        msg = f"[ \033[1mWARNING\033[0m ] {message}"
        
        print(msg)
    
    # TODO: DEPRECATED
    def msg(message, prev="", end_msg="\n"):
        msg = f"{prev}>>> \033[32m{message}\033[0m{end_msg}"

        print(msg)

class check(object):
   
    def install(port_dir):
        files = ["/install", "/config.json"]

        v_error = False
        for file in files:
            f = port_dir + file

            if not os.path.isfile(f):
                log.error_msg(f"File '{f}': not found!")
                v_error = True
        
        if v_error:
            return False
        return True
    
    def remove(port_dir):
        files = ["/files.list", "/config.json"]

        v_error = False
        for file in files:
            file = port_dir + file

            if not os.path.isfile(file):
                log.error_msg(f"File '{file}': not found!")
                v_error = True
        
        if v_error:
            return False
        return True
    
    def json_config(config, param=None):
        if param != None:
            check_param = True
        else:
            check_param = False
        
        try:
            f = open(config)
            data = json.load(f)

            if check_param:
                data_param = data[param]
            
        except FileNotFoundError:
            log.error_msg(f"File '{config}' not found!")
            return False
        
        except KeyError:
            log.error_msg(f"File '{config}' is not a config!")
            return False
        
        except:
            log.error_msg(f"Uknown error while parsing config '{config}'!")
            return False
        
        return True
    
    def _get_calm_release():
        SYSTEM = "/etc/calm-release"
        
        if not check.json_config(SYSTEM):
            return "uknown release"
        
        f = open(SYSTEM)
        data = json.load(f)
        
        release = str(data["distroVersion"])
        f.close()
        
        return release
    
    def release(config):    
        # TODO: проверить на работоспособность    
        if check.json_config(config):
            f        = open(config)
            
            data     = json.load(f)
            releases = data["release"]
            
            f.close()

            ## CHANGE IN v1.0a3:
            # В конфиге 'config.json' релиз, для которого предназначен
            # порт, занесён в список 'release', который перебирается
            # ниже.
            ## OLD:
            # Раньше в конфиге 'release' был представлен обычным str

            for release in releases:
                if str(release) == check._get_calm_release():
                    return True
            else:
                return False

        else:
            return False

class settings(object):
    """```
    Содержит методы для работы с параметрами: получение параметров,
    изменение параметров, парсинг конфигов.
    ```"""

    conf = configparser.ConfigParser()

    def get(section, param, source=CONFIG):
        settings.conf.read(source)
        
        try:
            conf = settings.conf.get(section, param)
        except configparser.NoOptionError:
            conf = "uknown"

        return str(conf)
    
    def get_json(file):
        if check.json_config(file):
            f = open(file)
            data = json.load(f)
            f.close()

        else:
            data = {
                "data": "uknown"
            }

        return data
    
    def p_set(section, param, value, source=CONFIG):
        if os.path.isfile(source):
            log.error_msg(f"File '{source}' not found!")
            return False
        
        settings.conf.set(section, param, value)

        f = open(source, "w")
        settings.conf.write(f)
        f.close()

class lock():
    """```
    # `cp_default.lock()`

    API methods for blocking cport processes, as well as checking the status (blocked/not blocked).

    ## Files

    - `/var/lock/cport.lock` - the *.ini configuration file.

    ## File Contents

    This file contains information about the procedure that is currently being performed using cport:

    - "install";
    - "remove";
    - "other".

    ## File structure

    ```
    procedure = {procedure}
    time      = {time.ctime()}
    ```
    
    ## Variables

    - `lock.FILE` - the lock file.

    ## TODO:
    ```"""

    FILE = "/var/lock/cport.lock"

    def lock(procedure) -> bool:
        """```
        # `cp_default.lock.lock(procedure)`
        Function for blocking the cport processes

        ## Arguments:

        - `procedure`: procedure name:
            - `install`;
            - `remove`;
            - `other`.
        ```"""

        if os.path.isfile(lock.FILE):
            return False
        
        try:
            info = f"[lock]\nprocedure = {procedure}\ntime      = {time.ctime()}"
            f = open(lock.FILE, "w")
            
            f.write(info)
            f.close()

            return True
        except:
            return False
    
    def unlock() -> bool:
        """```
        # `cp_default.lock.unlock()`
        Function for unblocking the cport processes
        ```"""

        try:
            os.remove(lock.FILE)
            return True
        except:
            return False
    
    def info() -> dict:
        """```
        # `cp_default.lock.info()`

        Function for get info about the cport locking process.

        ## Returned

        The function returned a `dict`:

        ```
        data = {
            "procedure": f"{procedure}",
            "time": f"{lock_time}"
        }
        ```

        ```"""

        if not os.path.isfile(lock.FILE):
            data = {
                "procedure": "cport doesn't locked",
                "time": f"{time.ctime()}"
            }
        else:
            procedure = settings.get("lock", "procedure", source=lock.FILE)
            lock_time = settings.get("lock", "time", source=lock.FILE)

            data = {
                "procedure": procedure,
                "time": lock_time
            }

        return data