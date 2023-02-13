from typing import Protocol
from exceptions import exceptions
import logging

logging.getLogger().setLevel(logging.DEBUG)

class CaughtTipFirmAndOrient(Protocol):
    def caught_tip_firm_and_orient(self) -> bool:
        ... 

class DiscardTipSuccess(Protocol):
    def discard_tip_success(self) -> bool:
        ...

class Caught_tip_firm_and_orient:
    def caught_tip_firm_and_orient(self) -> bool:
        return True

class Discard_tip_success:
    def discard_tip_success(self) -> bool:
        return True

class TipChecker:
    def caught_tip_firm_and_orient(self, obj: CaughtTipFirmAndOrient) -> bool:
        return obj.caught_tip_firm_and_orient()
    
    def discard_tip_success(self, obj: DiscardTipSuccess) -> bool:
        return obj.discard_tip_success()

        print("caught_tip_firm_and_orient success")

if __name__ == "__main__":
    tip_checker = TipChecker()
    check = input("Enter Query: ")
    match check:
        case "caught_tip_firm_and_orient":
            logging.debug(tip_checker.caught_tip_firm_and_orient(Caught_tip_firm_and_orient()))
        case "discard_tip_success":
            logging.debug(tip_checker.discard_tip_success(Discard_tip_success()))