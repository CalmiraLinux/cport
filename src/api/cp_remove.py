#!/usr/bin/python3
#
# CPort - a new port manager for Calmira Linux
# Copyright (C) 2021, 2022 Michail Krasnov <linuxoid85@gmail.com>
#
# cp_remove.py
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
import sys
import json
import shutil
import cp_info    as cpI
import cp_default as cdf
import cp_blacklists as cpb

PORTDIR = cdf.PORTDIR
LOG     = cdf.LOG

def get_files(port) -> list:
    port_dir = PORTDIR + port
    files_list = port_dir + "/files.list"

    files = [] # Files list
    f = open(files_list, "r")

    while True:
        line = f.readline()

        if not line:
            break
        else:
            files.append(f'{line.strip()}')
    
    f.close()

    return files

def remove(port):
    files = get_files(port)
    error_files = []
    v_error = False

    for file in files:
        cdf.log.log_msg(f"Start removing a file '{file}'...", level="INFO")

        try:
            os.remove(file)
            cdf.log.log_msg(f"File '{file}' deleted successfully", level=" OK ")
        
        except IsADirectoryError:
            shutil.rmtree(file)
            cdf.log.log_msg(f"Directory '{file}' deleted successfully", level=" OK ")
        
        except FileNotFoundError:
            message = f"File '{file}' not found!"
            
            cdf.log.log_msg(message, level="FAIL")
            cdf.log.error_msg(message)

            error_files.append(file)
            v_error = True

        except PermissionError:
            message = f"Permission denied while removing a file '{file}'"
            
            cdf.log.log_msg(message, level="FAIL")
            cdf.log.error_msg(message)

            error_files.append(file)
            v_error = True

    if v_error:
        cdf.log.error_msg(f"Some errors while deleting {len(error_files)} files", prev="\n")
        return False
    else:
        cdf.log.msg(f"{len(files)} files successfully deleted")
        return True
