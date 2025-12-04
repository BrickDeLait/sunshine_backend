from abc import ABC, abstractmethod
from enum import EnumMeta

class Endpoint(ABC, EnumMeta):
    @abstractmethod
    def host(self):
        pass

    @abstractmethod
    def path(self):
        pass

    @abstractmethod
    def url(self):
        pass

    @abstractmethod
    def method(self):
        pass
    