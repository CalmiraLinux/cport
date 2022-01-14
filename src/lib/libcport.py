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

"""```
cport functions. Uses the Ports API.

# TODO:
- `remove()` method;
- `info()` method;
- `blacklist()` method.

# Description

This module is used in the `cport` package manager as a wrapper over the Port API.

There are plans to implement functions for deleting a port and viewing information about it,
as well as working with a blacklist of ports.

Intended for use **only** in sport.
```"""

import os
import cp_blacklists as cpb
import cp_default    as cdf
import cp_info       as cpI
import cp_install    as cpi
import cp_remove     as cpr

PORTDIR = cdf.PORTDIR

def getgid(gid: int):
    if os.getgid() != gid:
        return False
    else:
        return True

def install(port, flags="default"):
    port_dir       = PORTDIR  + port # Directory with port

    port_install   = port_dir + "/install"
    port_config    = port_dir + "/config.json"
    port_resources = port_dir + "/resources.conf"

    try:
        res = cdf.settings.get_json(port_resources)
        download = res["resources"]["url"]
        archive  = res["resources"]["file"]
    except:
        return False

    cdf.log.log_msg(f"{42*'='}", level="SEP ")
    cdf.log.log_msg(f"Starting building a port '{port}'...", level="INFO")

    ## Checkings ##
    cdf.log.log_msg("Checking for file exist...", level="INFO")
    if not cdf.check.install(port_dir):
        message = "Error during testing for the presence of port files"

        cdf.log.log_msg(message, level="FAIL")
        cdf.log.error_msg(message)

        return False
    else:
        cdf.log.log_msg("Checking successfully", level=" OK ")

    # Проверка на наличие порта в чёрном списке
    cdf.log.log_msg("Checking for the presence of a port in the blacklist...", level="INFO")
    if cpb.fetch(port):
        message = f"The port '{port}' is blacklisted"

        cdf.log.log_msg(message, level="ERROR")
        cdf.log.error_msg(message)

        return False
    else:
        cdf.log.log_msg(f"The port '{port}' isn't blacklisted", level=" OK ")
    
    # Check priority
    if cpI.get.priority(port_config) == "system":
        cdf.log.warning(f"'{port}' have a system priority!")
        cdf.dialog(p_exit=True)
        
    """
    # Check release
    if not cdf.check.release(port_config):
        cdf.log.error_msg(
            f"Port '{port}' isn't compatible with the installed Calmira release!"
        )
        cdf.dialog(p_exit=True)
    """
    
    ## Print inforpation about port ##
    print("\033[1mBase information:\033[0m")
    cpI.info.port(port_config)

    print("\n\033[0mDependencies:\033[0m")
    cpI.info.depends([port_config])

    cdf.dialog(p_exit=True)

    ## Download files ##
    message = f"Downloading file '{download}'..."

    cdf.log.log_msg(message, level="INFO")
    print(f"\n{message}", end = " ")

    d = cpi.prepare.download(download, cdf.CACHE)

    if d != True:
        message = f"Error while downloading file '{download}'!"

        cdf.log.log_msg(message, level="ERROR")
        
        return False
    else:
        cdf.log.log_msg(f"File '{download}' was downloaded successfully", level=" OK ")

    ## Unpack files ##
    message = f"Unpacking file '{archive}'..."

    cdf.log.log_msg(message, level="INFO")
    print(f"\n\n{message}")

    u = cpi.prepare.unpack(archive, cdf.CACHE)

    if u != True:
        message = f"Error while unpacking file '{archive}'"

        cdf.log.log_msg(message, level="ERROR")
        cdf.log.error_msg(message)

        return False
    else:
        cdf.log.log_msg(f"File '{archive}' was unpacked successfully", level=" OK ")
    
    del(u)
    del(d)

    ## Build port ##
    cdf.log.log_msg("Start building a port...", level="INFO")
    if cpi.install.build(port_install, flags) == 0:
        f = open(port_config)
        js = json.load(f)

        data = (
            js["name"], js["version"], js["maintainer"], js["release"], time.ctime()
        )

        cpi.install.add_in_db(data)
    else:
        return False

def remove(port):
    port_dir    = PORTDIR + port
    port_config = port_dir + "/config.json"

    cdf.log.log_msg(f"{42 * '='}", level="SEP ")
    cdf.log.log_msg(f"Starting the removal of the '{port}' port...", level="INFO")

    ## Checkings ##
    if not cdf.check.remove(port_dir):
        message = "Error during testing for the presence of port files"

        cdf.log.log_msg(message, level="FAIL")
        cdf.log.error_msg(message)

        return False
    else:
        cdf.log.log_msg("Checking successfully", level=" OK ")
    
    # Проверка на наличие порта в чёрном списке
    cdf.log.log_msg("Checking for the presence of a port in the blacklist...", level="INFO")
    if cpb.fetch(port):
        message = f"The port '{port}' is blacklisted"

        cdf.log.log_msg(message, level="FAIL")
        cdf.log.error_msg(message)

        return False
    else:
        cdf.log.log_msg(f"The port '{port}' isn't blacklisted", level=" OK ")
    
    # Check priority
    if cpI.get.priority(port_config) == "system":
        message = f"'{port}' have a system priority. Aborted."

        cdf.log.log_msg(message, level="FAIL")
        cdf.log.error_msg(message)

        return False
    
    ## Print information about port ##
    print("\033[1mBase information:\033[0m")
    cpI.info.port(port_config)

    print("\n\033[1mDependencies:\033[0m")
    cpI.info.depends([port_config])

    cdf.dialog(p_exit=True)

    ## Remove files ##
    if not cpr.remove(port):
        return False
    return True