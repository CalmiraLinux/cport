#!/usr/bin/python3

import os
import wget
import time
import tarfile
import subprocess
import cp_default as cdf
import cp_info    as cpI

PORT_DIR  = cdf.PORT_DIR
CACHE_DIR = cdf.CACHE_DIR
CACHE_DATA_DIR = cdf.CACHE_DATA_DIR

class prepare():
    
    def download(self, port):
        url  = cpI.get().port_info(port, "port_management", "url")
        file = cpI.get().port_info(port, "port_management", "file")
        cache_file = f"{CACHE_DIR}{file}"

        if os.path.isfile(cache_file):
            os.remove(cache_file)

        try:
            wget.download(url, file)
            return True
        except Error as err:
            cdf.msg().error_trace(
                err,
                f"cpi.prepare.gownload({port})"
            )
            return False

    def unpack(self, port):
        file = cpI.get().port_info(port, "port_management", "file")
        cache_file = f"{CACHE_DIR}{file}"

        if not os.path.exists(cache_file):
            cdf.msg().error_trace(
                f"File '{cache_file}' not found!",
                f"cpi.prepare.unpack({port})"
            )
            return False

        if os.path.exists(CACHE_DATA_DIR):
            # Очистка директории, в которую будет распакован архив с исходным кодом
            os.removedirs(CACHE_DATA_DIR)
            # TODO: проверить на работоспособность
        os.makedirs(CACHE_DATA_DIR)

        try:
            with tarfile.open(cache_file) as t:
                t.extractall(path=CACHE_DATA_DIR)
            return True
        except Error as err:
            cdf.msg().error_trace(
                f"File '{cache_file}' not found!",
                f"cpi.prepare.unpack({port})"
            )
            return False

class build(prepare):

    def calc_time(self, func):
        def wrapper(*args, **kwargs):
            time_start = time.time()
            data = func(*args, **kwargs)
            time_end = time.time()

            diff = (time_end - time_start) / 189

            print(f"Build time: {diff} SBU")
            return func
        return wrapper
    
    @self.calc_time
    def build(self, port) -> int:
        port_config = PORT_DIR + port + "/config.ini"
        port_install = PORT_DIR + port + "/install"

        run = subprocess.run(port_install, shell=True)

        return run.returncode

    def add_in_db(self, port):
        """
        TODO: add a code
        """
