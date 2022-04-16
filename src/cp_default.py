#!/usr/bin/python3

"""
Модуль, содержащий общие функции для всех остальных модулей cp_*.py

Константы и глобальные переменные:
    - Порты:
        - PORT_DIR - директория с системой портов;
    - Для логирования:
        - LOG_DIR - директория с лог-файлами;
        - LOG_FILE_MASTER - master-файл, содержащий все сообщения;
        - LOG_FILE_API - файл, содержащий сообщения API;
    - Дистрибутиво-ориентированные данные:
        - CALMIRA - файл с информацией о Calmira GNU/Linux(-libre)

Классы и методы:
    - msg() - логирование, отправка сообщений в stdout и stderr:
        - log() - отправка сообщений в логи cport;
        - error() - отправка сообщений об ошибках программы в stderr;
        - error_trace() - отправка сообщений об ошибках в работе API в stderr;
        - status() - отправка сообщений о текущей операции в stdout;
    - parser() - парсинг конфигов формата TOML:
        - check() - проверка наличия конфигурационного файла;
        - get() - парсинг конфига и возвращение полученных из него данных;
"""

import os
import sys
import time
import toml # TODO: обновить после выхода Python 3.11

SETTINGS_DIR = "/etc/cport.d"
API_SETTINGS = f"{SETTINGS_DIR}/api.conf"

PORT_DIR = "/usr/ports"

LOG_DIR = "/var/log/cport.log.d"
LOG_FILE_MASTER = f"{LOG_DIR}/master.log"
LOG_FILE_API = f"{LOG_DIR}/api.log"

CALMIRA = "/etc/calm-release"

CACHE_DIR = "/var/cache/cport"
CACHE_DOWNLOADED = f"{CACHE_DIR}/archives"
CACHE_UNPACKED = f"{CACHE_DIR}/unpacked"

DB_DIR = "/var/lib/cport.d/db"
DBATABASE_MASTER = f"{DB_DIR}/master.db"

class msg:
    
    def log(self, msgs, status = "INFO", file = LOG_FILE_MASTER):
        with open(LOG_FILE, "a") as f:
            msg = f"[ {time.ctime()} ] [ {status} ] - {msg}"
            f.write(msg)

    def error(self, *messages, log = True):
        prefix = f"\033[31m[!]\033[0m"

        for msg in messages:
            print(f"{prefix} {msg}", file = sys.stderr)

            if log:
                self.log(msg, status = "FAIL")

    def error_trace(self, msg, func, return_code, log = True):
        print(
            "\033[31mAPI Error!\n\033[0m",
            "\033[1mmessage:\033[0m {msg}\n",
            "\033[1mobject:\033[0m {func}\n",
            "\033[1mreturned value:\033[0m {return_code}"
        )

        if log:
            msg1 = f"Error in function '{func}' (returned '{return_code}'):"
            msg2 = f"\t{msg}"

            self.log(msg1, file = LOG_FILE_API)
            self.log(msg2, file = LOG_FILE_API)

    def status(self, msg, log = True, center = False):
        if center:
            scr_msg = msg.center(os.get_terminal_size()[0] - 1, "=")
            print(scr_msg)
        else:
            print(f"==> {msg}")

        if log:
            self.log(msg, status = "INFO")

class parser:

    def check(self, file: str) -> bool:
        """
        Function for checking the presence of a TOML file

        Usage:
        check(file)

        | variable | data type |
        |----------|-----------|
        | 'file'   | str       |

        Return code: bool
        """

        return os.path.isfile(file)

    def get(self, file: str) -> dict:
        """
        Function for getting all parameters from a TOML file

        Usage:
        get(file)

        | variable | data type |
        |----------|-----------|
        | 'file'   | str       |

        Return code: dict
        Errors/exceptions:

            1. Config ('file' arg.) not found:
            {
                "request": None
            }

            2. Decode error (toml.TomlDecodeError exception):
            {
                "request": "TomlDecodeError"
            }

            3. FileNotFoundError (after calling the 'self.check()' function)/
               IOError/NameError:
            {
                "request": "FileNotFoundError/IOError/NameError"
            }
        """

        if not self.check(file):
            return {"request": None}

        try:
            data = toml.load(file)
        except toml.TomlDecodeError:
            data = {"request": "TomlDecodeError"}
        except toml.FNFError:
            data = {"request": "FileNotFoundError/IOError/NameError"}

        return data
