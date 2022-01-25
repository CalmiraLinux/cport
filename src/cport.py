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

import libcport
import cp_info       as cpI
import cp_blacklists as cpb
import cp_default    as cdf
import argparse

parser = argparse.ArgumentParser(
    description="Utility for building and installing the ports"
)

######################################################################

parser.add_argument(
    "--remove", "-r", type=str, dest="remove", nargs="+",
    help="Remove the port package from system"
)

parser.add_argument(
    "--info", "-I", type=str, dest="info",
    help="Get information about port package"
)

parser.add_argument(
    "--update", type=str, help="Update the port system"
)

parser.add_argument(
    "-v", "--version", dest="version",
    action="store_true", help="Get information about cport version"
)

subparser = parser.add_subparsers()

### START INSTALL ###
install = subparser.add_parser("install")

install.add_argument("--package", "-p", type=str, dest="inst",
    nargs="+", help="Build and install the port package"
)

install.add_argument(
    "--flags", "-f", dest="flags", type=str,
    help="Using compiler flags and cmd arguments"
)

### END INSTALL ###

### START BLACKLIST ###

blacklist = subparser.add_parser("blacklist")

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
    help="Check the presence of the port in the blacklist"
)

### END BLACKLIST ###

args = parser.parse_args()

def ver():
    msg = "cport " + cdf.VERSION + " - utility for building and installing the ports\n"
    print(msg)
    print("Copyright (C) 2021, 2022 Michail Linuxoid85 Krasnov <linuxoid85@gmail.com>")

def cmd_parser():
    if args.inst:
        if not libcport.getgid(0):
            cdf.log.error_msg("Error: you must run 'cport' as root!")
            exit(1)
        
        for port in args.inst:
            if args.flags:
                print(args.flags)
                if not libcport.install(port, flags=args.flags):
                    exit(1)
            else:
                print("Start building...")
                if not libcport.install(port):
                    exit(1)
            
            if len(args.inst) > 1:
                sep = 80 * '-'
                print(sep)
    
    elif args.remove:
        if not libcport.getgid(0):
            cdf.log.error_msg("Error: you must run 'cport' as root!")
            exit(1)
        
        for port in args.remove:
            if not libcport.remove(port):
                exit(1)

            if len(args.remove) > 1:
                sep = 80 * '-'
                print(sep)
    
    elif args.info:
        config = cdf.PORTDIR + args.info + "/config.json"
        if not cpI.info.port(config):
            exit(1)
    
    elif args.fs_find:
        print("Этот кусок кода, конечно, должен работать, но из-за разработчиков Python и прочих он не работает.")
        libcport.find(args.find_fs).filesystem()

    elif args.add_blacklist:
        if not libcport.getgid(0):
            cdf.log.error_msg("Error: you must run 'cport' as root!")
            exit(1)
        
        if not cpb.add(args.add_blacklist):
            exit(1)
    
    elif args.remove_blacklist:
        if not libcport.getgid(0):
            cdf.log.error_msg("Error: you must run 'cport' as root!")
            exit(1)
        
        if not cpb.remove(args.remove_blacklist):
            exit(1)
    
    elif args.fetch_blacklist:
        if not libcport.getgid(0):
            cdf.log.error_msg("Error: you must run 'cport' as root!")
            exit(1)
        
        if cpb.fetch(args.fetch_blacklist):
            print(f"\033[1m{args.fetch_blacklist}:\033[0m true")
            exit(0)
        else:
            print(f"\033[1m{args.fetch_blacklist}:\033[0m false")
            exit(1)

    elif args.version:
        ver()
    
    else:
        cdf.log.error_msg("You must input an arguments!")
        exit(1)

try:
    cmd_parser()
except KeyboardInterrupt:
    cdf.log.error_msg("Keyboard interrupt!")

    os.system("killall install")
    exit(1)
except SystemExit:
    cdf.log.error_msg("An incorrigible error occurred during the build/remove!")
    exit(1)
#except:
    #cdf.log.error_msg("Uknown error!")
    #exit(1)