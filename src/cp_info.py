#!/usr/bin/python3

"""
Модуль, содержащий классы и функции для получения информации о портах.

Пример полного конфигурационного файла:
    ; Описание информации о пакете
    [package]
    name = "Имя пакета"
    version = "версия пакета"
    description = "краткое описание пакета"
    maintainer = "информация о сопровождающем пакета"
    architecture = "архитектура пакета"
    priority = "приоритет пакета"
    calm_release = [ "список релизов Calmira, с которым совместим пакет" ]

    ; Описание зависимостей пакета/порта
    [depends]
    required = [ "список необходимых зависимостей" ]
    recommend = [ "список рекомендуемых зависимостей" ]
    optional = [ "список опциональных пакетов" ]
    runtime = [ "список необходимых зависимостей в рантайме" ]
    conflict = [ "конфликтующие с этим портом зависимости" ]

    ; Информация для cport
    [port]
    url = "ссылка для скачивания архива с исходным кодом порта"
    file = "имя файла, который будет скачан"

Константы и глобальные переменные:
    - Дистрибутиво-ориентированные данные:
        - CALMIRA (= cp_default.CALMIRA)
    - PORT_DIR - директория с системой портов;
    - DATABASE_MASTER - основная база данных cport;

Классы и методы:
    - port() - для получения данных о порте. Наследован от cdf.pasrer():
        - path() - получение пути до порта;
        - info_param() - получение указанной информации из конфига порта;
"""

import cp_default as cdf

PORT_DIR = cdf.PORT_DIR
CALMIRA = cdf.CALMIRA
DATABASE_MASTER = cdf.DATABASE_MASTER

class port(cdf.parser):

    """
    Получение данных о порте
    """

    def __init__(self, port_name: str):
        self.port_name = port_name

    def path(self) -> str:
        """
        Function for getting information about port path directory

        Usage:
        path(port)

        | variable | data type |
        |----------|-----------|
        | 'port'   | str       |

        Return code: str
        """

        port_path = f"{PORT_DIR}/{self.port_name}"

        if not os.path.isdir(port_path):
            return None
        return port_path

    def info_param(self):
        """
        Function for get some parameters from a TOML file (port config)

        Usage:
        info_param(port)

        | variable | data type |
        |----------|-----------|
        | 'port'   | str       |

        Return code: dict
        """

        port_path = self.path(port_name)
        port_config = f"{port_path}/port.conf"

        data = self.get(port_config)

        return data

class database:

    def __init__(self, port_name: str):
        self.port_name = port_name

        self.conn = sqlite3.connect(DATABASE_MASTER)
        self.cursor = conn.cursor()

    def check_port_exists(self) -> bool:
        self.cursor.execute("SELECT name FROM ports WHERE name = ?", (self.port_name ))
        if self.cursor.fetchone() is None:
            return False
        return True

class format_out:

    def __init__(self, port_name: str):
        self.port_name = port_name

    def base_info(self, section: str, params: tuple):
        port_path = port().path(self.port_name)

        if not port_path is None:
            for param in params:
                data = port().get(self.port_name)
                if not data is none:
                    print(f"\033[1m{param}:\033[0m {data[section][param]}")
            return {"request": "ok"}
        else:
            return {"request": "PortNotFoundError"}

    def description(self):
        port_path = port().path(self.port_name)
        data = port().info_param(self.port_name)

        description_base = data['package']['description']

        description_file = f"{port_path}/description.txt"
        with open(description_file) as f:
            description_full = f.read()

        print(f"\033[1mdescription:\033[0m {description_base}")
        print(f"\033[1mdescription full:\033[0m {description_full}")
