#!/usr/bin/python3
#
# CPort - a new port manager for Calmira Linux
# Copyright (C) 2021 Michail Krasnov <linuxoid85@gmail.com>
#
# main.py
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

#==================================================================#
#
# LOAD SCRIPT CONFIGURATIONS
#

import cp_remove as cpr
import cp_install as cpi
import cp_info as cpI
import cp_default as cdf
import argparse

parser = argparse.ArgumentParser(
    description="Utility for building and installing the port"
)

parser.add_argument(
    "--install", "-i", type=str, dest="install", nargs="+",
    help="Build and install the port package"
)

parser.add_argument(
    "--remove", "-r", type=str, dest="remove", nargs="+",
    help="Remove the port package from system"
)

parser.add_argument(
    "-f", "--flags", dest="flags", type=str,
    help="[EXPERIMENT] - using compiler flags"
)

parser.add_argument(
    "--info", "-I", type=str, dest="info",
    help="Get information about port package"
)

args = parser.parse_args()

def main():
    if args.install:
        for port in args.install:
            if args.flags:
                cpi.install(port, flags=args.flags)
            else:
                cpi.install(port)
            
            if len(args.install) > 1:
                sep = 80 * '-'
                print(sep)
    
    elif args.remove:
        for port in args.remove:
            if not cpr.remove(port):
                exit(1)

            if len(args.remove) > 1:
                sep = 80 * '-'
                print(sep)
    
    elif args.info:
        config = cdf.PORTDIR + args.info + "/config.json"
        cpI.info.port(config)

try:
    main()
except KeyboardInterrupt:
    cdf.log.error_msg("Keyboard interrupt!")
    exit(1)
except SystemExit:
    cdf.log.error_msg("An incorrigible error occurred during the build/remove!")
    exit(1)
except:
    cdf.log.error_msg("Uknown error!")
    exit(1)