from typing import Protocol, Dict
from btree.node import Node, NodeState # type: ignore
import zenoh # type: ignore
import json
import time
import logging

logging.getLogger().setLevel(logging.DEBUG)

class Node_class(Protocol):
    def Evaluate(self):
        pass

def get_status(key_expression: str) -> Dict[str, str]:
    """
    Get status of the node from hardware modules through zenoh.
    """
    session = zenoh.open(zenoh.Config())
    replies = session.get(key_expression, zenoh.Queue(), zenoh.QueryTarget.ALL())
    for reply in replies:
        try:
            value = json.loads(reply.ok.payload.decode("utf-8"))
        except:
            value = json.loads(reply.err.payload.decode("utf-8"))
        return value
    #session.close()
    return {}

class Intake_new_sample(Node):
    def Evaluate(self):
        logging.debug("Intake_new_Sample")
        state = NodeState.SUCCESS
        return state
    
class Sample_quality_check(Node):
    def Evaluate(self):
        logging.debug("Sample_quality_check")
        state = NodeState.SUCCESS
        return state
    
class Sample_purification(Node):
    def Evaluate(self):
        logging.debug("Sample_purification")
        state = NodeState.SUCCESS
        return state

class Sample_processing(Node):
    def Evaluate(self):
        logging.debug("Sample_processing")
        state = NodeState.SUCCESS
        return state

class Detection(Node):
    def Evaluate(self):
        logging.debug("Detection")
        state = NodeState.SUCCESS
        return state
    
class Result_and_cleanup(Node):
    def Evaluate(self):
        logging.debug("Result_and_cleanup")
        state = NodeState.SUCCESS
        return state

class TipAvailable(Node):
    def Evaluate(self):
        keyexpression = "TipRm/trigger?timestamp={}&event=tip_available".format(time.time())
        result = get_status(keyexpression)
        print(result)
        if result != {}:
            if result["response_type"] == "Accepted":
                state = NodeState.SUCCESS
            else:
                state = NodeState.FAILURE
        else:
            state = NodeState.FAILURE
        logging.debug("TipAvailable: {}".format(state))
        return state

class TipAvailableInTray(Node):
    def Evaluate(self):
        logging.debug("TipAvailableInTray")
        keyexpression = "TipRm/trigger?timestamp={}&event=tip_available_in_tray".format(time.time())
        result = get_status(keyexpression)
        print(result)
        if result != {}:
            if result["response_type"] == "Accepted":
                state = NodeState.SUCCESS
            else:
                state = NodeState.FAILURE
        else:
            state = NodeState.FAILURE
        logging.debug("TipAvailableInTray: {}".format(state))
        return state

class MoveTipSliderToPos(Node):
    def Evaluate(self):
        logging.debug("MoveTipSliderToPos")
        keyexpression = "TipRm/trigger?timestamp={}&event=move_tip_slider_to_pos".format(time.time())
        result = get_status(keyexpression)
        print(result)
        if result != {}:
            if result["response_type"] == "Accepted":
                state = NodeState.SUCCESS
            else:
                state = NodeState.FAILURE
        else:
            state = NodeState.FAILURE
        logging.debug("MoveTipSliderToPos: {}".format(state))
        return state

class PickUp(Node):
    def Evaluate(self):
        logging.debug("PickUp")
        keyexpression = "Orchestrator/trigger?timestamp={}&event=pick_up".format(time.time())
        result = get_status(keyexpression)
        print(result)
        if result != {}:
            if result["response_type"] == "Accepted":
                state = NodeState.SUCCESS
            else:
                state = NodeState.FAILURE
        else:
            state = NodeState.FAILURE
        logging.debug("PickUp: {}".format(state))
        return state

