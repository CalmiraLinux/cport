# Список файлов утилиты

## Исходный код

* Файл для запуска: `/usr/bin/cport`;
* Модули: `/usr/lib/python3.10/site-packages`.

## Конфигурация

* `/etc/cport.d/`:
    * Базовая конфигурация: `config.ini`;
    * Репозитории: `sources.ini`.
* `/var/db/cport.d`:
    * Чёрный список портов: `blacklist.db`;
    * Установленные порты: `installed.db`.
