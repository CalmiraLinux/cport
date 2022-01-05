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
Функции cport. Использует Ports API.

# TODO:
- 'remove()' method;
- 'info()' method;
- 'blacklist()' method.

# Описание

Данный модуль используется в пакетном менеджере `cport` как обёртка над Port API.

В планах реализация функций для удаления порта и просмотре о нём информации,
а так же работы с чёрным списком портов.

Предназначен для использования **только** в cport.
"""

import cp_blacklists as cpb
import cp_default    as cdf
import cp_info       as cpI
import cp_install    as cpi
import cp_remove     as cpr

PORTDIR = cdf.PORTDIR

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

    log_message = f"Starting building a port '{port}'..."

    cdf.log.msg(log_message)
    cdf.log.log_msg(f"{42*'='}", level="SEP ")
    cdf.log.log_msg(log_message, level="INFO")

    ## Checkings ##
    cdf.log.log_msg("Checking for file exist...", level="INFO")
    if not cdf.check.install(port_dir):
        message = "Error while checking files for install"

        cdf.log.log_msg(message, level="ERROR")
        cdf.log.error_msg(message)

        return False
    else:
        cdf.log.log_msg("Checking successfully", level=" OK ")

    # Проверка на наличие порта в чёрном списке
    cdf.log.log_msg("Checking where port is blacklisted...", level="INFO")
    if cpb.fetch(port):
        message = f"Port '{port}' is blacklisted"

        cdf.log.log_msg(message, level="ERROR")
        cdf.log.error_msg(message)

        return False
    else:
        cdf.log.log_msg(f"Port '{port}' isn't blacklisted", level=" OK ")
    
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
    
    # Print inforpation about port
    cdf.log.msg("Base info:")
    cpI.info.port(port_config)

    cdf.log.msg("Depends", prev="\n")
    cpI.info.depends([port_config])

    cdf.dialog(p_exit=True)

    ## Download files ##
    cdf.log.log_msg(f"Downloading file '{download}'...", level="INFO")
    d = cpi.prepare.download(download, cdf.CACHE)

    if d != True:
        message = f"Error while downloading file '{download}'!"

        cdf.log.log_msg(message, level="ERROR")
        cdf.log.error_msg(message)

        return False
    else:
        cdf.log.log_msg(f"File '{download}' was downloaded successfully", level=" OK ")

    ## Unpack files ##
    cdf.log.log_msg(f"Unpacking file '{archive}'...", level="INFO")
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
        return True
    else:
        return False