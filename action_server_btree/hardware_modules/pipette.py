import py_trees
from typing import Protocol

class Pipette(Protocol):
    def discard_success(self) -> py_trees.common.Status:
        ...

    def load_success(self) -> py_trees.common.Status:
        ...

    def eject_tip(self) -> py_trees.common.Status:
        ...
    
    def discard_tip_success(self) -> py_trees.common.Status:
        ...

if __name__ == "__main__":
    pass