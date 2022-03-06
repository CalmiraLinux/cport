#!/usr/bin/python3
#
# CPort - a new port manager for Calmira Linux
# Copyright (C) 2021, 2022 Michail Krasnov <linuxoid85@gmail.com>
#
# cp_blacklists.py
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
A module with functions for working with a blacklist of ports.

Opportunities:
- Adding ports to the blacklist;
- Removing ports from the blacklist;
- Viewing the contents of the blacklist - TODO;
- Checking for the presence of a port in the blacklist - TODO.

The blacklist is represented by the SQLite3 database. By default,
it is not installed in the Caldera Linux distribution, so if the
database is not found, then working with the blacklist will be
impossible.

Table contents:
| Port name | Date added to blacklist |
|-----------|-------------------------|
| test_port | 31.12.2021              | (for example)
"""

import os
import time
import json
import cp_default as cdf
import cp_info    as cpI

try:
    import sqlite3

    PORTDIR = cdf.PORTDIR
    db = cdf.DB + "/blacklist.db"

    conn = sqlite3.connect(db)
    cursor = conn.cursor()
except:
    cdf.log().error_msg(
        "It is not possible to use the cp_blacklists API Module: you must install the 'sqlite3' port and rebuild the 'base/python' port."
    )
    exit(1)

def _get_port_info(port: str) -> dict:
    """
    Get all port information from 'config.json' port file
    
    Usage:
    _get_port_info(port: str)
    
    'port' - the port name (e.g. base/editors/vim)
    """
    
    config = PORTDIR + port + "/config.json"
    
    def get_port_exists() -> bool:
        port_dir = PORTDIR + port
        
        return os.path.isdir(port_dir)
    
    if not get_port_exists():
        port_info = {
            "name": "uknown"
        }
        return port_info
    
    with open(config) as f:
        data = json.load(f)
    
    return data

class check:
    def exists_fs(self, port):
        port_dir = PORTDIR + port
        
        config = port_dir + "/config.json"
        resources = port_dir + "/resources.json"
        install = port_dir + "/install"
        files = port_dir + "/files.list"
        
        if not os.path.isdir(port_dir):
            cdf.msg().error(f"Port '{port}' not found!")
            data = {
                "port": "not found",
                "exist": "not exist",
                "not_exist": "not exist"
            }
            
            return data
        
        f_error = []
        f_exist = []

        for file in config, resources, install, files:
            if os.path.isfile(file):
                f_exist.append(file)
            else:
                f_error.append(file)
        
        data = {
            "port": "found",
            "exist": f_exist,
            "not_exist": f_error
        }
        
        return data
        
    def exists_db(self, port):
        """
        Method for checking the presense of a port in the blacklist. If the
        package is present, it returns 'True', if it is absent, it returns
        'False'
        """
        db = cursor.execute(f"SELECT * FROM ports WHERE port = '{port}'")
        
        if db.fetchone() is None:
            return False
        else:
            return True

def check_priority(port: str):
    # TODO: DEPRECATED
    config = PORTDIR + port + "/config.json"
    port_dir = PORTDIR + port

    if not os.path.isdir(port_dir):
        cdf.msg().error(f"Port '{port}': not found!")
        return False
    
    if cpI.get(config).priority() == "system":
        cdf.msg().error("It is impossible to use the blacklist: the port has a system priority.")
        return False
    else:
        return True

def add(port: str):
    if not check_priority(port):
        return False
    
    data = [port, time.ctime()]

    try:
        cursor.execute("INSERT INTO ports VALUES (?,?)", data)
        conn.commit()

        return True

    except sqlite3.DatabaseError as error:
        cdf.msg().error(f"SQLite3 Database error: {error}")
        return False

def remove(port: str):
    data = f"DELETE FROM ports WHERE port = '{port}'"

    try:
        cursor.execute(data)
        conn.commit()
        
        return True

    except sqlite3.DatabaseError as error:
        cdf.msg().error(f"SQLite3 Database error: {error}")
        return False
