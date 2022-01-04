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
import subprocess
import cp_info    as cpI
import cp_default as cdf
import cp_blacklists as cpb

PORTDIR = cdf.PORTDIR
LOG     = cdf.LOG

class remove(object):

    def __init__(self, port):
        self.port = port

        port_dir = PORTDIR + port
        port_config = [port_dir+"/config.json"]
        conf        = port_dir + "/config.json"
        port_remove = port_dir + "/remove"

        cdf.log.msg(f"Start removing a port '{port}'...")

        if cdf.check.remove(port_dir) and cpb.check_bl(port):
            if cpI.get.priority(conf) == "system":
                cdf.log.error_msg(f"Port '{port}': system priority. Deleting the port is not possible.")
                exit(1)
            
            cdf.log.msg("Base info:")
            cpI.info.port(conf)

            cdf.log.msg("Depends:", prev="\n")
            cpI.info.depends(port_config)

            cdf.dialog(p_exit=True)

            cdf.log.log_msg(f"Start removing port '{port}'...", level="INFO")

            remove.remove_pkg(port_remove)
        else:
            exit(1)

    def remove_pkg(port_remove):
        cdf.log.msg("Executing a remove script...", prev="\n")
        run = subprocess.run(port_remove, shell=True)

        if run.returncode != 0:
            cdf.log.error_msg(
                "Port returned a non-zero return code!", prev="\n\n"
            )
            cdf.log.error_msg("Port returned a non-zero return code!", level="FAIL")
            return False
        else:
            cdf.log.ok_msg("Remove complete!", prev="\n\n")
            return True
