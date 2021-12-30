#!/usr/bin/python3
#
# CPort - a new port manager for Calmira Linux
# Copyright (C) 2021 Michail Krasnov <linuxoid85@gmail.com>
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
import json
import cp_default as cdf

base_info  = [
    "name", "version", "description",
    "priority", "maintainer", "deps"
]

deps_info  = [
    "required", "optional", "recommend",
    "before", "conflict"
]

files_info = [
    "bins", "libs", "dirs"
]

class get(object):
    # TODO: добавить функцию 'port()' для проверки на существование порта
    # TODO: добавить функцию 'port_files()' для получения списка файлов порта
    def param(config, conf_param):
        if not os.path.isfile(config):
            cdf.log.error_msg(f"File '{config}': not found!")
            exit(1)
        
        try:
            f = open(config)
            data = json.load(f)
        except KeyError:
            cdf.log.error_msg(f"File '{config}: file is not config!")
            exit(1)
        
        try:
            prm = data[conf_param]
        except:
            prm = "not found"
        
        f.close()
        return prm
    
class info(object):
    def depends(configs: list):
        for config in configs:
            for param in deps_info:
                print(f"{param}: {get.param(config, param)}")
    
    def files(configs: list):
        for config in configs:
            for param in files_info:
                print(f"{param}: {get.param(config, param)}")
    
    def port(config):
        for param in base_info:
            print(f"{param}: {get.param(config, param)}")