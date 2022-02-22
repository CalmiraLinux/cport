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

VERSION = "v1.0b1 DEV"
PORTDIR = "/usr/ports/"
LOG_DIR = "/var/log/cport.log.d"
LOG_FILE = "/var/log/cport.log"
DB  = "/var/db/cport.d"            # cport databases
CONFIG = "/etc/cport.d/cport.conf" # cport configuration file
SOURCES = "/etc/cport.d/sources.list"
METADATA_INST = "/usr/share/cport/metadata.json"    # Installed metadata file
METADATA_TMP  = "/tmp/metadata.json"                # Temp downloaded metadata file
CACHE = "/usr/src/"

LOG = LOG_FILE # Для совместимости со старыми версиями. TODO - ВРЕМЕННО

class log:

    def __init__(self):
        if os.path.isdir(LOG_DIR):
            self.logdir = True
        else:
            self.logdir = False
    
    def log(self, message, level="UKNOWN"):
        msg = f"[ {time.ctime()} ] - {level} - {message}"

        with open(LOG_FILE, "a") as f:
            f.write(msg)
    
    def show(self):
        with open(LOG_FILE) as f:
            print(f.read())

class msg:

    def error(self, message, prev="", log=False):
        msg = f"\033[1m!!!\033[0m \033[31m{message}\033[0m"

        print(prev, msg)
        if log:
            log().log(message, level="FAIL")
    
    def ok(self, message, prev="", log=False):
        msg = f"[ {time.ctime()} ] - \033[32m{message}\033[0m"

        print(prev, msg)
        if log:
            log().log(message, level=" OK ")
    
    def warning(self, message):
        msg = f"[ \033[1mWARNING\033[0m ] {message}"
        
        print(msg)
    
    def dialog(self, default_no=False):
        print("\n> Continue?", end=" ")

        if default_no:
            print("(y/N)", end=" ")
        else:
            print("(Y/n)", end=" ")
        
        try:
            run = input()
        except KeyboardInterrupt:
            print("Keyboard Interrupt!")
            return False
        
        if run == "n" or run == "N":
            print("Aborted!")
            return False
        elif run == "y" or run == "Y":
            return True
        else:
            print(f"Uknown command '{run}'!")
            return False

class check():
   
    def install(self, port_dir):
        files = ["/install", "/config.json"]

        v_error = False
        for file in files:
            f = port_dir + file

            if not os.path.isfile(f):
                log().error_msg(f"File '{f}': not found!")
                v_error = True
        
        if v_error:
            return False
        return True
    
    def remove(self, port_dir):
        files = ["/files.list", "/config.json"]

        v_error = False
        for file in files:
            file = port_dir + file

            if not os.path.isfile(file):
                log().error_msg(f"File '{file}': not found!")
                v_error = True
        
        if v_error:
            return False
        return True
    
    def json_config(self, config, param=None) -> bool:
        if param != None:
            check_param = True
        else:
            check_param = False
        
        try:
            with open(config) as f:
                data = json.load(f)

            if check_param:
                data_param = data[param] # Проверка наличия значения в словаре
                del(data_param) # Очистка
            
        except FileNotFoundError:
            log().error_msg(f"File '{config}' not found!")
            return False
        
        except KeyError:
            log().error_msg(f"File '{config}' is not a config!")
            return False
        
        except:
            log().error_msg(f"Uknown error while parsing config '{config}'!")
            return False
        
        return True
    
    def _get_calm_release(self):
        SYSTEM = "/etc/calm-release"
        
        if not check.json_config(SYSTEM):
            return "NaN"
        
        f = open(SYSTEM)
        data = json.load(f)
        
        release = str(data["distroVersion"])
        f.close()
        
        return release
    
    def release(self, config):    
        # TODO: проверить на работоспособность    
        if not self.json_config(config):
            return False
        
        f        = open(config)

        with open(config) as f:
            data = json.load(f)
            releases = data["release"]

        ## CHANGE IN v1.0a3:
        # В конфиге 'config.json' релиз, для которого предназначен
        # порт, занесён в список 'release', который перебирается
        # ниже.
        ## OLD:
        # Раньше в конфиге 'release' был представлен обычным str

        for release in releases:
            if str(release) == self._get_calm_release():
                return True
        else:
            return False

class settings:

    def __init__(self):
        self.conf = configparser.ConfigParser()
    
    def _get_conf_type(self, param_name):
        """
        Function for get data type of some parameter from *.ini file

        Usage:
        settings()._get_conf_type(param_name)
        """
        
        param_type = str(f"{param_name[-2]}{param_name[-1]}")

        match(param_type):
            case "_i":
                return int
            case "_f":
                return float
            case "_s":
                return str
            case "_b":
                return bool
            case "_t":
                return tuple
            case "_l":
                return list
            case _:
                return str
    
    def _check_config(self, section, param):
        """
        Function for check some parameters from *.ini config files

        Usage:
        settings()._check_config(section, param)
        """

        try:
            conf = self.conf.get(section, param)
            no_option = False
        except configparser.NoOptionError:
            conf = "uknown"
            no_option = True
        
        if no_option:
            return False
        else:
            return True
    
    def config_param_get(self, section, param, source=CONFIG):
        """
        Get some parameters from *.ini config file

        Usage:
        settings().get(section, param, source=SOURCE)
        """

        self.conf.read(source)

        if not self._check_config(section, param):
            no_option = True
            conf = self.conf.get(section, param)
        else:
            no_option = False
            conf = "uknown"
        
        if not no_option:
            param_type = self._get_conf_type(param)
            conf = param_type(conf)
        
        return conf
    
    def config_param_set(self, section, param, value: str, source=CONFIG):
        """
        Function for update some params in the *.ini config files.

        Usage:
        settings().config_param_set(section, param, value, source=SOURCE)
        """

        if not os.path.isfile(source):
            msg().error(f"File '{source}' not found!")
            return False
        
        if not self._check_config(section, param):
            msg().error(f"Parameter '{param}' is uknown!")
            return False
        
        self.conf.set(section, param, value)

        with open(source, "w") as f:
            self.conf.write(f)
        
        return True
    
    def json_data_get(self, file) -> dict:
        """
        Get all parameters from *.json file.

        Usage:
        settings().json_data_get(file)
        """

        if check().json_config(file):
            with open(file) as f:
                data = json.load(f)
        else:
            data = {
                "data": "uknown"
            }

        return data

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

    def __init__(self, procedure=None):
        self.procedure = procedure

    def lock(self) -> bool:
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
            info = f"[lock]\nprocedure = {self.procedure}\ntime      = {time.ctime()}"

            with open(self.FILE, "w") as f:
                f.write(info)
            return True

        except:
            return False
    
    def unlock(self) -> bool:
        """```
        # `cp_default.lock.unlock()`
        Function for unblocking the cport processes
        ```"""

        if self.procedure != None:
            if settings().get("lock", "procedure", source=self.FILE) != self.procedure:
                return False

        try:
            os.remove(lock.FILE)
            return True
        except:
            return False
    
    def info(self) -> dict:
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
            procedure = settings().get("lock", "procedure", source=lock.FILE)
            lock_time = settings().get("lock", "time", source=lock.FILE)

            data = {
                "procedure": procedure,
                "time": lock_time
            }

        return data