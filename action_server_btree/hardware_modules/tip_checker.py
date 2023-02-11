import py_trees
from typing import Protocol
from exceptions import exceptions

class CaughtTipFirmAndOrient(Protocol):
    def caught_tip_firm_and_orient(self) -> py_trees.common.Status:
        ... 

class DiscardTipSuccess(Protocol):
    def discard_tip_success(self) -> None:
        ...

class Caught_tip_firm_and_orient:
    def caught_tip_firm_and_orient(self) -> py_trees.common.Status:
        return py_trees.common.Status.SUCCESS

class Discard_tip_success:
    def discard_tip_success(self) -> None:
        raise exceptions.RetryException()

class TipChecker:
    def caught_tip_firm_and_orient(self, obj: CaughtTipFirmAndOrient) -> py_trees.common.Status:
        return obj.caught_tip_firm_and_orient()
    
    def discard_tip_success(self, obj: DiscardTipSuccess) -> None:
        return obj.discard_tip_success()

def main() -> None:
    tip_checker = TipChecker()
    if tip_checker.caught_tip_firm_and_orient(Caught_tip_firm_and_orient()) != py_trees.common.Status.SUCCESS:
        raise Exception("fail")
    else:
        print("caught_tip_firm_and_orient success")

if __name__ == "__main__":
    main()