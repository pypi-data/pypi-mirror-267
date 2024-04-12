from typing import Any

from .data import Data


class Nested(Data):
    """
    Nested data type.
    """

    attributes: dict[str, Data]

    def __init__(self, attributes: dict[str, Data], /) -> None:
        super().__init__()

        self.attributes = attributes

    def __getitem__(self, key: str) -> Data:
        return self.attributes[key]

    def __setitem__(self, key: str, value: Data) -> None:
        self.attributes[key] = value
