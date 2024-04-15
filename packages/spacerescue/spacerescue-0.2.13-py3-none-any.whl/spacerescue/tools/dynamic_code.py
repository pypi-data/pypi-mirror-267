from ctypes.wintypes import PFILETIME
from types import ModuleType
from multiprocessing import Process, Queue

import os
import time
import logging
import subprocess
import importlib


class DynamicModule:

    def __init__(self, module: ModuleType, timestamp: float):
        self.module = module
        self.timestamp = timestamp


class DynamicCode:

    FAIL_UNDER = 80

    def __init__(self, src: str):
        self.dynamic_package = self._import_dynamic_package(src)
        self.queue = Queue()
        self.last_result = None

    def validate_code(self) -> Process:
        p = Process(target=_validate_code_proc, args=(self.queue,))
        p.start()
        return p

    def get_validate_code_result(self) -> subprocess.CompletedProcess:
        return self.queue.get()

    def execute_code(self, id, context):
        self.dynamic_package = self._reload_dynamic_package(
            "brain", self.dynamic_package
        )
        self.last_result = self.dynamic_package["brain.brain"].module.think(id, context)
        return self.last_result

    def get_execute_code_result(self):
        return self.last_result

    def _import_dynamic_package(self, package_name: str, dynamic_packages: dict = {}):
        packages = self._list_packages(package_name)
        for _, package, timestamp in packages:
            dynamic_packages = self._import_one_package(package, timestamp, dynamic_packages)
        return dynamic_packages

    def _reload_dynamic_package(self, package_name: str, dynamic_packages: dict):
        modules = self._list_packages(package_name)
        for _, package, timestamp in modules:
            if not package in dynamic_packages.keys():
                dynamic_packages = self._import_one_package(
                    package, timestamp, dynamic_packages
                )
            elif timestamp > dynamic_packages[package].timestamp:
                dynamic_packages = self._reload_one_package(
                    package, timestamp, dynamic_packages
                )
        return dynamic_packages

    def _list_packages(self, package_name: str):
        result = []
        for root, _, files in os.walk(package_name):
            result += [
                self._get_package_info(file_path)
                for file_path in [os.path.join(root, file) for file in files]
                if self._is_valid_package_name(file_path)
            ]
        return result

    def _get_package_info(self, file_path: str):
        return file_path, file_path.replace(os.path.sep, ".")[:-3], os.path.getmtime(file_path)

    def _is_valid_package_name(self, file: str):
        return file.endswith(".py") and os.path.isfile(file)
    
    def _import_one_package(
        self, package: str, timestamp: float, dynamic_packages: dict
    ):
        logging.debug(f"DEBUG: CODE: [{package}] Found a new package to load")
        module = importlib.import_module(package)
        dynamic_packages[package] = DynamicModule(module, timestamp)
        return dynamic_packages

    def _reload_one_package(
        self, package: str, timestamp: float, dynamic_packages: dict
    ):
        logging.debug(f"DEBUG: CODE: [{package}] Found an existing package to reload")
        importlib.reload(dynamic_packages[package].module)
        dynamic_packages[package].timestamp = timestamp
        return dynamic_packages


def _validate_code_proc(queue: Queue):
    result = subprocess.run(["coverage", "run", "--module", "pytest"])
    if result.returncode != 0:
        time.sleep(1)
        return queue.put(result)

    result = subprocess.run(
        [
            "coverage",
            "report",
            "--show-missing",
            "--skip-covered",
            f"--fail-under={DynamicCode.FAIL_UNDER}",
            "--include=brain/*.py",
            "--omit=brain/__init__.py",
        ]
    )
    if result.returncode != 0:
        time.sleep(1)
        return queue.put(result)

    time.sleep(1)
    return queue.put(result)
