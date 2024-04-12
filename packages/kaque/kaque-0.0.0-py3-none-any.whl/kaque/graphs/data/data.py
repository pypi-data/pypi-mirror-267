import uuid
from typing import Protocol


class Data(Protocol):
    """
    DataTypes are integral to the Kaque data model.
    They are used to define the type of data that a variable can hold,
    and with it, transformations that must be satisfied.
    """

    def __str__(self) -> str:
        return self.__class__.__name__

    def __hash__(self) -> str:
        return self.unique_id()

    def unique_id(self) -> str:
        return str(uuid.uuid4())
