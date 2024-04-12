import abc
from typing import Protocol

from kaque.graphs.data import Data


class Map(Protocol):
    @property
    @abc.abstractmethod
    def input(self) -> Data: ...

    @property
    @abc.abstractmethod
    def output(self) -> Data: ...
