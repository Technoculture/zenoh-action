from typing import Protocol, Dict
from btree.node import Node, NodeState
import zenoh
import json

class Hardware_module(Protocol):
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

class DiscardCurrentTray(Node):
    def Evaluate(self):
        keyexpression = "TipRm/trigger?timestamp=123456789&event=discard_current_tray"
        result = get_status(keyexpression)
        if result != {}:
            if result["response_type"] == NodeState.SUCCESS:
                state = NodeState.SUCCESS
            else:
                state = NodeState.FAILURE
        else:
            state = NodeState.FAILURE
        return state

class DiscardSuccess(Node):
    def Evaluate(self):
        keyexpression = "Pipette/trigger?timestamp=123456789&event=discard_success"
        result = get_status(keyexpression)
        if result != {}:
            if result["response_type"] == NodeState.SUCCESS:
                state = NodeState.SUCCESS
            else:
                state = NodeState.FAILURE
        else:
            state = NodeState.FAILURE
        return state

class TrayAvailable(Node):
    def Evaluate(self):
        keyexpression = "TipRm/trigger?timestamp=123456789&event=tray_available"
        result = get_status(keyexpression)
        if result != {}:
            if result["response_type"] == NodeState.SUCCESS:
                state = NodeState.SUCCESS
            else:
                state = NodeState.FAILURE
        else:
            state = NodeState.FAILURE
        return state

class SliderMoveToLoad(Node):
    def Evaluate(self):
        keyexpression = "TipRm/trigger?timestamp=123456789&event=slider_move_to_load"
        result = get_status(keyexpression)
        if result != {}:
            if result["response_type"] == NodeState.SUCCESS:
                state = NodeState.SUCCESS
            else:
                state = NodeState.FAILURE
        else:
            state = NodeState.FAILURE
        return state

class LoadNextTray(Node):
    def Evaluate(self):
        keyexpression = "TipRm/trigger?timestamp=123456789&event=load_next_tray"
        result = get_status(keyexpression)
        if result != {}:
            if result["response_type"] == NodeState.SUCCESS:
                state = NodeState.SUCCESS
            else:
                state = NodeState.FAILURE
        else:
            state = NodeState.FAILURE
        return state

class LoadSuccess(Node):
    def Evaluate(self):
        keyexpression = "Pipette/trigger?timestamp=123456789&event=load_success"
        result = get_status(keyexpression)
        if result != {}:
            if result["response_type"] == NodeState.SUCCESS:
                state = NodeState.SUCCESS
            else:
                state = NodeState.FAILURE
        else:
            state = NodeState.FAILURE
        return state
    
class AlreadyInPos(Node):
    def Evaluate(self):
        keyexpression = "TipRm/trigger?timestamp=123456789&event=already_in_pos"
        result = get_status(keyexpression)
        if result != {}:
            if result["response_type"] == NodeState.SUCCESS:
                state = NodeState.SUCCESS
            else:
                state = NodeState.FAILURE
        else:
            state = NodeState.FAILURE
        return state
    
class MoveTipSlider(Node):
    def Evaluate(self):
        keyexpression = "TipRm/trigger?timestamp=123456789&event=move_tip_slider"
        result = get_status(keyexpression)
        if result != {}:
            if result["response_type"] == NodeState.SUCCESS:
                state = NodeState.SUCCESS
            else:
                state = NodeState.FAILURE
        else:
            state = NodeState.FAILURE
        return state
    
class SliderReached(Node):
    def Evaluate(self):
        keyexpression = "TipRm/trigger?timestamp=123456789&event=slider_reached"
        result = get_status(keyexpression)
        if result != {}:
            if result["response_type"] == NodeState.SUCCESS:
                state = NodeState.SUCCESS
            else:
                state = NodeState.FAILURE
        else:
            state = NodeState.FAILURE
        return state

class GoToDiscardPos(Node):
    def Evaluate(self):
        keyexpression = "Orchestrator/trigger?timestamp=123456789&event=goto_discard_position"
        result = get_status(keyexpression)
        if result != {}:
            if result["response_type"] == NodeState.SUCCESS:
                state = NodeState.SUCCESS
            else:
                state = NodeState.FAILURE
        else:
            state = NodeState.FAILURE
        return state
    
class PrepareToDiscard(Node):
    def Evaluate(self):
        keyexpression = "TipRm/trigger?timestamp=123456789&event=prepare_to_discard"
        result = get_status(keyexpression)
        if result != {}:
            if result["response_type"] == NodeState.SUCCESS:
                state = NodeState.SUCCESS
            else:
                state = NodeState.FAILURE
        else:
            state = NodeState.FAILURE
        return state
    
class EjectTip(Node):
    def Evaluate(self):
        keyexpression = "Pipette/trigger?timestamp=123456789&event=eject_tip"
        result = get_status(keyexpression)
        if result != {}:
            if result["response_type"] == NodeState.SUCCESS:
                state = NodeState.SUCCESS
            else:
                state = NodeState.FAILURE
        else:
            state = NodeState.FAILURE
        return state

class RetryCountBelowThreshold(Node):
    def Evaluate(self):
        return NodeState.FAILURE
    
class DiscardTipSuccess(Node):
    def Evaluate(self):
        keyexpression = "Pipette/trigger?timestamp=123456789&event=discard_tip_success"
        _keyexpression = "TipChecker/trigger?timestamp=123456789&event=discard_tip_success"
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