class CaughtTipFirmAndOriented(Node):
    def Evaluate(self):
        logging.debug("CaughtTipFirmAndOriented")
        keyexpression = "TipChecker/trigger?timestamp={}&event=caught_tip_firm_and_orient".format(time.time())
        _keyexpression = "Orchestrator/trigger?timestamp={}&event=caught_tip_firm_and_oriented".format(time.time())
        result = get_status(keyexpression)
        _result = get_status(_keyexpression)
        print(result)
        if result != {} and _result != {}:
            if result["response_type"] == "Accepted" and _result["response_type"] == "Accepted":
                state = NodeState.SUCCESS
            else:
                state = NodeState.FAILURE
        else:
            state = NodeState.FAILURE
        logging.debug("CaughtTipFirmAndOriented: {}".format(state))
        return state

class PickupSuccess(Node):
    def Evaluate(self):
        logging.debug("PickupSuccess")
        keyexpression = "TipRm/trigger?timestamp={}&event=pick_up_success".format(time.time())
        result = get_status(keyexpression)
        print(result)
        if result != {}:
            if result["response_type"] == "Accepted":
                state = NodeState.SUCCESS
            else:
                state = NodeState.FAILURE
        else:
            state = NodeState.FAILURE
        logging.debug("PickupSuccess: {}".format(state))
        return state

class DiscardCurrentTray(Node):
    def Evaluate(self):
        logging.debug("DiscardCurrentTray")
        keyexpression = "TipRm/trigger?timestamp=123456789&event=discard_current_tray"
        result = get_status(keyexpression)
        print("class: {}".format(result))
        if result != {}:
            if result["response_type"] == "Accepted":
                state = NodeState.SUCCESS
            else:
                state = NodeState.FAILURE
        else:
            state = NodeState.FAILURE
        logging.debug("DiscardCurrentTray: {}".format(state))
        return state

class DiscardSuccess(Node):
    def Evaluate(self):
        logging.debug("DiscardSuccess")
        keyexpression = "Pipette/trigger?timestamp=123456789&event=discard_success"
        result = get_status(keyexpression)
        print(result)
        if result != {}:
            if result["response_type"] == "Accepted":
                state = NodeState.SUCCESS
            else:
                state = NodeState.FAILURE
        else:
            state = NodeState.FAILURE
        logging.debug("DiscardSuccess: {}".format(state))
        return state

class TrayAvailable(Node):
    def Evaluate(self):
        logging.debug("TrayAvailable")
        keyexpression = "TipRm/trigger?timestamp=123456789&event=tray_available"
        result = get_status(keyexpression)
        print(result)
        if result != {}:
            if result["response_type"] == "Accepted":
                state = NodeState.SUCCESS
            else:
                state = NodeState.FAILURE
        else:
            state = NodeState.FAILURE
        logging.debug("TrayAvailable: {}".format(state))
        return state

class SliderMoveToLoad(Node):
    def Evaluate(self):
        logging.debug("SliderMoveToLoad")
        keyexpression = "TipRm/trigger?timestamp=123456789&event=slider_move_to_load"
        result = get_status(keyexpression)
        print("class: {}".format(result))
        if result != {}:
            if result["response_type"] == "Accepted":
                state = NodeState.SUCCESS
            else:
                state = NodeState.FAILURE
        else:
            state = NodeState.FAILURE
        logging.debug("SliderMoveToLoad: {}".format(state))
        return state

class LoadNextTray(Node):
    def Evaluate(self):
        logging.debug("LoadNextTray")
        keyexpression = "TipRm/trigger?timestamp=123456789&event=load_next_tray"
        result = get_status(keyexpression)
        print(result)
        if result != {}:
            if result["response_type"] == "Accepted":
                state = NodeState.SUCCESS
            else:
                state = NodeState.FAILURE
        else:
            state = NodeState.FAILURE
        logging.debug("LoadNextTray: {}".format(state))
        return state

class LoadSuccess(Node):
    def Evaluate(self):
        logging.debug("LoadSuccess")
        keyexpression = "Pipette/trigger?timestamp=123456789&event=load_success"
        result = get_status(keyexpression)
        print(result)
        if result != {}:
            if result["response_type"] == "Accepted":
                state = NodeState.SUCCESS
            else:
                state = NodeState.FAILURE
        else:
            state = NodeState.FAILURE
        logging.debug("LoadSuccess: {}".format(state))
        return state
    
