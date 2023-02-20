"""Make sequence and selector of nodes from tree as node class is gettipnode.   """

from zenoh import QueryTarget #type: ignore
from pydantic import BaseModel #type: ignore
from behaviourTree.node import Node, NodeState #type: ignore
import logging
import zenoh #type: ignore

logging.getLogger().setLevel(logging.DEBUG)

def get_status(key_expression: str):
    session = zenoh.open(zenoh.Config())
    replies = session.get(key_expression, zenoh.Queue(), QueryTarget.ALL())
    for reply in replies:
        logging.debug("Received reply: {}".format(reply))
        return reply.ok.payload.decode("utf-8")

class GetTipNode(BaseModel):
    prepare_tip_for_pickup: str = "prepare_tip_for_pickup"
    pick_up_using_orchestraror: str = "pick_up_using_orchestraror"
    tip_available: str= "tip_available"
    pick_up_success: str= "pick_up_success"
    tip_available_in_tray: str= "tip_available_in_tray"
    move_tip_slider_to_pos: str= "move_tip_slider_to_pos"
    pick_up: str= "pick_up"
    caught_tip_firm_and_orient: str = "caught_tip_firm_and_orient"
    discard_current_tray: str = "discard_current_tray"
    load_new_tray: str = "load_new_tray"
    load_success: str = "load_success"
    already_in_pos: str = "already_in_pos"
    move_tip_slider: str = "move_tip_slider"
    slider_reached: str = "slider_reached"
    discard_tip: str = "discard_tip"
    tray_avaialble: str = "tray_avaialble"
    slider_move_to_load: str = "slider_move_to_load"
    load_next_tray: str = "load_next_tray"
    goto_discard_position: str = "goto_discard_position"
    prepare_to_discard: str = "prepare_to_discard"
    eject_tip: str = "eject_tip"
    discard_tip_success: str = "discard_tip_success"
    retry_count_below_threshold: str = "retry_count_below_threshold"

class GetTip(Node):
    def __init__(self) -> None:
        pass
    
    def decide_hardware_module(self, node):
        hardware_module = False
        tiprm = ["prepare_tip_for_pickup", "pick_up_using_orchestraror", "tip_available", "pick_up_success", "tip_available_in_tray", "move_tip_slider_to_pos"]
        tipchecker = ["pick_up", "caught_tip_firm_and_orient", "discard_current_tray", "load_new_tray", "load_success", "already_in_pos", "move_tip_slider", "slider_reached", "discard_tip", "tray_avaialble", "slider_move_to_load", "load_next_tray", "goto_discard_position", "prepare_to_discard", "eject_tip", "discard_tip_success", "retry_count_below_threshold"]
        orchestrator = ["pick_up", "caught_tip_firm_and_orient", "discard_current_tray", "load_new_tray", "load_success", "already_in_pos", "move_tip_slider", "slider_reached", "discard_tip", "tray_avaialble", "slider_move_to_load", "load_next_tray", "goto_discard_position", "prepare_to_discard", "eject_tip", "discard_tip_success", "retry_count_below_threshold"]
        pipette = ["pick_up", "caught_tip_firm_and_orient", "discard_current_tray", "load_new_tray", "load_success", "already_in_pos", "move_tip_slider", "slider_reached", "discard_tip", "tray_avaialble", "slider_move_to_load", "load_next_tray", "goto_discard_position", "prepare_to_discard", "eject_tip", "discard_tip_success", "retry_count_below_threshold"]
        if node in tiprm:
            hardware_module = "TipRM"
        elif node in tipchecker:
            hardware_module = "TipChecker"
        elif node in orchestrator:
            hardware_module = "Orchestrator"
        elif node in pipette:
            hardware_module = "Pipette"
        return hardware_module

    def Evaluate(self, timestamp, node) -> str:
        value = self.decide_hardware_module(node)
        if value:
            response = get_status(f"{value}/trigger?timestamp={timestamp}&event={node}")
            if response['response_type'] == "rejected":
                return "Issue with trigger."
        return "Trigger is triggered."

class Get_Tip():
    def prepare_tip_for_pickup(self, timestamp) -> str:
        return "prepare_tip_for_pickup"
    def pick_up_using_orchestraror(self, timestamp) -> str:
        return "pick_up_using_orchestraror"
    def tip_available(self, timestamp) -> None:
        expr = f"TipRM/trigger?timestamp={timestamp}&event=tip_available"
        value = get_status(expr)
        return value
    def pick_up_success(self, timestamp=123456789) -> str:
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
