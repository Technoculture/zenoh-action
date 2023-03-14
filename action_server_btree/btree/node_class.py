from typing import Any, List, Dict
from itertools import islice
from node import Node, NodeState
from zenoh import QueryTarget # type: ignore
import zenoh # type: ignore
import json

def get_status(key_expression: str) -> Dict[str, str]:
    """
    Get status of the node from hardware modules through zenoh.
    """
    session = zenoh.open(zenoh.Config())
    replies = session.get(key_expression, zenoh.Queue(), QueryTarget.ALL())
    for reply in replies:
        return json.loads(reply.ok.payload.decode("utf-8"))
    return {}

def decide_hardware_module(node):
    """
    Decide the hardware module based on the node.
    """
    hardware_module = ""

    tiprm = ["tip_available", "pickup_success", "tip_available_in_tray", "move_tip_slider_to_pos", 
             "discard_current_tray", "move_tip_slider", "slider_reached", "tray_available", 
             "slider_move_to_load", "load_next_tray", "already_in_pos", "prepare_to_discard"]
    tipchecker = ["discard_tip_success", "caught_tip_firm_and_orient"]
    orchestrator = ["pick_up", "caught_tip_firm_and_orient", "goto_discard_pos", "discard_tip_success"]
    pipette = ["load_success", "discard_success", "eject_tip", "discard_tip_success"]
    
    if node in tiprm:
        hardware_module = "TipRM"
    elif node in tipchecker:
        hardware_module = "TipChecker"
    elif node in orchestrator:
        hardware_module = "Orchestrator"
    elif node in pipette:
        hardware_module = "Pipette"
    return hardware_module

def check_node_valid(node) -> bool:
    """ Checks if the node is valid or not. """

    if Node()._datacontext == {}:
        Node().setData(node, "Running")
    node_list = islice(Node.children, 0, Node.children.index(node))
    for _node in node_list:
        if _node not in Node()._datacontext.keys():
            return False
    return True

class non_hardware_node(Node):
    def __init__(self) -> None:
        super().__init__()

    def Evaluate(self, node: Any, timestamp: Any) -> NodeState:
        if check_node_valid(node=node):
            if self.getData(node) == "Running":
                self.setData(node, "Success")
                state = NodeState.SUCCESS
            else:
                self.setData(node, "Running")
                state = NodeState.SUCCESS
        else:
            state = NodeState.FAILURE
        return state


class hardware_node(Node):
    def __init__(self) -> None:
        super().__init__()

    def Evaluate(self, node: Any, timestamp: Any) -> NodeState:
        hardware_module = decide_hardware_module(node)
        if check_node_valid(node=node) == False:
            self.setData(node, "Failure")
            state = NodeState.FAILURE
            return state
        if hardware_module != "":
            result = get_status(f"{hardware_module}/trigger?timestamp={timestamp}&event={node}")
            if result != {}:
                if result["response_type"] == "Accepted":
                    self.setData(node, "Success")
                    state = NodeState.SUCCESS
                elif result["response_type"] == "Error":
                    self.setData(node, "Error")
                    state = NodeState.ERROR
                elif result["response_type"] == "Exception":
                    self.setData(node, "Exception")
                    state = NodeState.EXCEPTION
                else:
                    self.setData(node, "Failure")
                    state = NodeState.FAILURE
            else:
                self.setData(node, "No response")
                state = NodeState.FAILURE
        else:
            self.setData(node, "Success")
            state = NodeState.SUCCESS
        return state