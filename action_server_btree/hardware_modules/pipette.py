import py_trees
from typing import Protocol
from exceptions import exceptions

class DiscardSuccess(Protocol):
    def discard_success(self) -> py_trees.common.Status:
        ...

class LoadSuccess(Protocol):
    def load_success(self) -> py_trees.common.Status:
        ...

class EjectTip(Protocol):
    def eject_tip(self) -> py_trees.common.Status:
        ...
    
class DiscardTipSuccess(Protocol):
    def discard_tip_success(self) -> py_trees.common.Status:
        ...

class Discard_success:
    def discard_success(self) -> py_trees.common.Status:
        return py_trees.common.Status.SUCCESS

class Load_success:
    def load_success(self) -> py_trees.common.Status:
        if py_trees.blackboard.Blackboard().get("Load")
            raise exceptions.RetryException()

class Eject_tip:
    def eject_tip(self) -> py_trees.common.Status:
        return py_trees.common.Status.SUCCESS

class Discard_tip_success:
    def discard_tip_success(self) -> None:
        raise exceptions.RetryException()
        

class Pipette:
    def discard_success(self, obj: DiscardSuccess) -> py_trees.common.Status:
        return obj.discard_success()

    def load_success(self, obj: LoadSuccess) -> py_trees.common.Status:
        return obj.load_success()

    def eject_tip(self, obj: EjectTip) -> py_trees.common.Status:
        return obj.eject_tip()

    def discard_tip_success(self, obj: DiscardTipSuccess) -> py_trees.common.Status:
        return obj.discard_tip_success()



if __name__ == "__main__":
    pass