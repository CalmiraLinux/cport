#!/bin/python
#
# CPkg - an automated packaging tool for Calmira Linux
# Copyright (C) 2021 Michail Krasnov
#
# core-functions.sh
#
# Project Page: http://github.com/Linuxoid85/cpkg
# Michail Krasnov <michail383krasnov@mail.ru>
#

import tarfile
import json
import os
import platform
import other-functions
import shutil
from datetime import datetime
from subprocess import call

#==================================================================#
#
# BASE VARIABLES
#

VERSION = "v2.0" 				# cpkg version
GetArch = platform.processor()	# System arch
GetDate = other-functions.print_date_time() # System date
pkg_cache_dir = "/var/cache/cpkg/archives"
PACKAGE_CACHE = "/var/cache/cpkg/archives/PKG"
PACKAGE_CONFIG = PACKAGE_CACHE + "/config.json" # config.json
PREINSTALL = PACKAGE_CACHE + "/preinst.sh"
POSTINSTALL = PACKAGE_CACHE + "/postinst.sh"
VARDIR = "/var/db/cpkg" # Database dir
PORT = "false"

#==================================================================#
#
# PROGRAM FUNCTIONS
#


# List package depends
## Variables
# REQ_DEPS  - required depends
# TEST_DEPS - deps for test suite (only for port-packages)
# OPT_DEPS  - optional deps
# BEF_DEPS  - package may be installed before this depends
# from $BEF_DEPS variable
## Options
# list_depends install - for install_pkg function
# list_depends remove  - for remove_pkg function
# list_depends info    - for package_info function
def list_depends(package, mode):
	if mode == "install":
		PackageName = PACKAGE_CONFIG
	else:
		PackageName = VARDIR + '/packages/' + package + '/config.json'

	if os.path.isfile(PackageName):
		with open(PackageName, 'r') as f:
			packageData = json.load(f.read())

			print("Необходимые зависимости: ", packageData["deps"]["require"])
			print("Для тестирования: ", packageData["deps"]["test"])
			print("Опциональные: ", packageData["deps"]["optional"])
			print("Рекомендуемые: ", packageData["deps"]["recommend"])
			print("Runtime: ", packageData["deps"]["runtime"])
			print("Конфликтует с: ", packageData["deps"]["conflict"])
			print("Порт: ", packageData["port"])

		if mode == "install":
			print("Установите эти зависимости перед установкой исходного пакета {}!", package)
		elif mode == "remove":
			print("Удалите эти зависимости после удаления исходного пакета {}!", package)
		elif mode == "info":
			print("При удалении или переустановке пакета убедитесь, что зависимости удовлетворены!")
		else:
			print("Неправильное употребление функции 'list_depends'!")
			exit(1)

	else:
		print("Ошибка: пакета {} не существует!", package)
		exit(1)

# Function for check priority of package
# If priority = system, then package doesn't
# can remove from Calmira GNU/Linux
## Priority:
# 'system' and 'user'
def check_priority(package):
	PackageName = VARDIR + '/packages/' + package + '/config.json'
	if os.path.isfile(PackageName):
		with open(PackageName, 'r') as f:
			packageData = json.load(f.read())

			if packageData["priority"] == "system":
				print_msg("Приоритет пакета: системный.")
				return 1
			elif packageData["priority"] == "user":
				print("Приоритет пакета: пользовательский")
				return 0
			else:
				print("Ошибка: приоритет не может быть установлен!")
				exit(1)
	else:
		print("Ошибка: пакета {} не существует!", package)
		exit(1)

# Function for search a package
# Only for install_pkg function
def search_pkg(archive):
	archive_tar = archive + '.txz' 	# Если пользователь ищет пакет по названию без расширения,
									# то добавить его
	print(">> Поиск пакета ", archive)
	
	if os.path.isfile(archive) or os.path.isfile(archive_tar):
		print("Пакет существует в файловой системе!")
	else:
		print("Ошибка: пакета не существует, либо его имя введено неправильно.")
		exit(1)
	
# Function for unpack a package
def unpack_pkg(archive):
	if os.path.isdir(pkg_cache_dir):
		print("Кеш существует.")
	else:
		print("Кеш не существует, создаю новый."
		os.makedirs(pkg_cache_dir)
	
	# Распаковка пакета
	if os.path.isfile(archive):
		try:
			t = tarfile.open(archive, 'r')
			
			# Проверка на наличие старого пакета в кеше
			if os.path.isdir(PACKAGE_CACHE):
				shutil.rmtree(PACKAGE_CACHE)
			
			t.extractall(path=pkg_cache_dir) # Распаковка в кеш
			
			# Проверка на наличие уже распакованного пакета
			if os.path.isdir(PACKAGE_CACHE):
				print("Пакет распакован успешно!")
			else:
				print("Неизвестная ошибка: пакет не был распакован, так как не найдена директория ", PACKAGE_CACHE)
				exit(1)
			
		except ReadError:
			print("Ошибка чтения пакета!")
			exit(1)
		except CompressionError:
			print("Ошибка: формат сжатия не поддерживается!")
			exit(1)
	
# Install package
def install_pkg():
	PKGDIR = PACKAGE_CACHE + '/pkg/' # Директория с данными пакета

	if os.path.isfile(PACKAGE_CONFIG):
		with open(PACKAGE_CONFIG, 'r') as f:
			packageData = json.load(f.read())
			
			print(">> Установка пакета ", packageData["name"])
			list_depends("nopkg", "install")
			other-functions.dialog_msg()
			
			# Выволнение предустановочных скриптов
			if os.path.isfile(PREINSTALL):
				print("Выполнение preinstall скриптов...")
				rc = call(PREINSTALL, shell=True)
			else:
				print("preinstall скрипты не найдены.")
			
			# Копирование данных
			if os.path.isdir(PKGDIR):
				print("Найдена директория с данными пакета. Устанавливаю их...")
				shutil.copy2(PKGDIR, '/')
			else:
				print("Ошибка: не найдена директория с данными пакета. Аварийное завершение работы.")
				exit(1)
			
			# Выполнение послеустановочных скриптов
			if os.path.isfile(POSTINSTALL):
				print("Выполнение postinstall скриптов...")
				rc = call(POSTINSTALL, shell=True)
			else:
				print("postinstall скрипты не найдены.")
			
			# Добавление пакета в базу данных
	else:
		print("Ошибка: не существует конфигурационного файла 'config.json'! Работа cpkg более невозможна.")
		exit(1)


