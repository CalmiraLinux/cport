#!/usr/bin/python3
#
# CPort - a new port manager for Calmira Linux
# Copyright (C) 2021, 2022 Michail Krasnov <linuxoid85@gmail.com>
#
# libcport.py
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
cport functions. Uses the Ports API.

## TODO:
- 'update()' method.

## Description

This module is used in the cport package manager as a wrapper over the Port
API.

There are plans to implement functions for deleting a port and viewing
information about it, as well as working with a blacklist of ports.

Intended for use **only** in cport.
"""

import os
import json
import time
import sqlite3
import cp_blacklists as cpb
import cp_default    as cdf
import cp_info       as cpI
import cp_install    as cpi
import cp_remove     as cpr

VERSION  = "v1.0a4"
PORTDIR  = cdf.PORTDIR
METADATA = cdf.METADATA_INST

def ver(args):
    msg = f"cport {VERSION} - utility for manage Calmira Port system"
    msg_api = f"API version: {cdf.VERSION}\n"
    print(msg)
    print(msg_api)
    print("(C) 2021, 2022 Michail Linuxoid85 Krasnov <linuxoid85@gmail.com>")

    print("\033[1mZ 🇷🇺️\033[0m")

def getgid(gid: int):
    if os.getgid() != gid:
        return False
    else:
        return True

def unlock():
    if not cdf.lock().unlock():
        cdf.msg().error("Unknown error unlocking the cport process")
        return False
    else:
        return True

def install(port, yes_st=False):
    port_dir       = PORTDIR  + port # Directory with port

    port_install   = port_dir + "/install"
    port_config    = port_dir + "/config.json"
    port_resources = port_dir + "/resources.conf"

    print("check locking")
    if os.path.isfile(cdf.lock.FILE):
        data = cdf.lock().info()

        cdf.msg().error(
            f"""The port assembly process cannot be started!
            The cport process executes the following script {data['procedure']}, started at {data['time']}"""
        )
        return False
    
    print("locking...")
    if not cdf.lock("install").lock():
        cdf.msg().error("Unknown error blocking the installation process")
        return False

    print("parsing the resources file...")
    
    res = cdf.settings().json_data_get(port_resources)
    download = res["resources"]["url"]
    archive  = res["resources"]["file"]

    print("start building a port...")
    cdf.log().log(f"{42*'='}", level="SEP ")
    cdf.log().log(f"Starting building a port '{port}'...", level="INFO")

    ## Checkings ##
    cdf.log().log("Checking for file exist...", level="INFO")
    if not cdf.check().install(port_dir):
        message = "Error during testing for the presence of port files"

        cdf.log().log(message, level="FAIL")
        cdf.msg().error(message)

        unlock()
        return False
    else:
        cdf.log().log("Checking successfully", level=" OK ")

    # Проверка на наличие порта в чёрном списке
    cdf.log().log("Checking for the presence of a port in the blacklist...", level="INFO")
    if cpb.check().exists_db(port):
        message = f"The port '{port}' is blacklisted"

        cdf.log().log(message, level="ERROR")
        cdf.msg().error(message)

        unlock()
        return False
    else:
        cdf.log().log(f"The port '{port}' isn't blacklisted", level=" OK ")
    
    # Check priority
    if cpI.get(port_config).priority() == "system":
        cdf.msg().warning(f"'{port}' have a system priority!")
        cdf.msg().dialog()
    
    # Check disk usage
    with open(port_config) as f:
        try:
            data = json.load(f)
            size = float(data["size"])
        except:
            size = 1.0
    
    if not cpi.prepare().check_size(size):
        message = "There is no space on the hard disk to build the port!"
        cdf.log().log(message)
        cdf.msg().error(message)

        return False
    
    """
    # Check release
    if not cdf.check().release(port_config):
        cdf.msg().error(
            f"Port '{port}' isn't compatible with the installed Calmira release!"
        )
        cdf.msg().dialog()
    """
    
    ## Print inforpation about port ##
    print("\033[1mBase information:\033[0m")
    cpI.info(port_config).port()

    print("\n\033[0mDependencies:\033[0m")
    cpI.info(port_config).depends()

    if not yes_st:
        if not cdf.msg().dialog():
            unlock()
            return False

    ## Download files ##
    message = f"Downloading file '{download}'..."

    cdf.log().log(message, level="INFO")
    print(f"\n{message}")

    # Следующая часть кода скачивает необходимый файл из репозиториев
    # NOTE: работает только в том случае, когда выключен
    # cacheonly-режим ('cache_b = false' в /etc/cport.d/cport.conf).
    cache = cdf.settings().config_param_get("develop", "cache_b")

    if cache:
        d = cpi.prepare().download(download, cdf.CACHE)

        if d != True:
            message = f"Error while downloading file '{download}'!"

            cdf.log().log(message, level="ERROR")
            unlock()

            return False
        else:
            cdf.log().log(f"File '{download}' was downloaded successfully", level=" OK ")
    else:
        cdf.msg().warning("Cacheonly mode is used! In this case, no files will be downloaded. Local versions of archives are used (if they are present on the disk).")
    
    ## Unpack files ##
    message = f"Unpacking file '{archive}'..."

    cdf.log().log(message, level="INFO")
    print(f"\n\n{message}")

    u = cpi.prepare().unpack(archive, cdf.CACHE)

    if u != True:
        message = f"Error while unpacking file '{archive}'"

        cdf.log().log(message, level="ERROR")
        cdf.msg().error(message)

        unlock()
        return False
    else:
        cdf.log().log(f"File '{archive}' was unpacked successfully", level=" OK ")
    
    del(u)
    del(d)

    ## Build port ##
    cdf.log().log("Start building a port...", level="INFO")
    if cpi.install().build(port_install) == 0:
        with open(port_config) as f:
            js = json.load(f)

        data = (
            js["name"], js["version"], js["maintainer"], js["release"], time.ctime()
        )

        cpi.install().add_in_db(data)

        unlock()
        return True
    else:
        unlock()
        return False

def remove(port, yes_st):
    port_dir    = PORTDIR + port
    port_config = port_dir + "/config.json"

    if os.path.isfile(cdf.lock.FILE):
        data = cdf.lock().info()
        cdf.msg().error(
            f"""The port assembly process cannot be started!
            The cport process executes the following script {data['procedure']}, started at {data['time']}"""
        )
        return False
    
    if not cdf.lock("remove").lock():
        cdf.msg().error("Unknown error blocking the deletion process")
        return False

    cdf.log().log(f"{42 * '='}", level="SEP ")
    cdf.log().log(f"Starting the removal of the '{port}' port...", level="INFO")

    ## Checkings ##
    if not cdf.check.remove(port_dir):
        message = "Error during testing for the presence of port files"

        cdf.log().log(message, level="FAIL")
        cdf.msg().error(message)

        unlock()
        return False
    else:
        cdf.log().log("Checking successfully", level=" OK ")
    
    # Проверка на наличие порта в чёрном списке
    cdf.log().log("Checking for the presence of a port in the blacklist...", level="INFO")
    if cpb.check().exists_db(port):
        message = f"The port '{port}' is blacklisted"

        cdf.log().log(message, level="FAIL")
        cdf.msg().error(message)

        unlock()
        return False
    else:
        cdf.log().log(f"The port '{port}' isn't blacklisted", level=" OK ")
    
    # Check priority
    if cpI.get(port_config).priority() == "system":
        message = f"'{port}' have a system priority. Aborted."

        cdf.log().log(message, level="FAIL")
        cdf.msg().error(message)

        unlock()
        return False
    
    ## Print information about port ##
    print("\033[1mBase information:\033[0m")
    cpI.info(port_config).port()

    print("\n\033[1mDependencies:\033[0m")
    cpI.info(port_config).depends()

    if not yes_st:
        if not cdf.msg().dialog():
            unlock()
            return False

    ## Remove files ##
    for port in args.remove:
        if not cpr.remove(port).remove():
            unlock()
            
            message = f"Port '{port}' is damaged!"
            cdf.log().log(message, level="FAIL")
            cdf.msg().error(message)

            return False
        
        if not cpr.remove(port).remove_from_db():
            unlock()

            message = f"Port '{port}' was removed from the system, but by an unknown error remained in the '{cdf.DB+'/installed.db'}' database!"
            cdf.log().log(message, level="FAIL")
            cdf.msg().error(message)

            return False
    unlock()
    return True

class find():
    """
    Class with methods for search the ports in filesystem,
    ports metadata and databases

    Methods:
    - filesystem() - find ports in filesystem (/usr/ports/*)
    - database(db) - find ports in database (e.g. installed.db)
    - metadata() - find ports in cport metadata
    - f_all() - find ports in filesystem, database and metadata.
    """

    def __init__(self, args):
        if args.find_fs:
            self.port = args.find_fs
            self.filesystem()
        elif args.find_db:
            self.port = args.find_db
            self.database(cdf.DB+"/installed.db")
        else:
            self.port = args.find_md
            self.metadata()

    def filesystem(self) -> bool:
        directory = "/usr/ports/" + self.port

        if not os.path.isdir(directory):
            print(f"{self.port}: false")
            return False
        else:
            print(f"{self.port}: true")
            return True
    
    def database(self, database) -> bool:
        conn   = sqlite3.connect(database)
        cursor = conn.cursor()

        command = f"SELECT * FROM ports WHERE name = '{self.port}'"
        db      = cursor.execute(command)

        if db.fetchone() is None:
            print(f"\033[1m{self.port}\033[0m: false")
            return False
        else:
            print(f"\033[1m{self.port}\033[0m: true")
            return True

    def metadata(self) -> bool:
        if not cdf.check.json_config(METADATA):
            cdf.msg().error(f"Config {METADATA} is not config")
            return False
        
        try:
            with open(METADATA, 'r') as f:
                data = json.load(f)
                find_value = data["port_list"][self.port] # Проверка наличия значения в словаре
            del(find_value)

            return True
        except:
            cdf.msg().error(f"Port '{self.port}' doesn't found in metadata!")
            return False
    
    def f_all(self) -> dict:
        cdf.log().log(f"Checking found port '{self.port}' in metadata", level="INFO")

        if not self.metadata(self.port):
            cdf.log().log(f"Port '{self.port}' doesn't found in metadata!", level="FAIL")
            metadata = False

        else:
            cdf.log().log(f"Port '{self.port}' is found in metadata!", level=" OK ")
            metadata = True
        
        cdf.log().log(f"Checking found port '{self.port}' in filesystem", level="INFO")

        if not self.filesystem(self.port):
            cdf.log().log(f"Port '{self.port}' doesn't found in filesystem!", level="FAIL")
            filesystem = False

        else:
            cdf.log().log(f"Port '{self.port}' is found in filesystem!", level=" OK ")
            filesystem = True
        
        cdf.log().log(f"Checking found port '{self.port}' in installed database", level="INFO")

        if not self.database(self.port):
            cdf.log().log(f"Port '{self.port}' doesn't found in database!", level="FAIL")
            database = False

        else:
            cdf.log().log(f"Port '{self.port}' is found in database!", level=" OK ")
            database = True
        
        data = {
            "metadata": metadata,
            "filesystem": filesystem,
            "database": database
        }

        return data

class check():
    """
    Class with methods for checking ports
    """

    def __init__(self, port: str):
        self.port  = port
        self.p_dir = PORTDIR + port
    
    def port_dir(self) -> bool:
        cdf.log().log(f"Start checking of exists dir '{self.p_dir}'...", level="INFO")
        if os.path.isdir(self.p_dir):
            cdf.log().log("OK", level=" OK ")
            return True
        else:
            cdf.log().log("FAIL", level="FAIL")
            return False
    
    def port_files(self) -> bool:
        cdf.log().log(f"Start checking of exists port '{self.port}' files...", level="INFO")

        files = [
            "config.json",
            "resources.conf"
            "install"
        ] # Require files

        additional_files = [
            "files.list",
            "port_configuration.sh"
        ]

        files_not_exist = []

        for file in files:
            file = self.p_dir + "/" + file

            if not os.path.isfile(file):
                files_not_exist.append(file)
        
        f_n_e = ""
        f_add = ""
        for file in files_not_exist:
            f_n_e = f_n_e + f"{file} "
        
        print(f"\033[1mDon't exist files:\033[0m {f_n_e}")

        for file in additional_files:
            if os.path.isfile(file):
                f_add = f_add + f"{file} "
        
        print(f"Additional files:\n{f_add}")
        
        del(f_add)
        del(file)
        del(additional_files)

        if len(files_not_exist) > 0:
            return False
        else:
            return True

class blacklists():

    def __init__(self, args):
        if args.add_blacklist:
            self.add(args.add_blacklist)
        elif args.remove_blacklist:
            self.remove(args.remove_blacklist)
        else:
            self.fetch(args.fetch_blacklist)

    def add(self, port) -> int:
        if cpb.check().exists_db(port):
            cdf.msg().error(f"Error: Port '{port}' is already blacklisted!")
            return 1
        
        if not cpb.add(port):
            return 1
        else:
            return 0

    def remove(self, port) -> int:
        if not cpb.check().exists_db(port):
            cdf.msg().error(f"Error: Port '{port}' is not blacklisted!")
            return 1
        
        if not cpb.remove(port):
            return 1
        else:
            return 0

    def fetch(self, port) -> int:
        if cpb.check().exists_db(port):
            print(f"\033[1m{port}\033[0m: true")
            return 0
        else:
            print(f"\033[1m{port}\033[0m: false")
            return 1

def inst_port(args):
    if args.yes_answer:
        yes_answ = True
    else:
        yes_answ = False
    
    for port in args.inst:
        install(port, yes_st=yes_answ)

        if len(args.inst) > 1:
            sep = 80 * "-"
            print(sep)

def rem_port(args):
    if args.yes_answer:
        yes_answ = True
    else:
        yes_answ = False
    
    for port in args.remove:
        remove(port, yes_st=yes_answ)

        if len(args.remove) > 1:
            sep = 80 * "-"
            print(sep)

def info(args):
    if args.info:
        port_config = PORTDIR + args.info + "/config.json"
    
    if not os.path.isfile(port_config):
        cdf.msg().error(f"File '{port_config}' not found!")
        return False
    
    cpI.info(port_config).port()
    return True