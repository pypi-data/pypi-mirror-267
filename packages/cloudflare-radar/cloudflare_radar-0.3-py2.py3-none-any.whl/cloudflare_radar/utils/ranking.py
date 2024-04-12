# coding:utf-8

import csv
import os
from typing import Optional

from pycountry.db import Country
from xarg import commands

from .domains import domain_database
from .request import download


class domain_ranking(dict[str, int]):
    PREFIX = "http://radar.cloudflare.com/charts/TopDomainsTable"

    def __init__(self, location: Optional[Country] = None,
                 database: Optional[domain_database] = None):
        if database is None:
            database = domain_database()
        self.__location: Optional[Country] = location
        self.__database: domain_database = database
        super().__init__()

    @property
    def location(self) -> str:
        return self.__location.name if self.__location else "Worldwide"

    @property
    def database(self) -> domain_database:
        return self.__database

    @property
    def url(self) -> str:
        location: str = self.__location.alpha_2 if self.__location else ""
        return f"{self.PREFIX}/attachment?location={location.lower()}"

    def load(self, path: str) -> bool:
        if not os.path.isfile(path):
            return False
        self.clear()
        for line in sorted(csv.DictReader(open(path)),
                           key=lambda x: int(x["rank"])):
            domain: str = line["domain"]
            assert domain not in self, f"{domain} already exists in {path}"
            self[domain] = self.database.index(domain)
        return True

    def download(self, path: str) -> bool:
        filepath: Optional[str] = download(url=self.url, path=path)
        if isinstance(filepath, str):
            commands().logger.info(f"download {self.url} success")
        else:
            commands().logger.warn(f"download {self.url} failed")
        return self.load(filepath) if isinstance(filepath, str) else False
