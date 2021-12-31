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
import cp_info       as cpI
import cp_default    as cdf
import cp_blacklists as cpb

PORTDIR = cdf.PORTDIR
LOG     = cdf.LOG

class install(object):

    def __init__(self, port, flags="default"):
        self.port    = port
        self.flags   = flags

        port_dir     = PORTDIR  + port
        port_install = port_dir + "/install"
        port_config  = port_dir + "/config.json"

        cdf.log.msg(f"Starting building a port '{port}'...")

        if cdf.check.install(port_dir) and cpb.check_bl(port):
            if cpI.get.priority(port_config) == "system":
                cdf.log.warning(f"Port '{port}': system priority. system priority. Subsequent port deletion is not possible.")
                cdf.dialog(p_exit=True)
                
            else:
                cdf.log.msg("Base info:")
                cpI.info.port(port_config)
                
                cdf.log.msg("Depends:", prev="\n")
                cpI.info.depends([port_config])

                cdf.dialog(p_exit=True)

            cdf.log.log_msg(
                f"Starting building port {port} using the '{flags}' flags...", level="INFO"
            )
            install.build(port_install, flags)
        else:
            cdf.log.error_msg(f"Some errors while testing port files!")

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
        
        return run.returncode