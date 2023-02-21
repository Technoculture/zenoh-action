from typing import Protocol
from node import Node #type: ignore
from zenoh import QueryTarget #type: ignore
import logging
import zenoh #type: ignore

logging.getLogger().setLevel(logging.DEBUG)

count = -1

def get_status(key_expression: str):
    session = zenoh.open(zenoh.Config())
    replies = session.get(key_expression, zenoh.Queue(), QueryTarget.ALL())
    for reply in replies:
        return reply.ok.payload.decode("utf-8")


def decide_hardware_module(node):
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

class Tree(Protocol):
    _root: Node = None #type: ignore
    def SetupTree(self) -> Node:
        ...
    def start(self)-> None:
        ...
    def update(self,node, timestamp) -> None:
        ...

class Monobehaviour():
    _root: Node = None #type: ignore

    def SetupTree(self) -> Node:
        ...

    def start(self) -> None:
        self._root = self.SetupTree()
    
    def update(self) -> None:
        global count
        if self._root != None:
            count -= 1
            if type(self._root) != str:
                self._root = self._root.children[count]
            count = 0
            if type(self._root) == str or self._root.children == None:
                count += 1

class Sequence(Node):
    def __init__(self, children = []):
        Node.__init__(self, child = children)

    def Evaluate(self, node, timestamp = 123456789) -> str:
        value = decide_hardware_module(node)
        if value:
            response = get_status(f"{value}/trigger?timestamp={timestamp}&event={node}")
            if response == None:
                return "Issue with trigger."
        return "Trigger is triggered."

class Selector(Node):
    def __init__(self, children=[]):
        Node.__init__(self, child = children)

    def Evaluate(self, node, timestamp = 123456789) -> str:
        value = decide_hardware_module(node)
        if value:
            response = get_status(f"{value}/trigger?timestamp={timestamp}&event={node}")
            if response == None:
                return "Issue with trigger."
        return "Trigger is triggered."