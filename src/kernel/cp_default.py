#!/usr/bin/python3

import os
import json
import time
import configparser
import cp_exceptions as cpe

VERSION   = "v1.0a3"

LOG_DIR   = "/var/log/cport.d/"
LOG       = "/var/log/cport.log"
DB        = "/var/lib/cport.d/cport.db"
CACHE_DIR = "/var/cache/cport/"
CACHE_DATA_DIR = CACHE_DIR + "pkg"
PORT_DIR  = "/usr/ports/"

CALMIRA   = "/etc/calm-release"

def log(message, level="INFO"):
    """
    Usage:
    log(message, level)
    """

    message = f"[ {time.ctime()} ] [ {level} ] - {message}"

    with open(LOG, "a") as f:
        data = f.write(message)

class msg:

    def error(self, message, log_msg=False):
        print(f"\033[31m[!]\033[0m {message}")

        if log_msg:
            log(message, level="FAIL")

    def error_trace(self, message, function):
        print(
            "!!! ERROR TRACEBACK:\n",
            "\033[1mError:\033[0m \033[31m{message}\033[0m\n",
            "\033[1mFunction/class:\033[0m {function}\n",
            "\033[1mTime:\033[0m {time.time()} (UNIX), {time.ctime()} (human)",
            "\033[1meRepository:\033[0m https://github.com/CalmiraLinux/cport/"
        )

        log(message, level="TRACE")

    def ok(self, message, log_msg=False):
        print(f"\033[32m[+]\033[0m {message}")

        if log_msg:
            log(message, level=" OK ")

    def header(self, message):
        print(f"===> {message}")

    def sub_header(self, message):
        print(f"==> {message}")

    def sub_sub_header(self, message):
        print(f"-> {message}")

class PortError(Exception):
    """
    Какая-либо ошибка, связанная с портом
    """

class KernelModuleError(Exception):
    """
    Связанные с модулем ядра ошибки
    """

class KernelModuleImportError(Exception, KernelModuleError):
    """
    Ошибки, связанные с ImportError в модулях ядра
    """

class settings:
    # TODO: изменить алгоритм автоматического определения типа данных параметра
    # Не на основе суффикса названия параметра, а на основе префикса значения:
    # list:///, bool:/// intg:///

    def __init__(self):
        self.config = configparser.ConfigParse()

    def _get_type(self, tp: str):
        tp = f"{tp[0:7]}"

        match(tp):
            case "INTG:///":
                return int
            case "FLOT:///":
                return float
            case "BOOL:///":
                return bool
            case "LIST:///":
                return list
            case _:
                return str

    def get(self, config, section, param):
        conf = self.config(config)
        
        try:
            data = conf.get(section, param)
        except Error as err:
            msg().error_trace(
                    err, f"cdf.settings().get({config}, {section}, {param})"
            )
            return None

        get_type = self._get_type(param)

        _type = data[0:7]
        _types = ["INTG:///", "FLOT:///", "BOOL:///", "LIST:///"]

        if _type in _types:
            data = data[8:]
        
        return get_type(data)

    def set(self, config, section, param, value):
        conf = self.config(config)

        try:
            data = conf.set(section, param, value)
        except Error as err:
            msg().error_trace(
                err,
                f"cdf.settings().set({config}, {section}, {param}, {value}"
            )
            return None

        return data