class AlreadyInPos(Node):
    def Evaluate(self):
        logging.debug("AlreadyInPos")
        keyexpression = "TipRm/trigger?timestamp=123456789&event=already_in_pos"
        result = get_status(keyexpression)
        print(result)
        if result != {}:
            if result["response_type"] == "Accepted":
                state = NodeState.SUCCESS
            else:
                state = NodeState.FAILURE
        else:
            state = NodeState.FAILURE
        logging.debug("AlreadyInPos: {}".format(state))
        return state
    
class MoveTipSlider(Node):
    def Evaluate(self):
        logging.debug("MoveTipSlider")
        keyexpression = "TipRm/trigger?timestamp=123456789&event=move_tip_slider"
        result = get_status(keyexpression)
        logging.debug("MoveTipSlider result: {} in class".format(result))
        if result != {}:
            if result["response_type"] == "Accepted":
                state = NodeState.SUCCESS
            else:
                state = NodeState.FAILURE
        else:
            state = NodeState.FAILURE
        logging.debug("MoveTipSlider: {}".format(state))
        return state
    
class SliderReached(Node):
    def Evaluate(self):
        logging.debug("SliderReached")
        keyexpression = "TipRm/trigger?timestamp=123456789&event=slider_reached"
        result = get_status(keyexpression)
        print(result)
        if result != {}:
            if result["response_type"] == "Accepted":
                state = NodeState.SUCCESS
            else:
                state = NodeState.FAILURE
        else:
            state = NodeState.FAILURE
        logging.debug("SliderReached: {}".format(state))
        return state

class GoToDiscardPos(Node):
    def Evaluate(self):
        logging.debug("GoToDiscardPos")
        keyexpression = "Orchestrator/trigger?timestamp=123456789&event=goto_discard_position"
        result = get_status(keyexpression)
        print(result)
        if result != {}:
            if result["response_type"] == "Accepted":
                state = NodeState.SUCCESS
            else:
                state = NodeState.FAILURE
        else:
            state = NodeState.FAILURE
        logging.debug("GoToDiscardPos: {}".format(state))
        return state
    
class PrepareToDiscard(Node):
    def Evaluate(self):
        logging.debug("PrepareToDiscard")
        keyexpression = "TipRm/trigger?timestamp=123456789&event=prepare_to_discard"
        result = get_status(keyexpression)
        print(result)
        if result != {}:
            if result["response_type"] == "Accepted":
                state = NodeState.SUCCESS
            else:
                state = NodeState.FAILURE
        else:
            state = NodeState.FAILURE
        logging.debug("PrepareToDiscard: {}".format(state))
        return state
    
class EjectTip(Node):
    def Evaluate(self):
        logging.debug("EjectTip")
        keyexpression = "Pipette/trigger?timestamp=123456789&event=eject_tip"
        result = get_status(keyexpression)
        print(result)
        if result != {}:
            if result["response_type"] == "Accepted":
                state = NodeState.SUCCESS
            else:
                state = NodeState.FAILURE
        else:
            state = NodeState.FAILURE
        logging.debug("EjectTip: {}".format(state))
        return state

class RetryCountBelowThreshold(Node):
    def Evaluate(self):
        logging.debug("RetryCountBelowThreshold")
        return NodeState.FAILURE
    
class DiscardTipSuccess(Node):
    def Evaluate(self):
        logging.debug("DiscardTipSuccess")
        keyexpression = "Pipette/trigger?timestamp=123456789&event=discard_tip_success"
        _keyexpression = "TipChecker/trigger?timestamp=123456789&event=discard_tip_success"
        result = get_status(keyexpression)
        _result = get_status(_keyexpression)
        print(result)
        if result != {} and _result != {}:
            if result["response_type"] == "Accepted" and _result["response_type"] == "Accepted":
                state = NodeState.SUCCESS
            else:
                state = NodeState.FAILURE
        else:
            state = NodeState.FAILURE
        logging.debug("DiscardTipSuccess: {}".format(state))
        return state