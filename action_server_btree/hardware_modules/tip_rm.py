from typing import Protocol
import logging

logging.getLogger().setLevel(logging.DEBUG)

class TipAvailable(Protocol):
    def tip_available(self) -> bool:
        ...
class TipAvailableInTray(Protocol):
    def tip_available_in_tray(self) -> bool:
        ...
class DiscardCurrentTray(Protocol):
    def discard_current_tray(self) -> bool:
        ...
class TrayAvailable(Protocol):
    def tray_available(self) -> bool:
        ...
class SliderMoveToLoad(Protocol):
    def slider_move_to_load(self) -> bool:
        ...
class LoadNextTray(Protocol):
    def load_next_tray(self) -> bool:
        ...
class PrepareToDiscard(Protocol):
    def prepare_to_discard(self) -> bool:
        ...
class MoveTipSlider(Protocol):
    def move_tip_slider(self) -> bool:
        ...
class PickupSuccess(Protocol):
    def pickup_success(self) -> bool:
        ...

class Tip_available:
    def tip_available(self) -> bool:
        return True
class Tip_available_in_tray:
    def tip_available_in_tray(self) -> bool:
        return True
class Discard_current_tray:
    def discard_current_tray(self) -> bool:
        return True
class Tray_available:
    def tray_available(self) -> bool:
        return True
class Slider_move_to_load:
    def slider_move_to_load(self) -> bool:
        return True
class Load_next_tray:
    def load_next_tray(self) -> bool:
        return True
class Prepare_to_discard:
    def prepare_to_discard(self) -> bool:
        return True
class Move_tip_slider:
    def move_tip_slider(self) -> bool:
        return True
class Pickup_success:
    def pickup_success(self) -> bool:
        return True

class TipRM:
    def tip_available(self, obj: TipAvailable) -> bool:
        return obj.tip_available()

    def tip_available_in_tray(self, obj: TipAvailableInTray) -> bool:
        return obj.tip_available_in_tray()

    def discard_current_tray(self, obj: DiscardCurrentTray) -> bool:
        return obj.discard_current_tray()

    def tray_available(self, obj: TrayAvailable) -> bool:
        return obj.tray_available()

    def slider_move_to_load(self, obj: SliderMoveToLoad) -> bool:
        return obj.slider_move_to_load()

    def load_next_tray(self, obj: LoadNextTray) -> bool:
        return obj.load_next_tray()
    
    def prepare_to_discard(self, obj: PrepareToDiscard) -> bool:
        return obj.prepare_to_discard()

    def move_tip_slider(self, obj: MoveTipSlider) -> bool:
        return obj.move_tip_slider()
    
    def pickup_success(self, obj: PickupSuccess) -> bool:
        return obj.pickup_success()

if __name__ == "__main__":
    tip_rm = TipRM()
    check = input("Enter Query: ")
    match check:
        case "tip_available":
            logging.debug(tip_rm.tip_available(Tip_available()))
        case "tip_available_in_tray":
            logging.debug(tip_rm.tip_available_in_tray(Tip_available_in_tray()))
        case "discard_current_tray":
            logging.debug(tip_rm.discard_current_tray(Discard_current_tray()))
        case "tray_available":
            logging.debug(tip_rm.tray_available(Tray_available()))
        case "slider_move_to_load":
            logging.debug(tip_rm.slider_move_to_load(Slider_move_to_load()))
        case "load_next_tray":
            logging.debug(tip_rm.load_next_tray(Load_next_tray()))
        case "prepare_to_discard":
            logging.debug(tip_rm.prepare_to_discard(Prepare_to_discard()))
        case "move_tip_slider":
            logging.debug(tip_rm.move_tip_slider(Move_tip_slider()))
        case "pickup_success":
            logging.debug(tip_rm.pickup_success(Pickup_success()))
            
