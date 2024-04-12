# coding:utf-8

import csv
import os
from typing import Any
from typing import Dict
from typing import List
from typing import Union

from xarg import safile


class domain_name(object):
    FIELDS: List[str] = ["number", "domain"]

    def __init__(self, number: Union[int, str], domain: str, **kwargs: Any):
        self.__number: int = int(number)
        self.__domain: str = domain
        super().__init__()

    @property
    def number(self) -> int:
        return self.__number

    @property
    def domain(self) -> str:
        return self.__domain

    def dump(self) -> Dict[str, str]:
        values = [self.number, self.domain]
        return {k: v for k, v in zip(self.FIELDS, values)}


class domain_database(dict[str, domain_name]):

    def __init__(self):
        self.__updated: bool = False
        self.__peak: int = 0
        super().__init__()

    @property
    def peak(self) -> int:
        return self.__peak

    @property
    def updated(self) -> bool:
        return self.__updated

    @updated.setter
    def updated(self, value: bool):
        self.__updated = value

    def add(self, object: domain_name):
        assert object.domain not in self, f"{object.domain} already exists"
        self.__peak = max(self.peak, object.number)
        self[object.domain] = object

    def index(self, domain: str) -> int:
        if domain not in self:
            self.add(domain_name(number=self.peak + 1, domain=domain))
            self.updated = True
        assert domain in self, f"{domain} not exists"
        return self[domain].number


class domain_dbstore(domain_database):

    def __init__(self, path: str):
        self.__path: str = path
        super().__init__()
        self.__load()

    def __load(self):
        assert safile.restore(self.path), f"restore {self.path} failed"
        if not os.path.exists(self.path):
            return
        assert os.path.isfile(self.path), f"{self.path} not a regular file"
        with open(self.path) as rhdl:
            for line in csv.DictReader(rhdl):
                self.add(domain_name(**line))

    def dump(self):
        if not self.updated:
            return
        assert safile.create_backup(self.path), \
            f"create {self.path} backup failed"
        with open(self.path, "w") as whdl:
            writer = csv.DictWriter(whdl, fieldnames=domain_name.FIELDS)
            writer.writeheader()
            for item in self.values():
                writer.writerow(item.dump())
        assert safile.delete_backup(self.path), \
            f"delete {self.path} backup failed"
        self.updated = False

    @property
    def path(self) -> str:
        return self.__path
