from typing import Optional, Sequence


from clowder.specs import NestedArray
from clowder.variable import VariableSource


class MockVariableSource(VariableSource):
    def __init__(self, variables: Optional[NestedArray] = None) -> None:
        super().__init__()
        self._variables = variables

    def get_variables(self, names: Sequence[str]):
        return names
