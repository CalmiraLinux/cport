#!/usr/bin/python3
# Демонстрация обработчика зависимостей

import os
import subprocess
import json

PORT = "./ports/"

def depends(object):
    def get(port):
        config = PORT + port + "/config.json"
        
        if not os.path.isfile(config):
            print(f"Ошибка: конфига порта '{port}' не существует!")
            exit(1)
        
        f = open(config)
        data = json.load(f)
        deps = data["deps"]["required"]
        
        f.close()
        return deps
    

def install(port):
