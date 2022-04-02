#!/usr/bin/python3
#
# CPort - a new port manager for Calmira Linux
# Copyright (C) 2021, 2022 Michail Krasnov <linuxoid85@gmail.com>
#
# cp_install.py
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
import wget
import time
import tarfile
import cp_default as cdf
import cp_info    as cpI

try:
    import sqlite3

    db     = cdf.DB
    conn   = sqlite3.connect(db)
    cursor = conn.cursor()
except ImportError:
    cdf.msg().error_trace(
        f"It is not possible to use the cp_install kernel module: the" \
        " 'sqlite3' package doesn't installed",
        "cp_install kernel module"
    )
    raise cdf.KernelModuleImportError

PORT_DIR  = cdf.PORT_DIR
CACHE_DIR = cdf.CACHE_DIR
CACHE_DATA_DIR = cdf.CACHE_DATA_DIR

class check():

    def filesystem(self, port) -> bool:
        # TODO: перенести в cp_default
        port = PORT_DIR + port
        return os.path.isdir(port)

class prepare():

    def check_in_db(self, port):
        data = "SELECT * FROM installed_ports WHERE name = (?)"
        _db = cursor.execute(data, (port,))

        return _db.fetchone() is None
    
    def download(self, port):
        url  = cpI.get().port_info(port, "port_management", "url")
        file = cpI.get().port_info(port, "port_management", "file")
        cache_file = f"{CACHE_DIR}{file}"

        if os.path.isfile(cache_file):
            os.remove(cache_file)

        try:
            wget.download(url, file)
            return True
        except Error as err:
            cdf.msg().error_trace(
                err,
                f"cpi.prepare.gownload({port})"
            )
            return False

    def unpack(self, port):
        file = cpI.get().port_info(port, "port_management", "file")
        cache_file = f"{CACHE_DIR}{file}"

        if not os.path.exists(cache_file):
            cdf.msg().error_trace(
                f"File '{cache_file}' not found!",
                f"cpi.prepare.unpack({port})"
            )
            return False

        if os.path.exists(CACHE_DATA_DIR):
            # Очистка директории, в которую будет распакован архив с исходным кодом
            os.removedirs(CACHE_DATA_DIR)
            # TODO: проверить на работоспособность
        os.makedirs(CACHE_DATA_DIR)

        try:
            with tarfile.open(cache_file) as t:
                t.extractall(path=CACHE_DATA_DIR)
            return True
        except Error as err:
            cdf.msg().error_trace(
                f"File '{cache_file}' not found!",
                f"cpi.prepare.unpack({port})"
            )
            return False

class build(prepare):

    def calc_time(self, func):
        def wrapper(*args, **kwargs):
            time_start = time.time()
            data = func(*args, **kwargs)
            time_end = time.time()

            diff = (time_end - time_start) / 189

            print(f"Build time: {diff} SBU")
            return func
        return wrapper
    
    @self.calc_time
    def build(self, port) -> int:
        port_config = PORT_DIR + port + "/config.ini"
        port_install = PORT_DIR + port + "/install"

        run = os.system(port_install)

        return run

    def add_in_db(self, port):
        """
        TODO: add a code
        """

        data = ""

        try:
            cursor.execute(data)
            conn.commit()

            return True
        except sqlite3.DatabaseError as error:
            cdf.msg().error_trace(
                error,
                f"cpi.build.add_in_db({port})"
            )
            return False
