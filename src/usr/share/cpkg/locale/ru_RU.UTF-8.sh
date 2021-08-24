#!/bin/bash
#
# CPkg - an automated packaging tool for Calmira Linux
# Copyright (C) 2021 Michail Krasnov
#
# Project Page: http://github.com/Linuxoid85/cpkg
# Michail Krasnov <michail383krasnov@mail.ru>
#

# cpkg
CPKG_ABOUT="CPkg - пакетный менеджер для Calmira GNU/Linux"
CPKG_VER="Версия ПМ:"
CPKG_DISTRO_VER="Версия дистрибутива:"
METADATA_IS_CREATED="Метаданные успешно созданы!"
METADATA_IS_NOT_CREATED="Метаданные не были созданы!"

# errors
ERROR="ОШИБКА:"
ERROR_NO_FUNC="\e[1;31mОШИБКА: файл /usr/lib/cpkg/$FUNC не существует! \e[0m"
ERROR_PACKAGE_NOT_INSTALLED="\e[1;31mОШИБКА: пакет \e[1;35m$PACKAGE\e[0m\e[1;31m не установлен! \e[0m"
ERROR_NO_OPTION="\e[1;31mОШИБКА: опция(и) '$@' не существуют! \e[0m\n"
ERROR_UNPACK_PKG_NOT_FOUND="\e[1;31mПакет\e[0m\e[35m $PKG\e[0m\e[1;31m не распакован! \e[0m"
ERROR_NO_OPTION="Опция не распознана!"
ERROR_NO_MODE_FOR_CHECK_MD="\e[1;31m$ERROR для функции 'check_md' не указан режим работы! \e[0m"
CRITICAL_ERROR="\e[1;31mКритическая ошибка! Работа cpkg более не возможна.\e[0m"
ERROR_PKG_BLOCKED="Пакет находится в чёрном списке, поэтому его удаление запрещено!"
ERROR_NO_FILE_VAR="Не существует файловой переменной в описании пакета, либо пакет системный и устанавливался из портов! Выход."
WARNING="ПРЕДУПРЕЖДЕНИЕ:"

# actions
ACTION_INSTALL="Установка пакета"
ACTION_REMOVE="Удаление пакета"
ACTION_DOWNLOAD="Установка пакета"
ACTION_UPDATE_LIST="Обновление списка пакетов"
ACTION_LIST="Просмотр списка пакетов"
ACTION_SEARCH="Поиск пакета"
ACTION_INFO="Просмотр информации о пакете"
ACTION_CLEAN="Очистка кеша"
ACTION_SOURCE="Редактирование списка пакетов"
ACTION_UKNOWN_OPTION="Запуск 'cpkg' с опцией(ями), которая(ые) неизвестна(ы) ПМ: "

# other
DONE="Завершено"
RETRY="повторение..."
FAIL="\e[1;31mОШИБКА\e[0m"
PKGLIST_DOWNLOAD="\e[1;32mСкачивание списка пакетов...\e[0m"
FILE="Файл"
DOESNT_EXISTS="не существует!"
DOESNT_INSTALLED="не установлен!"
PACKAGE="Пакет"
CONTINUE="Продолжить?"
NONE="нет"
CANSELLED="Прервано!"
WARIABLE="Переменная"

# depends
REQUIRED_DEP="Необходимые:"
TESTING_DEP="Для тестирования:"
OPTIONAL_DEP="Опциональные:"
BEFORE_DEP="Установлен перед ними:"
RECOMMEND_DEP="Рекомендуемые:"
RUNTIME_DEP="Во время выполнения:"
CONFLICT_DEP="Конфликтует с:"
PORT_PKG="Установлен из порта:"
DEP_INSTALL="Установите эти зависимости перед установкой пакета, если иное не сказано в пункте $BEFORE_DEP!\e[0m"
DEP_REMOVE="Удалите эти зависимости перед удалением пакета, если иное не сказано в пунктах выше!"
DEP_INFO="При удалении или переустановке пакета убедитесь, что зависимости удовлетворены!"


###########################
##                       ##
##   core-functions.sh   ##
##                       ##
###########################

