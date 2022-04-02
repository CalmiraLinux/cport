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

    db     = cdf.DB
    conn   = sqlite3.connect(db)
    cursor = conn.cursor()
except ImportError:
    cdf.msg().error_trace(
        f"It is not possible to use the cp_remove kernel module: the" \
        " 'sqlite3' package doesn't installed",
        "cp_remove kernel module"
    )
    raise cdf.KernelModuleImportError

PORTDIR = cdf.PORTDIR
LOG = cdf.LOG

class prepare():
    
    def check_in_db(self, port):
        data = f"SELECT * FROM ports WHERE name = '{port}'"
        db = cursor.execute(data)

        if db.fetchone() is None:
            return False
        else:
            return True
    
    def get_files(self, port) -> list:
        port_dir = PORTDIR + port
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
    - 'remove_from_db()' - remove from database
    """

    def remove(self, port):
        files = prepare().get_files(port)
        error_files = []
        v_error = False

        for file in files:
            cdf.log(f"Start removing a file '{file}'...", level="INFO")
            
            try:
                if os.path.isfile(file):
                    os.remove(file)
                else:
                    shutil.rmtree(file)
            
            except FileNotFoundError:
                message = f"File '{file}' not found!"
                
                cdf.log(message, level="FAIL")
                cdf.msg().error(message)

                error_files.append(file)
                v_error = True
            
            except PermissionError:
                message = f"Permission denied while removing a file '{file}'"

                cdf.log(message, level="FAIL")
                cdf.msg().error(message)

                error_files.append(file)
                v_error = True
        
        if v_error:
            cdf.msg().error(f"Some errors while deleting {len(error_files)} files!")
            return False

        else:
            cdf.msg().ok(f"{len(files)} successfully deleted!")
            return True
    
    def remove_from_db(self, port):
        """
        Removing ports from database
        """

        data = f"DELETE FROM ports WHERE name = '{port}'"

        try:
            cursor.execute(data)
            conn.commit()

            return True
        except sqlite3.DatabaseError as error:
            cdf.msg().error(f"SQLite3 error: {error}")
            return False
