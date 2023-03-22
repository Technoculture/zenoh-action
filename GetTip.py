from typing import Protocol, Dict
from btree.node import Node, NodeState
import zenoh
import json
import time

class GetTip(Protocol):
    def Evaluate(self):
        pass

def get_status(key_expression: str) -> Dict[str, str]:
    """
    Get status of the node from hardware modules through zenoh.
    """
    session = zenoh.open(zenoh.Config())
    replies = session.get(key_expression, zenoh.Queue(), zenoh.QueryTarget.ALL())
    for reply in replies:
        return json.loads(reply.ok.payload.decode("utf-8"))
    return {}

class TipAvailable(Node):
    def Evaluate(self):
        keyexpression = "TipRm/trigger?timestamp={}&event=tip_available".format(time.time())
        result = get_status(keyexpression)
        if result != {}:
            if result["response_type"] == NodeState.SUCCESS:
                state = NodeState.SUCCESS
            else:
                state = NodeState.FAILURE
        else:
            state = NodeState.FAILURE
        return state

class TipAvailableInTray(Node):
    def Evaluate(self):
        keyexpression = "TipRm/trigger?timestamp={}&event=tip_available_in_tray".format(time.time())
        result = get_status(keyexpression)
        if result != {}:
            if result["response_type"] == NodeState.SUCCESS:
                state = NodeState.SUCCESS
            else:
                state = NodeState.FAILURE
        else:
            state = NodeState.FAILURE
        return state

class MoveTipSliderToPos(Node):
    def Evaluate(self):
        keyexpression = "TipRm/trigger?timestamp={}&event=move_tip_slider_to_pos".format(time.time())
        result = get_status(keyexpression)
        if result != {}:
            if result["response_type"] == NodeState.SUCCESS:
                state = NodeState.SUCCESS
            else:
                state = NodeState.FAILURE
        else:
            state = NodeState.FAILURE
        return state

class PickUp(Node):
    def Evaluate(self):
        keyexpression = "Orchestrator/trigger?timestamp={}&event=pick_up".format(time.time())
        result = get_status(keyexpression)
        if result != {}:
            if result["response_type"] == NodeState.SUCCESS:
                state = NodeState.SUCCESS
            else:
                state = NodeState.FAILURE
        else:
            state = NodeState.FAILURE
        return state

class CaughtTipFirmAndOriented(Node):
    def Evaluate(self):
        keyexpression = "TipChecker/trigger?timestamp={}&event=caught_tip_firm_and_orient".format(time.time())
        _keyexpression = "Orchestrator/trigger?timestamp={}&event=caught_tip_firm_and_oriented".format(time.time())
        result = get_status(keyexpression)
        _result = get_status(_keyexpression)
        if result != {} and _result != {}:
            if result["response_type"] == NodeState.SUCCESS and _result["response_type"] == NodeState.SUCCESS:
                state = NodeState.SUCCESS
            else:
                state = NodeState.FAILURE
        else:
            state = NodeState.FAILURE
        return state

class PickupSuccess(Node):
    def Evaluate(self):
        keyexpression = "TipRm/trigger?timestamp={}&event=pick_up_success".format(time.time())
        result = get_status(keyexpression)
        if result != {}:
            if result["response_type"] == NodeState.SUCCESS:
                state = NodeState.SUCCESS
            else:
                state = NodeState.FAILURE
        else:
            state = NodeState.FAILURE
        return state