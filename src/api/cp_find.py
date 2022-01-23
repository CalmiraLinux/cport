#!/usr/bin/python3
#
# CPort - a new port manager for Calmira Linux
# Copyright (C) 2021, 2022 Michail Krasnov <linuxoid85@gmail.com>
#
# cp_find.py
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
import json
import sqlite3
import cp_default as cdf

METADATA = cdf.METADATA_INST
PORTDIR  = cdf.PORTDIR
DB       = cdf.DB + "/installed.db"

def find_in_metadata(port: str) -> bool:
    if not cdf.check.json_config(METADATA):
        return False

    try:
        f    = open(METADATA)
        data = json.load(f)

        find_value = data["ports_list"][port]

        return True

    except KeyError:
        cdf.log.error_msg(f"Port {port} not found in metadata!")
        return False

def find_in_filesystem(port: str) -> bool:
    directory = PORTDIR + port

    if not os.path.isdir(directory):
        cdf.log.error_msg(f"Port {port} not found in Port system!")
        return False
    else:
        return True

def find_in_database(port: str) -> bool:
    conn   = sqlite3.connect(DB)
    cursor = conn.cursor()

    command = f"SELECT * FROM ports WHERE port = '{port}'"
    db      = cursor.execute(command)
    
    if db.fetchone() is None:
        return False
    else:
        return True