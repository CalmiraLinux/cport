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

# TODO: добавить проверку на наличие удаляемого порта в 'installed.db'

import os
import shutil
import cp_default as cdf

try:
    import sqlite3

    db = cdf.DB + "/installed.db"

    conn = sqlite3.connect(db)
    cursor = conn.cursor()
except ImportError:
    cdf.log().error_msg(
        "It is not possible to use the cp_remove API Module: you must install the 'sqlite3' port and rebuild the 'base/python' port."
    )
    exit(1)

PORTDIR = cdf.PORTDIR
LOG     = cdf.LOG

class prepare():
    
    """
    Some preparations before removing ports
    """

    def __init__(self, port):
        self.port = port

    def check_in_db(self):
        data = f"SELECT * FROM ports WHERE name = '{self.port}'"
        db = cursor.execute(data)

        if db.fetchone() is None:
            return False
        else:
            return True
    
    def get_files(self) -> list:
        port_dir = PORTDIR + self.port
        files_list = port_dir + "/files.list"

        files = [] # Files list

        with open(files_list, "r") as f:
            while True:
                line = f.readline()

                if not line:
                    break
                else:
                    files.append(f'{line.strip()}')
        
        return files

class remove():
        
    """
    Removing the ports from file system and database

    Methods:

    - 'remove()' - remove from file system;
    - 'remove_from_db()' - remove from 'installed.db' database
    """

    def __init__(self, port):
        self.port = port
    
    def remove(self):
        """
        Removing ports from filesystem
        """

        files = prepare(self.port).get_files()
        error_files = []
        v_error = False

        for file in files:
            cdf.log().log_msg(f"Start removing a file '{file}'...", level="INFO")
            
            try:
                os.remove(file)
                cdf.log().log_msg(f"File '{file}' deleted successfully", level=" OK ")
            
            except IsADirectoryError:
                shutil.rmtree(file)
                cdf.log().log_msg(f"Directory '{file}' deleted successfully", level=" OK ")
            
            except FileNotFoundError:
                message = f"File '{file}' not found!"
                
                cdf.log().log_msg(message, level="FAIL")
                cdf.log().error_msg(message)

                error_files.append(file)
                v_error = True
            
            except PermissionError:
                message = f"Permission denied while removing a file '{file}'"

                cdf.log().log_msg(message, level="FAIL")
                cdf.log().error_msg(message)

                error_files.append(file)
                v_error = True
        
        if v_error:
            cdf.log().error_msg(f"Some errors while deleting {len(error_files)} files!")
            cdf.log().error_msg(f"See the '{LOG}' file for get more info.")
            return False

        else:
            cdf.log().msg(f"{len(files)} successfully deleted!")
            return True
    
    def remove_from_db(self):
        """
        Removing ports from database
        """

        data = f"DELETE FROM ports WHERE name = '{self.port}'"

        try:
            cursor.execute(data)
            conn.commit()

            return True
        except sqlite3.DatabaseError as error:
            cdf.log().error_msg(f"SQLite3 error: {error}")
            return False