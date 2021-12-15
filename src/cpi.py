#!/usr/bin/python3
# Скрипт для автоматизированной сборки ПО из системы портов
# (C) 2021 Michail Linuxoid85 Krasnov <linuxoid85@gmail.com>
# For CalmiraLinux 2.0

import os
import sys
import json
import time
import subprocess
import cport_def as cdf

PORTDIR = cdf.PORTDIR
LOG     = cdf.LOG

class install(object):
    def __init__(self, port):
        self.port = port
        port_dir     = PORTDIR  + port
        port_install = port_dir + "/install"
        port_config  = port_dir + "/config.json"

        if cdf.check.install(port_dir) and install.print_info(port_config):
            cdf.log.log_msg(f"Starting building port {port}...")
            install.build(port_install)

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

    def build(install):
        run = subprocess.run(install, shell=True)
        if run.returncode != 0:
            cdf.log.error_msg("Port returned a non-zero return code!", prev="\n\n")
        else:
            cdf.log.ok_msg("Build complete!", prev="\n\n")

try:
    port = sys.argv[1]
    install(port)
    
except KeyboardInterrupt:
    cdf.log.error_msg("Keyboard Interrupt!")
except IndexError:
    cdf.log.error_msg("You must input 1 argument!")
    exit(1)