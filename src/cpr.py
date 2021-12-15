#!/usr/bin/python3
# Скрипт для автоматизированного удаления ПО
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

class remove(object):
    def __init__(self, port):
        self.port = port

        port_dir = PORTDIR + port
        port_remove = port_dir + "/remove"

        if cdf.check.remove(port_dir):
            remove.remove_pkg(port_remove)
        else:
            exit(1)

    def remove_pkg(port_remove):
        run = subprocess.run(port_remove, shell=True)

        if run.returncode != 0:
            cdf.log.error_msg("Port returned a non-zero return code!", prev="\n\n")
        else:
            cdf.log.ok_msg("Remove complete!", prev="\n\n")

##############################################################################################################
#------------------------------------------------------------------------------------------------------------#
##############################################################################################################

parser = argparse.ArgumentParser(description="Utility for building and installing the port")

parser.add_argument(
    "-n", "--name", dest="port", type=str, required=True, nargs="+",
    help="Pass the program the name of the port to remove"
)

args = parser.parse_args()

try:
    for port in args.port:
        remove(port)
                    
        if len(args.port) > 1:
            sep = 80 * '-'
            print(sep)
    
except KeyboardInterrupt:
    cdf.log.error_msg("Keyboard Interrupt!")
except:
    cdf.log.error_msg(f"Install port '{args.port}': Uknown error!")