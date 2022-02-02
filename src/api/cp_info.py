#!/usr/bin/python3
#
# CPort - a new port manager for Calmira Linux
# Copyright (C) 2021. 2022 Michail Krasnov <linuxoid85@gmail.com>
#
# cp_info.py
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
import cp_default    as cdf
import cp_blacklists as cpb

# base_info - base information about port
base_info  = [
    "name", "version", "description",
    "priority", "maintainer", "site",
    "slave", "size"
]

deps_info  = [
    "required", "optional", "recommend",
    "before", "conflict"
]

files_info = [
    "bins", "libs", "dirs"
]

class get():

    # TODO: добавить функцию 'port()' для проверки на существование порта
    # TODO: добавить функцию 'port_files()' для получения списка файлов порта

    def __init__(self, config):
        self.config = config
    
    def param(self, conf_param):
        if not os.path.isfile(self.config):
            cdf.log().error_msg(f"File '{self.config}': not found!")
            return False
        
        # TODO: заменить эту конструкцию на 'cdf.check.json_config()'
        try:
            with open(self.config) as f:
                data = json.load(f)
        except:
            cdf.log().error_msg(f"File '{self.config}: file is not config!")
            return False
        
        try:
            prm = data[conf_param]
        except KeyError:
            prm = "not found"
        
        return prm
    
    def param_dep(self, conf_param):
        if not os.path.isfile(self.config):
            cdf.log().error_msg(f"File '{self.config}': not found!")
            return False
        
        # TODO: заменить эту конструкцию на 'cdf.check.json_config()'
        try:
            with open(self.config) as f:
                data = json.load(f)
        except:
            cdf.log().error_msg(f"File '{self.config}: file is not config!")
            return False
        
        try:
            #not_deps = False
            prm = data['deps'][conf_param]

            param_list = ""
            for value in prm:
                param_list = param_list + f"'{value}' "

            return param_list
        except:
            f.close()
            return "not found"
    
    def priority(self):
        if not os.path.isfile(self.config):
            cdf.log().error_msg(f"File '{self.config}': not found!")
            return False
        
        # TODO: заменить эту конструкцию на 'cdf.check.json_config()'
        try:
            with open(self.config) as f:
                data = json.load(f)
        except:
            cdf.log().error_msg(f"File '{self.config}: file is not config!")
            return False

        prior = data["priority"]
        return str(prior)

class info():

    def __init__(self, config):
        self.config = config

    def description_port(self):
        with open(self.config) as f:
            data = json.load(f)
            desc = data["description"]

        return desc

    def depends(self):
        for param in deps_info:
            print(f"\033[1m{param}:\033[0m {get(self.config).param_dep(param)}")

        return 0
    
    def files(self):
        for param in files_info:
            print(f"\033[1m{param}:\033[0m {get(self.config).param(param)}")
    
    def port(self):
        for param in base_info:
            print(f"\033[1m{param}:\033[0m {get(self.config).param(param)}")
        
        # Get blacklist
        with open(self.config) as f:
            data = json.load(f)

        if cpb.fetch(data["name"]):
            print("\033[1mblacklist:\033[0m true")
        else:
            print("\033[1mblacklist:\033[0m false")

        return True