import py_trees
from typing import Protocol

class TipRM(Protocol):
    def tip_available(self) -> py_trees.common.Status:
        ...

    def tip_available_in_tray(self) -> py_trees.common.Status:
        ...

    def discard_current_tray(self) -> py_trees.common.Status:
        ...

    def tray_available(self) -> py_trees.common.Status:
        ...

    def slider_move_to_load(self) -> py_trees.common.Status:
        ...

    def load_next_tray(self) -> py_trees.common.Status:
        ...
    
    def prepare_to_discard(self) -> py_trees.common.Status:
        ...

    def move_tip_slider(self) -> py_trees.common.Status:
        ...
    
    def pickup_success(self) -> py_trees.common.Status:
        ...

if __name__ == "__main__":
    pass
