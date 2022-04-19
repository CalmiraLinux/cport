#!/usr/bin/python3

"""
Модуль, содержащий функции для установки порта в систему.

Константы и глобальные переменные:
    - API_SETTINGS - настройки API;
    - CALMIRA - информация о дистрибутиве Calmira GNU/Linux(-libre);
    - CACHE_DOWNLOADED - директория со скачанными архивами пакетов;
    - CACHE_UNPACKED - директория с распакованным архивом пакета;
    - DATABASE_MASTER - основная база данных cport;

Классы и методы:
    - prepare() - подготовка к установке (скачивание и распаковка файлов,
      базовые проверки);
    - build() - установка порта;

Структура базы данных:
    - 'packages_installed.db':
    | name | version | maintainer | architecture | priority | url | build_date |
    |------|---------|------------|--------------|----------|-----|------------|

    name - имя порта (например, 'base/editors/vim')
    version - версия порта
    maintainer - сопровождающий этот порт
    architecture - архитектура(ы), для которых предназначен порт
    priority - приоритет порта (пользовательский, системный)
    url - ссылка на репозиторий/файловое хранилище, откуда был скачан архив с
          исходным кодом пакета
    build_date - дата и время начала и окончания сборки
"""

import cp_default as cdf
import cp_info as cpI

import os
import shutil
import json
import wget
import tarfile
import subprocess
import sqlite3
import time
import hashlib

API_SETTINGS = cdf.API_SETTINGS
CALMIRA = cdf.CALMIRA
CACHE_DOWNLOADED = cdf.CACHE_DOWNLOADED
CACHE_UNPACKED = cdf.CACHE_UNPACKED
DATABASE_MASTER = cdf.DATABASE_MASTER

class prepare():

    def __init__(self, port_name: str):
        self.port_name = port_name
        self.port_info = cpI.port(port_name).info_param()

    def refresh_cache(self):
        for _dir in CACHE_DOWNLOADED, CACHE_UNPACKED:
            shutil.rmtree(_dir)
            os.makedirs(_dir)

    def check_disk_usage(self) -> bool:
        api_settings = cdf.parser().get(API_SETTINGS)
        minimal_disk_usage_free = float(
            api_settings['build']['mininal_disk_usage_free']
        )

        port_usage = float(self.port_info['package']['usage']) # Mb

        disk_usage_all = shutil.disk_usage('/')
        disk_usage_free = float(disk_usage_all[2])

        for i in range(2):
            disk_usage_free = disk_usage_free / 1024

        # The allowable use of disk space by the package is
        # calculated using the formula:
        # disk usage by the package (megabytes) + 10 megabytes
        acceptable_usage_free = port_usage + 10

        # In addition, the amount of data occupied by the package
        # is subtracted from the free disk space. If the result
        # value is less than 100, then this is unacceptable.
        if (disk_usage_free - acceptable_usage_free) < minimal_disk_usage_free:
            return False
        return True

    def check_release(self) -> bool:
        port_compat_rel = self.port_info['package']['release']

        calm_rel_info = cdf.parser().get(CALMIRA)
        calm_rel_number = calm_rel_info['system']['version']

        return calm_rel_number in port_compat_rel

    def download(self):
        port_url = self.port_info['port']['url']

        filename = wget.download(port_url, out = CACHE_DOWNLOADED)
        return filename

    def check_md5_hash(self) -> bool:
        filename = f"{CACHE_DOWNLOADED}/{port_conf_data['port']['file']}"
        md5_conf = self.port_info['port']['md5']

        if not os.path.isfile(filename):
            return False

        with open(filename, 'rb') as f:
            md5_file = hashlib.md5(f.read()).hexdigest()

        return md5_conf == md5_file

    def unpack(self):
        filename = self.port_info['port']['file']

        try:
            t = tarfile.open(filename, "r")
            t.extractall(path = CACHE_UNPACKED)
        except tarfile.ReadError:
            cdf.msg().error(f"Archive '{filename}': read error!")
            return False
        except tarfile.CompressionError:
            cdf.msg().error(f"Archive '{filename}': compression error!")
            return False
        except tarfile.ExtractError:
            cdf.msg().error(f"Archive '{filename}': extract error!")
            return False
        finally:
            t.close()

        return True

class build:

    def __init__(self, port_name: str):
        self.port_name = port_name
        
        port_info_func = cpI.port(port_name)
        self.port_path = port_info_func.path()
        self.port_info = port_info_func.info_param()

        self.conn = sqlite3.connect(DATABASE_MASTER)
        self.cursor = conn.cursor()

    def _create_table(self):
        # NOTE: only for initial startup!
        return self.cursor.execute("""CREATE TABLE IF NOT EXISTS ports(
            name TEXT,
            version TEXT,
            maintainer TEXT,
            architecture TEXT,
            priority TEXT,
            url TEXT,
            build_date TEXT);
        """)

    def build(self):
        port_build = f"{self.port_path}/install"
        build_time = []

        build_time.append(time.ctime())
        run = subprocess.run(port_build, shell = True)
        build_time.append(time.ctime())

        data = {
            "build_return_code": run.returncode,
            "build_time": build_time
        }
        return data

    def add_in_db(self):
        port_conf = self.port_info['package']

        port_data = (
            port_conf['name'], port_conf['version'], port_conf['maintainer'],
            port_conf['architecture'], port_conf['priority'],
            self.port_info['port']['url'], f"{time.ctime()}"
        )

        self.cursor.execute(
            "INSERT INTO ports VALUES(?, ?, ?, ?, ?, ?, ?)",
            port_data
        )
        self.conn.commit()
