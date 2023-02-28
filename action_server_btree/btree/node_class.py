from typing import Any, List
from node import Node, NodeState
from zenoh import QueryTarget # type: ignore
import zenoh # type: ignore

"""Global Variables"""
leaf_nodes: List[str] = ["pick_up", "discard_current_tray", "move_tip_slider", "slider_move_load", "load_next_tray", "goto_discard_pos", "prepare_to_discard", "eject_tip"]

def get_status(key_expression: str):
    session = zenoh.open(zenoh.Config())
    replies = session.get(key_expression, zenoh.Queue(), QueryTarget.ALL())
    for reply in replies:
        return reply.ok.payload.decode("utf-8")

def decide_hardware_module(node):
    hardware_module = False
    tiprm = ["tip_available", "pickup_success", "tip_available_in_tray", "move_tip_slider_to_pos", "diacrd_current_tray", "move_tip_slider", "slider_reached", "tray_available", "slidr_move_to_load", "load_next_tray", "already_in_pos", "prepare_to_discard"]
    tipchecker = ["discard_tip_success", "caught_tip_firm_and_orient"]
    orchestrator = ["pick_up", "caught_tip_firm_and_orient", "goto_diascard_pos", "discard_tip_success"]
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

class non_leaf_node(Node):
    def __init__(self) -> None:
        super().__init__()

    def Evaluate(self, node: Any, timestamp: Any):
        hardware_module = decide_hardware_module(node)
        if hardware_module != False:
            result = get_status(f"{hardware_module}/trigger?timestamp={timestamp}&event={node}")
            if result == "Accepted":
                if Node().getData(node) == "NodeState.RUNNING":
                    leaf_node_exists = Node.children[Node.children.index(node) + 1]
                    if leaf_node_exists in leaf_nodes:
                        Node().setData(node, "NodeState.SUCCESS")
                        state = NodeState.SUCCESS
                        return state
                    state = NodeState.RUNNING
                elif Node().getData(node) == None:
                    Node().setData(node, "NodeState.RUNNING")
                    state = NodeState.RUNNING
                else:
                    Node().setData(node, "NodeState.FAILURE")
                    state = NodeState.FAILURE
            else:
                state = NodeState.FAILURE
            return state

class leaf_node(Node):
    def __init__(self) -> None:
        super().__init__()

    def Evaluate(self, node: Any, timestamp: Any) -> NodeState:
        hardware_module = decide_hardware_module(node)
        if hardware_module != False:
            result = get_status(f"{hardware_module}/trigger?timestamp={timestamp}&event={node}")
            if result == "Accepted":
                state = NodeState.SUCCESS
            elif result == "Error":
                state = NodeState.ERROR
            elif result == "Exception":
                state = NodeState.EXCEPTION
            else:
                state = NodeState.FAILURE
        else:
            state = NodeState.SUCCESS
        return state