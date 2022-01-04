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

    """
    res = cdf.settings.get_json(port_resources)
    download = res["resources"]["url"]
    archive  = res["resources"]["file"]
    """

    log_message = f"Starting building a port '{port}'..."

    cdf.log.msg(log_message)
    cdf.log.log_msg(log_message, level="INFO")

    ## Checkings ##
    if cdf.check.install(port_dir) and not cpb.fetch(port):
        # Check priority
        if cpI.get.priority(port_config) == "system":
            cdf.log.warning(f"'{port}' have a system priority!")
            cdf.dialog(p_exit=True)
        
        """
        # Check release
        if not cdf.check.release(port_config):
            cdf.log.error_msg(f"Port '{port}' doesn't compatible with the installed Calmira release!")
            cdf.dialog(p_exit=True)
        """
    
    else:
        cdf.log.log_msg(f"Error while checking port '{port}' for building", level="FAIL")
        return False
    
    # Print inforpation about port
    cdf.log.msg("Base info:")
    cpI.info.port(port_config)

    cdf.log.msg("Depends", prev="\n")
    cpI.info.depends([port_config])

    cdf.dialog(p_exit=True)

    """
    # Download, unpack and build port
    if cpi.prepare.download(download, cdf.CACHE) and cpi.prepare.unpack(archive, cdf.CACHE):
        # Building port
        if cpi.install.build(port_install, flags) == 0:
            return True
        else:
            return False
    """

    if cpi.install.build(port_install, flags) == 0:
        return True
    else:
        return False
    
    """
    else:
        cdf.log.log_msg(f"Some errors while downloading or unpacking the port files!", level="FAIL")
        return False
    """