#!/usr/bin/python3
#
# CPort - a new port manager for Calmira Linux
# Copyright (C) 2021, 2022 Michail Krasnov <linuxoid85@gmail.com>
#
# kernel.py
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

from os import path
import cp_default as cdf
import cp_install as cpi
#import cp_remove  as cpr
import cp_info    as cpI

PORT_DIR = cdf.PORT_DIR

"""
О возвращаемых значениях функций, использующихся в cport

0 - завершено успешно, ошибок нет.
1 - завершено, ошибки есть.
Остальные значения - ошибки:
    - отсутствует файл,
    - непоправимая ошибка, баг.
    - прочие ошибки.
"""

def check_port(port) -> bool:
    port_dir = PORT_DIR + port
    if not path.isdir(port_dir):
        cdf.msg().error(f"Port '{port}' doesn't found!")
        return False

    if not cpI.check().port_files(port):
        cdf.msg().error(f"Port '{port}' is broken!")
        return False

    return True

def print_info(port, section, params: tuple):
    for param in params:
        value = cpI.get().port_info(port, section, param)
        print(f"\033[1m{param}:\033[0m {value}")

def port_info(port) -> int:
    if not check_port(port):
        return False

    package_sect = (
        "name", "version", "description",
        "maintainer", "release", "priority"
    )
    depends_sect = (
        "required", "recommend", "optional", "conflict"
    )
    port_sect = (
        "url", "file", "build_configuration"
    )
    
    print_info(port, "package", package_sect)
    print_info(port, "depends", depends_sect)
    print_info(port, "port_management", port_sect)

    return 0

def install(port) -> int:
    if not check_port(port):
        return False
    
    ## CHECKS ##
    if cpi.prepare().check_in_db(port):
        cdf.error(f"Port '{port}' is already installed!")
        return 1

    if not cpi.prepare().download(port):
        return 1

    if not cpi.prepare().unpack(port):
        return 1

    ## BUILDING ##
    build_port = cpi.build().build(port)
    if build_port != 0:
        cdf.error(f"Some errors while building '{port}' port!")
        return build_port

    if not cpi.build().add_in_db(port):
        return 1

    return 0