# check_priority
CHECK_PRIORITY_START="\e[1;32mЗапуск проверки приоритета пакета...\e[0m"
PRIORITY_NOT_FOUND="\e[31mПеременная приоритета \e[0m\e[35m\$PRIORITY\e[0m\e[31m не найдена в \e[0m\e[35m$(pwd)/config.sh\e[0m\e[31m!\e[0m"
PRIORITY_NOT_FOUND_ANSWER="\e[1mДействительно удалить пакет? Помните, что удаление пакета с неизвестным приоритетом НЕ РЕКОМЕНДУЕТСЯ! (y/n) \e[0m"
SYSTEM_PRIORITY_REMOVE_BLOCKED="ВНИМАНИЕ! Приоритет пакета: 'системный'. Это значит, что пакет необходим для
корректной работы системы, поэтому его удаление запрещено. Выход."
PRIORITY_DONE="\e[32mТест на приоритет прошёл успешно - это не системный пакет;
удалять можно.\e[0m"
PRIOTITY_MSG="Приоритет"

# check_md
CHECK_MD="Проверка md5 контрольных сумм..."

# check_metadata
CHECK_METADATA="Проверка метаданных пакета..."
CHECK_METADATA_OK="Проверка метаданных завершена успешно!"
CHECK_METADATA_FAIL="Проверка метаданных завершена с ошибкой. Вероятно, этот пакет не предназначен для Calmira текущей версии."

# blacklist_pkg
CHECK_INSTALLED="Проверка на наличие пакета в системе..."
CHECK_BLACKLIST_DONE="Пакет находится в чёрном списке"
CHECK_BLACKLIST_FAIL="Пакет НЕ находится в чёрном списке"
REMOVE_BLACK="Удаление пакета из чёрного списка..."
REMOVE_BLACK_DONE="Удаление пакета из чёрного списка: успешно"
REMOVE_BLACK_FAIL="Удаление пакета из чёрного списка: ОШИБКА!"
BLACKLIST_ADD_PKG="Добавление пакета в чёрный список"
BLACKLIST_CHECK_PKG="Проверка пакета на наличие в чёрном списке"
BLACKLIST_REMOVE_PKG="Удаление пакета из чёрного списка"

# blacklist_pkg
ADD_BLACKLIST="Добавление пакета в чёрный список..."
REMOVE_BLACKLIST="Удаление пакета из чёрного списка..."
CHECK_BLACKLIST="Проверка пакета на нахождение в чёрном списке..."

# search_pkg and file_search
SEARCH_PACKAGE="\e[1;32mПоиск пакета\e[0m \e[35m$PKG\e[0m\e[1;32m...\e[0m"
SEARCH1="Пакет"
SEARCH2="существует в"
SEARCH_RESULT="Результаты поиска:"

# unpack_pkg
UNPACK1="\e[1;32mРаспаковка пакета\e[0m"
UNPACK_COMPLETE1="\e[32mПакет\e[0m"
UNPACK_COMPLETE2="\e[32mраспакован\e[0m\n"
UNPACK_FAIL1="\e[1;31mПакет\e[0m"
UNPACK_FAIL2="\e[1;31mне был распакован! \e[0m"

# arch_test
ARCH_TEST="\e[1;32mТест архитектуры пакета...\e[0m"
ARCH_VARIABLE_NOT_FOUND="\e[31m[ Указатель архитектуры не существует ]\e[0m"
MULTIARCH_DONE="\e[32m [ Мультиархитектурный тест прошёл успешно! ] \e[0m"
ARCH_DONE="\e[32m[ Архитектурный тест прошёл успешно! ]\e[0m"

# install_pkg
DEPEND_LIST_INSTALL="\e[1;32mСписок зависимостей\e[0m"
EXECUTE_PREINSTALL="\e[32mЗапуск предустановочного скрипта...\e[0m"
EXECUTE_POSTINSTALL="\e[32mЗапуск послеустановочного скрипта...\e[0m"
SETTING_UP_POSTINSTALL="\e[32mНастройка послеустановочного скрипта...\e[0m"
INSTALL_PORT="\e[1;32mУстановка port-пакета...\e[0m"
COPY_PKG_DATA="\e[1;32mКопирование данных пакета...\e[0m"
WARN_NO_PKG_DIR="\e[33mПРЕДУПРЕЖДЕНИЕ: директория 'pkg' отсутствует\e[0m"
SETTING_UP_PACKAGE="\e[1;32mНастройка пакета...\e[0m"
ADD_IN_DB="\e[32mДобавление пакета в базу данных\e[0m"
PACKAGE_IN_OTHER_PREFIX="Пакет установлен в альтернативный префикс файловой системы и не может быть удалён!"
INSTALL_OTHER_PREFIX_WARNING="Если вы выбрали альтернативный префикс для установки пакета, то ВЫ НЕ СМОЖЕТЕ ЕГО УДАЛИТЬ ИЗ СИСТЕМЫ СРЕДСТВАМИ CPKG!
Для удаления отыщите пакет в альтернативном префиксе (который вы указали) и удалите ВРУЧНУЮ только те файлы, которые относятся к нужному пакету."

# remove_pkg
PACKAGE_NOT_INSTALLED_OR_NAME_INCORRECTLY="не установлен, либо имя введено неправильно."
REMOVE_PKG="\e[1;34mУдаление пакета\e[0m"
REMOVE_PKG_FAIL="не был удалён успешно!"
REMOVE_PKG_OK="удалён успешно."

# download_pkg
FOUND_PKG="Существует"
NOT_FOUND_PKG="не существует в"
DOWNLOAD_PKG="\e[1;32mСкачивание пакета...\e[0m"
DOWNLOAD_PKG_FAIL="не был скачан успешно!"

# package_info
PACKAGE_INFO="Информация о пакете"
PACKAGE_NAME="Имя:"
PACKAGE_RELEASE="Версия:"
PACKAGE_DESCRIPTION="Описание:"
PACKAGE_MAINTAINER="Сборщик пакета:"
PACKAGE_FILES="Установленные файлы:"
PACKAGE_IN_BLACKLIST="Пакет находится в чёрном списке cpkg и не может быть удалён."
PACKAGE_SITE="Сайт программы/пакета:"

# cpkg_clean
CACHE_CLEAN="Очистка кеша..."
CLEAN_MSG="Очистка (тип):"

# help_pkg
HELP_CPKG="
---------------------------------------------------

(C) 2021 Михаил Краснов \e[4m<michail383krasnov@mail.ru>\e[0m
Для Calmira GNU/Linux"
