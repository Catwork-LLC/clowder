import abc
from typing import Sequence


class VariableSource(abc.ABC):
    def get_variables(self, names: Sequence[str]):
        pass


class VariableClient(abc.ABC):
    def poll(self):
        pass
