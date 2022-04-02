#!/usr/bin/python3
# Copyright (C) 2022 Michail Krasnov <linuxoid85@gmail.com>

import os
import json
import cp_default as cdf

PORT_DIR = cdf.PORT_DIR
CALMIRA = cdf.CALMIRA

class get:

    def _listdir(_dir) -> list:
        return os.listdir(_dir)

    def port_files(self, port: str) -> list:
        port = PORT_DIR + port

        if not os.path.isdir(port):
            return []

        base_cont = os.listdir(port)
        content = []

        for file in base_cont:
            file_path = f"{port}/{file}"

            if os.path.isfile(file_path):
                content.append(file_path)
            elif os.path.isdir(file_path):
                files = listdir(file_path)
                for file in files:
                    if os.path.isfile(file):
                        content.append(file)

        return content

    def port_info(self, port: str, section: str, param: str):
        port = PORT_DIR + port
        conf = f"{port}/config.ini"

        if not os.path.exists(conf):
            return None

        data = cdf.settings().get(conf, section, param)
        return data

class check(get):
    
    def port_compatible(self, port) -> bool:
        with open(CALMIRA) as f:
            clm_release = json.load(f)
        
        data = self.port_info(port, "release")
        compat = clm_release["distroVersion"] in data

        return compat

    def port_files(self, port) -> bool:
        req_files = ("build", "config.ini", "files.list")
        port = PORT_DIR + port
        v_files = True
        
        for file in req_files:
            file = f"{port}/{file}"
            if not os.path.isfile(file):
                v_files = False

        return v_files
