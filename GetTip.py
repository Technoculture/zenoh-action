from typing import Protocol
from btree.node import Node, NodeState

class GetTip(Protocol):
    def Evaluate(self):
        pass

class TipAvailable(Node):
    def Evaluate(self):
        return NodeState.SUCCESS

class TipAvailableInTray(Node):
    def Evaluate(self):
        return NodeState.SUCCESS

class MoveTipSliderToPos(Node):
    def Evaluate(self):
        return NodeState.SUCCESS

class PickUp(Node):
    def Evaluate(self):
        return NodeState.SUCCESS

class CaughtTipFirmAndOriented(Node):
    def Evaluate(self):
        return NodeState.SUCCESS

class PickupSuccess(Node):
    def Evaluate(self):
        return NodeState.SUCCESS