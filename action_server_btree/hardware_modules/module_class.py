from typing import Protocol
from btree.node import Node, NodeState

class Hardware_module(Protocol):
    def Evaluate(self):
        pass

class DiscardCurrentTray(Node):
    def Evaluate(self):
        return NodeState.SUCCESS

class DiscardSuccess(Node):
    def Evaluate(self):
        return NodeState.SUCCESS

class TrayAvailable(Node):
    def Evaluate(self):
        return NodeState.SUCCESS

class SliderMoveToLoad(Node):
    def Evaluate(self):
        return NodeState.SUCCESS

class LoadNextTray(Node):
    def Evaluate(self):
        return NodeState.SUCCESS

class LoadSuccess(Node):
    def Evaluate(self):
        return NodeState.SUCCESS
    
class AlreadyInPos(Node):
    def Evaluate(self):
        return NodeState.SUCCESS
    
class MoveTipSlider(Node):
    def Evaluate(self):
        return NodeState.SUCCESS
    
class SliderReached(Node):
    def Evaluate(self):
        return NodeState.SUCCESS

class GoToDiscardPos(Node):
    def Evaluate(self):
        return NodeState.SUCCESS
    
class PrepareToDiscard(Node):
    def Evaluate(self):
        return NodeState.SUCCESS
    
class EjectTip(Node):
    def Evaluate(self):
        return NodeState.SUCCESS

class RetryCountBelowThreshold(Node):
    def Evaluate(self):
        return NodeState.FAILURE