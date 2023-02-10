import py_trees
from typing import Protocol

class TipChecker(Protocol):
    def caught_tip_firm_and_orient(self) -> py_trees.common.Status:
        ...

    def discard_tip_success(self) -> py_trees.common.Status:
        ...

class TipChecker_:
    def caught_tip_firm_and_orient(self) -> py_trees.common.Status:
        return py_trees.common.Status.SUCCESS

    def discard_tip_success(self) -> py_trees.common.Status:
        return py_trees.common.Status.SUCCESS

if __name__ == "__main__":
    tip_checker = TipChecker_()
    
