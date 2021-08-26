#!/bin/python
#
# CPkg - an automated packaging tool for Calmira Linux
# Copyright (C) 2021 Michail Krasnov
#
# other-functions.py
#
# Project Page: http://github.com/Linuxoid85/cpkg
# Michail Krasnov <michail383krasnov@mail.ru>
#

import os
import json
from datetime import datetime

#==================================================================#
#
# BASE VARIABLES
#
NAME_FILE = "other-functions.py" 	# File name for log_msg

#==================================================================#
#
# BASE FUNCTIONS
#

# Print current date
def print_date_time():
	return datetime.fromtimestamp(1576280665)

# Write information in text file
def write_file(file, message):
	f = open(file, 'a')
	for index in message:
		f.write(index + '\n')
	f.close()

# Print message from text file
def print_text(text):
    fp = open(text, "r")
    print(*fp)

# Print text message on screen - console output
def print_msg(message, mode):
	if mode == "quiet":
		write_file("/dev/null", message)
	elif mode == "nonquiet" or mode == "default":
		print(message)
	else:
		print("ОШИБКА: нет опции {}!", mode)

# Print debug message on screen
def print_dbg_msg(message, mode):
    if mode == "debug":
        MSG = print_date_time() + message
        print(MSG)
    elif mode == "nondbg":
        write_file("/var/log/cpkg_dbg.log", message)
    else:
        print("ОШИБКА: нет опции{}!", mode)

# Scan information from keyboard
def dialog_msg():
    print("Продолжить (Y/n)?", end=" ")
    RUN = input()

    if RUN == "y" or RUN == "Y":
        print_dbg_msg("Continue", "nondbg")
    elif RUN == "n" or RUN == "N":
        print_msg("Canselled!", "default")
    else:
        print_msg("ОШИБКА: аргумента {} не существует!", RUN)
        sys.exit(1)

# Check dirs after cpkg start
def check_file():
    for DIR in '/var/cache', '/var/cache/db', '/var/cache/db/cpkg', '/var/cache/cpkg/archives', '/var/db/cpkg', '/var/db/cpkg/packages', '/etc/cpkg':
        CHECK = "check dir '" + DIR + "' ..."
        print_dbg_msg(CHECK, "nonquiet")

        if os.path.isdir(DIR):
            print_dbg_msg("done", "debug")
        else:
            print("Ошибка: директории {} не существует!", DIR)
            dialog_msg()

# Function for write logs in log file
def log_msg(message, result):
    f = open("/var/log/cpkg.log", "a")
    for index in message:
        f.write(index + '\n')

# Function for get version of Calmira
def GetCalmiraVersion(mode):
    sysData = "/etc/calm-version"

    if os.path.isfile(sysData):
        print_dbg_msg("sysData file is OK", "nondbg")
    else:
        print("Ошибка: файла '/etc/calm-version' не существует, либо нет доступа для его чтения.")
        exit(1)

    with open(sysData, "r") as f:
        systemData = json.loads(f.read())

        if mode == "all":
            print("Имя: \t{}", systemData["distroName"])
            print("Версия: \t{}", systemData["distroVersion"])
            print("Кодовое имя: \t{}", systemData["distroCodename"])
        elif mode == "compact":
            return systemData["distroVersion"]
