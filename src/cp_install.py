#!/usr/bin/python3
#
# CPort - a new port manager for Calmira Linux
# Copyright (C) 2021 Michail Krasnov <linuxoid85@gmail.com>
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
import sys
import json
import subprocess
import cp_default as cdf

PORTDIR = cdf.PORTDIR
LOG     = cdf.LOG

class install(object):
    def __init__(self, port, flags="default"):
        self.port    = port
        self.flags   = flags

        port_dir     = PORTDIR  + port
        port_install = port_dir + "/install"
        port_config  = port_dir + "/config.json"

        cdf.log.msg(f"Starting building a port '{port}'...", prev="\n")

        if cdf.check.install(port_dir) and install.print_info(port_config):
            cdf.dialog(p_exit=True)
            
            cdf.log.log_msg(
                f"Starting building port {port} using the '{flags}' flags..."
            )
            install.build(port_install, flags)

        else:
            cdf.log.error_msg(f"Some errors while testing port files!")
            exit(1)

    def print_info(config):
        values = [
            "name", "version", "maintainer",
            "release", "priority"
        ]

        try:
            f = open(config, 'r')
            data = json.load(f)
        except FileNotFoundError:
            cdf.log.error_msg(f"File {config} doesn't exits!")
            return False
        except KeyError:
            cdf.log.error_msg(f"File {config} is not config!")
            return False
        except:
            cdf.log.error_msg(f"Uknown error while parsing file {config}!")
            return False
        
        for value in values:
            try:
                print(f"{value}: {data[value]}")
            except KeyError:
                print(f"{value}: not found")
        
        return True

    def build(install, flags=""):
        cdf.log.msg("Executing a build script...", prev="\n")
        command = f"{install} " + flags

        run = subprocess.run(command, shell=True)

        if run.returncode != 0:
            cdf.log.error_msg(
                "Port returned a non-zero return code!", prev="\n\n"
            )
        else:
            cdf.log.ok_msg("Build complete!", prev="\n\n")
  
"""
class db(object):
    def add(config):
        if not os.path.isfile(config):
            cdf.log.error_msg(f"Error while adding port in database: file '{config}' not found!")
            exit(1)
"""
