#!/usr/bin/python3

"""
Модуль с функциями для удаления портов

Константы и глобальные переменные:

"""

import cp_default as cdf
import cp_info as cpI

import os
import shutil

API_SETTINGS = cdf.API_SETTINGS
CALMIRA = cdf.CALMIRA
CACHE_DOWNLOADED = cdf.CACHE_DOWNLOADED
CACHE_UNPACKED = cdf.CACHE_UNPACKED
DATABASE_MASTER = cdf.DATABASE_MASTER

class prepare(cpI.database):

    def check_priority(self, port_name: str) -> str:
        port_config_data = cpI.port().info_param(port_name)

        return port_config_data['package']['priority']

class remove:

    def __init__(self, port_name: str):
        self.port_name = port_name

        self.conn = sqlite3.connect(DATABASE_MASTER)
        self.cursor = conn.cursor()

    def remove(self) -> bool:
        port_path = cpI.port().path(self.port_name)
        port_remove_file = f"{port_path}/files.list"
        port_remove_list = port_remove_file.split(sep='\n')
        
        ok_list = []
        error_list = []
        errors = False
        
        for file in port_remove_list:
            try:
                if os.path.isfile(file):
                    os.remove(file)
                else:
                    shutil.rmtree(file)
                ok_list.append(file)
            except FileNotFoundError:
                error_list.append(file)
                errors = True

        data = {
            "succesfull_deletion": not errors,
            "ok_files": ok_list,
            "error_list": error_list
        }

        return data
