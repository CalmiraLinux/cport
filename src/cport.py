#!/usr/bin/python3
#
# CPort - a new port manager for Calmira Linux
# Copyright (C) 2021, 2022 Michail Krasnov <linuxoid85@gmail.com>
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

import os
import libcport
import cp_info       as cpI
import cp_blacklists as cpb
import cp_default    as cdf
import argparse

######################################################################

parser = argparse.ArgumentParser(
    description="Utility for building and installing the ports"
)

subparser = parser.add_subparsers()

######################################################################

### BEGIN 'install' SUBPARSER ###

install = subparser.add_parser(
    "install", help="Build and install the port package"
)

install.add_argument(
    "--port", "-p", type=str, dest="inst",
    nargs="+", help="Build and install the port package"
)

install.add_argument(
    "--yes", "-y", dest="yes_answer",
    action="store_true", help="Answering 'yes'"
)

install.set_defaults(func=libcport.inst_port)

### END 'install' SUBPARSER ###

### BEGIN 'remove' SUBPARSER ###

remove = subparser.add_parser(
    "remove", help="Remove the port package from system"
)

remove.add_argument(
    "--port", "-p", type=str, dest="remove", nargs="+",
    help="Remove the port package from system"
)

remove.add_argument(
    "--yes", "-y", dest="yes_answer",
    action="store_true", help="Answering 'yes'"
)

remove.set_defaults(func=libcport.remove)

### END 'remove' SUBPARSER ###

### BEGIN 'blacklist' SUBPARSER ###

blacklist = subparser.add_parser(
    "blacklist", help="Add and remove ports from blacklist"
)

blacklist.add_argument(
    "--add", "-a", dest="add_blacklist", type=str,
    help="Add a port in blacklist"
)

blacklist.add_argument(
    "--remove", "-r", dest="remove_blacklist", type=str,
    help="Remove a port from blacklist"
)

blacklist.add_argument(
    "--fetch", "-f", dest="fetch_blacklist", type=str,
    help="Check the presense of the port in the blacklist"
)

blacklist.set_defaults(func=libcport.blacklists)

### END 'blacklist' SUBPARSER ###

### BEGIN 'find' SUBPARSER ###

find = subparser.add_parser(
    "find", help="Find ports in metadata, database and filesystem"
)

find.add_argument(
    "--fs", "-f", dest="find_fs", type=str,
    help="Find ports in the filesystem"
)

find.add_argument(
    "--db", "-d", dest="find_db", type=str,
    help="Find ports in database"
)

find.add_argument(
    "--metadata", "--md", "-m", dest="find_md",
    type=str, help="Find ports in metadata"
)

find.set_defaults(func=libcport.find)

### END 'find' SUBPARSER ###

### BEGIN 'info' SUBPARSER ###

info = subparser.add_parser(
    "info", help="Get information about package"
)

info.add_argument(
    "--port", "-p", type=str, dest="info",
    help="Get information about package"
)

info.set_defaults(func=libcport.info)

### END 'info' SUBPARSER ###

### BEGIN 'version' SUBPARSER ###

version = subparser.add_parser(
    "ver", help="Get information about cport version"
)

version.add_argument(
    "--api", action="store_true", help="Get information about Ports API"
)

version.add_argument(
    "--program", action="store_true", help="Get information about cport"
)

version.add_argument(
    "--all", "-a", action="store_true", help="Get all information"
)

version.set_defaults(func=libcport.ver)

### END 'version' SUBPARSER ###

args = parser.parse_args()

try:
    args.func(args)
except KeyboardInterrupt:
    cdf.log().error_msg("Keyboard interrupt!")
    os.system("killall install 2> /dev/null")
    exit(1)
except SystemExit:
    cdf.log().error_msg("Uknown error while working Ports API!")
    os.system("killall install 2> /dev/null")
    exit(1)