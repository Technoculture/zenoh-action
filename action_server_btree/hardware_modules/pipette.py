from typing import Protocol
from exceptions import exceptions
import logging

logging.getLogger().setLevel(logging.DEBUG)

class DiscardSuccess(Protocol):
    def discard_success(self) -> bool:
        ...

class LoadSuccess(Protocol):
    def load_success(self) -> bool:
        ...

class EjectTip(Protocol):
    def eject_tip(self) -> bool:
        ...
    
class DiscardTipSuccess(Protocol):
    def discard_tip_success(self) -> None:
        ...

class Discard_success:
    def discard_success(self) -> bool:
        return True

class Load_success:
    def load_success(self) -> bool:
        return True

class Eject_tip:
    def eject_tip(self) -> bool:
        return True

class Discard_tip_success:
    def discard_tip_success(self) -> None:
        raise exceptions.RetryException()
        

class Pipette:
    def discard_success(self, obj: DiscardSuccess) -> object:
        return obj.discard_success()

    def load_success(self, obj: LoadSuccess) -> object:
        return obj.load_success()

    def eject_tip(self, obj: EjectTip) -> object:
        return obj.eject_tip()

    def discard_tip_success(self, obj: DiscardTipSuccess) -> None:
        return obj.discard_tip_success()

if __name__ == "__main__":
    pipette = Pipette()
    check = input("Enter Query: ")
    match check:
        case "discard_success":
            logging.debug(pipette.discard_success(Discard_success()))
        case "load_success":
            logging.debug(pipette.load_success(Load_success()))
        case "eject_tip":
            logging.debug(pipette.eject_tip(Eject_tip()))
        case "discard_tip_success":
            pipette.discard_tip_success(Discard_tip_success())