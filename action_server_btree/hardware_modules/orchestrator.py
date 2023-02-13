from typing import Protocol

class Orchestrator(Protocol):
    def pick_up(self) -> None:
        ...

    def caught_tip_firm_and_orient(self) -> None:
        ...

    def go_to_discard_position(self) -> None:
        ...

    def goto_discard_position(self) -> None:
        ...

if __name__ == "__main__":
    pass