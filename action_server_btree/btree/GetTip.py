import logging
import zenoh
from zenoh import QueryTarget

logging.getLogger().setLevel(logging.DEBUG)

def get_status(key_expression: str):
    session = zenoh.open(zenoh.Config())
    replies = session.get(key_expression, zenoh.Queue(), QueryTarget.ALL())
    for reply in replies:
        logging.debug("Received reply: {}".format(reply))
        return reply.ok.payload.decode("utf-8")

class Get_Tip():
    def prepare_tip_for_pickup(self) -> str:
        return "prepare_tip_for_pickup"
    def pick_up_using_orchestraror(self) -> str:
        return "pick_up_using_orchestraror"
    def tip_available(self) -> None:
        expr = "TipRM/trigger?timestamp=123456789&event=tip_available"
        value = get_status(expr)
        return value
    def pick_up_success(self) -> str:
        expr = "TipRM/trigger?timestamp=123456789&event=pick_up_success"
        value = get_status(expr)
        return value
    def tip_available_in_tray(self) -> str:
        expr = "TipRM/trigger?timestamp=123456789&event=tip_available_in_tray"
        value = get_status(expr)
        return value
    def move_tip_slider_yo_pos(self) -> str:
        expr = "TipRM/trigger?timestamp=123456789&event=move_tip_slider_to_pos"
        value = get_status(expr)
        return value
    def pick_up(self) -> str:
        expr = "Orchestrator/trigger?timestamp=123456789&event=pick_up"
        value = get_status(expr)
        return value
    def caught_tip_firm_and_orient(self) -> str:
        expr = "TipChecker/trigger?timestamp=123456789&event=caught_tip_firm_and_orient"
        expr_ = "Orchestrator/trigger?timestamp=123456789&event=caught_tip_firm_and_orient"
        value = get_status(expr)
        value_1 = get_status(expr_)
        if value['response_type'] == "accepted" and value_1['response_type'] == "accepted":
            return value
        else:
            value = {"response_type":"Rejected", "response":"Tip not caught"}
            return value
    def discard_current_tray(self) -> str:
        expr = "TipRM/trigger?timestamp=123456789&event=discard_current_tray"
        value = get_status(expr)
        return value
    def discard_success(self) -> str:
        expr = "Pipette/trigger?timestamp=123456789&event=discard_success"
        value = get_status(expr)
        return value
    def load_new_tray(self) -> str:
        return "load_new_tray"
    def load_success(self) -> str:
        expr = "Pipette/trigger?timestamp=123456789&event=load_success"
        value = get_status(expr)
        return value
    def already_in_pos(self) -> str:
        expr = "TipRM/trigger?timestamp=123456789&event=already_in_pos"
        value = get_status(expr)
        return value
    def move_tip_slider(self) -> str:
        expr = "TipRM/trigger?timestamp=123456789&event=moving_tip_slider"
        value = get_status(expr)
        return value
    def slider_reached(self) -> str:
        expr = "TipRM/trigger?timestamp=123456789&event=slider_reached"
        value = get_status(expr)
        return value
    def discard_tip(self) -> str:
        return "discard_tip"
    def tray_avaialble(self) -> str:
        expr = "TipRM/trigger?timestamp=123456789&event=tray_available"
        value = get_status(expr)
        return value
    def slider_move_to_load(self) -> str:
        expr = "TipRM/trigger?timestamp=123456789&event=slider_move_to_load"
        value = get_status(expr)
        return value
    def load_next_tray(self) -> str:
        expr = "TipRM/trigger?timestamp=123456789&event=load_next_tray"
        value = get_status(expr)
        return value
    def goto_discard_position(self) -> str:
        expr = "Orchestrator/trigger?timestamp=123456789&event=goto_discard_position"
        value = get_status(expr)
        return value
    def prepare_to_discard(self) -> str:
        expr = "TipRM/trigger?timestamp=123456789&event=prepare_to_discard"
        value = get_status(expr)
        return value
    def eject_tip(self) -> str:
        expr = "Pipette/trigger?timestamp=123456789&event=eject_tip"
        value = get_status(expr)
        return value
    def discard_tip_success(self) -> str:
        expr = "TipChecker/trigger?timestamp=123456789&event=discard_tip_success"
        expr_ = "Pipette/trigger?timestamp=123456789&event=discard_tip_success"
        value = get_status(expr)
        value_1 = get_status(expr_)
        if value['response_type'] == "accepted" and value_1['response_type'] == "accepted":
            return value
        else:
            value = {"response_type":"Rejected", "response":"Tip not caught"}
            return value
    def retry_count_below_threshold(self) -> str:
        return "retry_count_below_threshold"
 