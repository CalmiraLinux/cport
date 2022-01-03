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
import sys
import json
import time
import wget
import tarfile
import subprocess
import cp_info       as cpI
import cp_default    as cdf
import cp_blacklists as cpb

PORTDIR = cdf.PORTDIR
LOG     = cdf.LOG

def calc_sbu(func):
    def wrapper(*args, **kwargs):
        time_def   = float(cdf.settings.get("base", "sbu"))
        time_start = float(time.time())

        return_value = func(*args, **kwargs)
        time_end     = float(time.time())

        difference   = time_end - time_start # Building time (secs)

        sbu = difference / time_def # Calculate Standrt Build Unit for port
        print(f"Build time (sbu) = {round(sbu, 2)}") # Rounding the sbu value to hundredths and print result
        
        return return_value

    return wrapper

class install(object):

    def __init__(self, port, flags="default"):
        self.port    = port
        self.flags   = flags

        port_dir     = PORTDIR  + port
        port_install = port_dir + "/install"
        port_config  = port_dir + "/config.json"
        port_resources = port_dir + "/resources.conf"

        res = cdf.settings.get_json(port_resources)
        d_link = res["resources"]["url"]
        d_archive = res["resources"]["file"]

        cdf.log.msg(f"Starting building a port '{port}'...")

        if cdf.check.install(port_dir) and cpb.check_bl(port):
            if cpI.get.priority(port_config) == "system":
                cdf.log.warning(
                    f"Port '{port}': system priority. system priority. Subsequent port deletion is not possible."
                )

                cdf.dialog(p_exit=True)
                
            else:
                # ==begin
                # Проверка на совместимость порта с текущим
                # релизом Calmira GNU/Linux
                if not cdf.check.release(port_config):
                    cdf.log.error_msg(f"Port '{port}' не совместим с текущим релизом Calmira!")
                    cdf.dialog(p_exit=True)
                # ==end
                
                cdf.log.msg("Base info:")
                cpI.info.port(port_config)
                
                cdf.log.msg("Depends:", prev="\n")
                cpI.info.depends([port_config])

                cdf.dialog(p_exit=True)

            cdf.log.log_msg(
                f"Starting building port '{port}' using the '{flags}' flags...", level="INFO"
            )
            if install.download(d_link, cdf.CACHE) and install.unpack(d_archive, cdf.CACHE):
                install.build(port_install, flags)
        else:
            cdf.log.error_msg(f"Some errors while testing port files!")
    
    def download(link, dest):
        """
        Function for download a port files

        Usage:
        download(link, dest)

        - 'link' - download url;
        - 'dest' - destination file.
        """

        if os.path.isfile(dest):
            os.remove(dest)
        
        try:
            wget.download(link, dest)
            return True

        except ConnectionError:
            cdf.log.error_msg(f"Connection error while downloading '{link}'!")
            return False

        except:
            cdf.log.error_msg(f"Uknown error while downloading '{link}'!")
            return False
    
    def unpack(file, dest):
        """
        Function for unpack a tar archives

        Usage:
        unpack(file, dest)

        - 'file' - archive file;
        - 'dest' - destination file.
        """

        if not os.path.isfile(file):
            cdf.log.error_msg(f"File '{file}' not found!")
            return False
        
        try:
            t = tarfile.open(file, 'r')
            t.extractall(path=dest)

            return True
        
        except tarfile.ReadError:
            cdf.log.error_msg(f"Package '{file}' read error! Perhaps he is broken.")
            return False
        
        except tarfile.CompressionError:
            cdf.log.error_msg(f"Package '{file}' unpacking error! The format isn't supported.")
            return False
        
        except:
            cdf.log.error_msg(f"Uknown error while unpacking '{file}'!")
            return False

    @calc_sbu
    def build(install, flags=""):
        cdf.log.msg("Executing a build script...", prev="\n")
        command = f"{install} {flags}"

        run = subprocess.run(command, shell=True)

        if run.returncode != 0:
            cdf.log.error_msg(
                "\aPort returned a non-zero return code!", prev="\n\n"
            )

        else:
            cdf.log.ok_msg("\aBuild complete!", prev="\n\n")
        
        return run.returncode