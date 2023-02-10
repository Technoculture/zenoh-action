import py_trees
from typing import Protocol

class Orchestrator(Protocol):
    def pick_up(self) -> py_trees.common.Status:
        ...

    def caught_tip_firm_and_orient(self) -> py_trees.common.Status:
        ...

    def go_to_discard_position(self) -> py_trees.common.Status:
        ...

    def goto_discard_position(self) -> py_trees.common.Status:
        ...

if __name__ == "__main__":
    pass