#!/usr/bin/python3
# Скрипт для автоматизированной сборки ПО из системы портов
# (C) 2021 Michail Linuxoid85 Krasnov <linuxoid85@gmail.com>
# For CalmiraLinux 2.0

import os
import sys
import json
import time
import subprocess
import argparse
import cport_def as cdf

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
            cdf.log.log_msg(f"Starting building port {port} using the '{flags}' flags...")
            install.build(port_install, flags)

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
            cdf.log.error_msg("Port returned a non-zero return code!", prev="\n\n")
        else:
            cdf.log.ok_msg("Build complete!", prev="\n\n")

##############################################################################################################
#------------------------------------------------------------------------------------------------------------#
##############################################################################################################

parser = argparse.ArgumentParser(description="Utility for building and installing the port")

parser.add_argument("-u", "--update", action="store_true", dest='update',
    help="Update the installed port instead of its \"clean\" installation")

parser.add_argument(
    "-n", "--name", dest="port", type=str, required=True, nargs="+",
    help="Pass the program the name of the port to install"
)

parser.add_argument(
    "-f", "--flags", dest="flags", type=str,
    help="[EXPERIMENT] - using compiler flags"
)

args = parser.parse_args()

try:
    for port in args.port:
        if args.flags:
            install(port, flags=args.flags)
        else:
            install(port)
                    
        if len(args.port) > 1:
            sep = 80 * '-'
            print(sep)
    
except KeyboardInterrupt:
    cdf.log.error_msg("Keyboard Interrupt!")
except:
    cdf.log.error_msg(f"Install port '{args.port}': Uknown error!")