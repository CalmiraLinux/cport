#!/usr/bin/python3
#
# CPort - a new port manager for Calmira Linux
# Copyright (C) 2021, 2022 Michail Krasnov <linuxoid85@gmail.com>
#
# cp_update.py
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
import json
import subprocess
import cp_default as cdf

BRANCH = cdf.settings.get("repors", "url", source=cdf.SOURCES) + cdf.settings.get("repos", "branch", source=cdf.SOURCES)

METADATA      = BRANCH + "/metadata.json"           # Link to download the metadata
METADATA_INST = "/usr/share/cport/metadata.json"    # Installed metadata file
METADATA_TMP  = "/tmp/metadata.json"                # Temp downloaded metadata file

PORTS         = BRANCH + "/ports.txz"               # Link to download the ports archive
PORTS_INST    = "/usr/ports"                        # Installed ports package
PORTS_TMP     = "/tmp/ports.txz"                    # Temp downloaded ports archive

class check(object):
    """
    Check updates
    """

    def get_update_number(metadata) -> int:
        if not os.path.isfile(metadata):
            raise FileNotFoundError
        
        f = open(metadata)
        data = json.load(f)
        update_number = data["update_number"]
        f.close()

        return int(update_number)
    
    def updates(metadata=METADATA_TMP) -> int:
        """
        Return codes:
        0  - updates not found;
        1  - found updates;
        -1 - downgrade
        """

        updt_num_inst  = check.get_update_number(METADATA_INST) # Update number from installed metadata
        updt_num_dwnld = check.get_update_number(metadata)      # Update number from downloaded metadata

        difference     = updt_num_dwnld - updt_num_inst

        if difference == 0:
            return 0
        elif difference < 0:
            return -1
        else:
            return 1

class get(object):

    def changelog():
        link = BRANCH + "/CHANGELOG.md"
        pager = cdf.settings.get("base", "pager")
        
        try:
            wget.download(link, "/tmp/CHANGELOG.md")

            command = pager + " /tmp/CHANGELOG.md"
            run     = subprocess.run(command, shell=True)

            return run.returncode

        except:
            return 1

    def get_metadata(branch, dest=METADATA_TMP):
        try:
            if os.path.isfile(dest):
                os.remove(dest)
            
            wget.download(METADATA, dest)
            return True
        except:
            return False
    
    def port(branch, dest=PORTS_TMP):
        try:
            if os.path.isfile(dest):
                os.remove(dest)
            
            wget.download(PORTS, dest)
            return True
        except:
            return False

    def diff(metadata):
        if not os.path.isfile(metadata):
            raise FileNotFoundError
        
        f = open(metadata)
        data = json.load(f)

        for param in "updates", "addings", "removes":
            try:
                print(f"\033[1m{param}\033[0m:", end=" ")
                values = data[param]

                for value in values:
                    print(f"{value}", end=" ")
                print()
            except:
                print(f"\033[1m{param}\033[0m: not found")
        
        f.close()