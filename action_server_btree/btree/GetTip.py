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
    def prepare_tip_for_pickup(self, timestamp) -> str:
        return "prepare_tip_for_pickup"
    def pick_up_using_orchestraror(self, timestamp) -> str:
        return "pick_up_using_orchestraror"
    def tip_available(self, timestamp) -> None:
        expr = f"TipRM/trigger?timestamp={timestamp}&event=tip_available"
        value = get_status(expr)
        return value
    def pick_up_success(self, timestamp) -> str:
        expr = f"TipRM/trigger?timestamp={timestamp}&event=pick_up_success"
        value = get_status(expr)
        return value
    def tip_available_in_tray(self, timestamp) -> str:
        expr = f"TipRM/trigger?timestamp={timestamp}&event=tip_available_in_tray"
        value = get_status(expr)
        return value
    def move_tip_slider_yo_pos(self, timestamp) -> str:
        expr = f"TipRM/trigger?timestamp={timestamp}&event=move_tip_slider_to_pos"
        value = get_status(expr)
        return value
    def pick_up(self, timestamp) -> str:
        expr = f"Orchestrator/trigger?timestamp={timestamp}&event=pick_up"
        value = get_status(expr)
        return value
    def caught_tip_firm_and_orient(self, timestamp) -> str:
        expr = f"TipChecker/trigger?timestamp={timestamp}&event=caught_tip_firm_and_orient"
        expr_ = f"Orchestrator/trigger?timestamp={timestamp}&event=caught_tip_firm_and_orient"
        value = get_status(expr)
        value_1 = get_status(expr_)
        if value['response_type'] == "accepted" and value_1['response_type'] == "accepted":
            return value
        else:
            value = {"response_type":"Rejected", "response":"Tip not caught"}
            return value
    def discard_current_tray(self, timestamp) -> str:
        expr = f"TipRM/trigger?timestamp={timestamp}&event=discard_current_tray"
        value = get_status(expr)
        return value
    def discard_success(self, timestamp) -> str:
        expr = f"Pipette/trigger?timestamp={timestamp}&event=discard_success"
        value = get_status(expr)
        return value
    def load_new_tray(self, timestamp) -> str:
        return "load_new_tray"
    def load_success(self, timestamp) -> str:
        expr = f"Pipette/trigger?timestamp={timestamp}&event=load_success"
        value = get_status(expr)
        return value
    def already_in_pos(self, timestamp) -> str:
        expr = f"TipRM/trigger?timestamp={timestamp}&event=already_in_pos"
        value = get_status(expr)
        return value
    def move_tip_slider(self, timestamp) -> str:
        expr = f"TipRM/trigger?timestamp={timestamp}&event=moving_tip_slider"
        value = get_status(expr)
        return value
    def slider_reached(self, timestamp) -> str:
        expr = f"TipRM/trigger?timestamp={timestamp}&event=slider_reached"
        value = get_status(expr)
        return value
    def discard_tip(self, timestamp) -> str:
        return "discard_tip"
    def tray_avaialble(self, timestamp) -> str:
        expr = f"TipRM/trigger?timestamp={timestamp}&event=tray_available"
        value = get_status(expr)
        return value
    def slider_move_to_load(self, timestamp) -> str:
        expr = f"TipRM/trigger?timestamp={timestamp}&event=slider_move_to_load"
        value = get_status(expr)
        return value
    def load_next_tray(self, timestamp) -> str:
        expr = f"TipRM/trigger?timestamp={timestamp}&event=load_next_tray"
        value = get_status(expr)
        return value
    def goto_discard_position(self, timestamp) -> str:
        expr = f"Orchestrator/trigger?timestamp={timestamp}&event=goto_discard_position"
        value = get_status(expr)
        return value
    def prepare_to_discard(self, timestamp) -> str:
        expr = f"TipRM/trigger?timestamp={timestamp}&event=prepare_to_discard"
        value = get_status(expr)
        return value
    def eject_tip(self) -> str:
        expr = "Pipette/trigger?timestamp=123456789&event=eject_tip"
        value = get_status(expr)
        return value
    def discard_tip_success(self, timestamp) -> str:
        expr = f"TipChecker/trigger?timestamp={timestamp}&event=discard_tip_success"
        expr_ = f"Pipette/trigger?timestamp={timestamp}&event=discard_tip_success"
        value = get_status(expr)
        value_1 = get_status(expr_)
        if value['response_type'] == "accepted" and value_1['response_type'] == "accepted":
            return value
        else:
            value = {"response_type":"Rejected", "response":"Tip not caught"}
            return value
    def retry_count_below_threshold(self, timestamp) -> str:
        return "retry_count_below_threshold"
 