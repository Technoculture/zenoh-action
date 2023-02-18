from typing import Protocol, Generic
from node import Node, BehaviorTree, NodeState

class Tree(Protocol):
    _root: Node = None #type: ignore
    def SetupTree(self) -> Node:
        ...
    def start(self)-> None:
        ...
    def update(self) -> None:
        ...

class Monobehaviour(Generic[BehaviorTree]):
    _root: Node = None #type: ignore

    def SetupTree(self) -> Node:
        ...

    def start(self) -> None:
        self._root = self.SetupTree()
    
    def update(self) -> None:
        if self._root != None:
            self._root.Evaluate()


class Sequence(Node, Generic[BehaviorTree]):
    def __init__(self, children = []):
        Node.__init__(child = children)

    def Evaluate(self) -> NodeState:
        self.anyChildisRunning: bool = False
        for node in self.children:
            match node.Evaluate():
                case NodeState.FAILURE:
                    state = NodeState.FAILURE
                    return state
                case NodeState.SUCCESS:
                    continue
                case NodeState.RUNNING:
                    self.anyChildisRunning = True
                    continue
                case _:
                    state = NodeState.SUCCESS
                    return state
        if self.anyChildisRunning:
            state = NodeState.RUNNING
            return state
        else:
            state = NodeState.SUCCESS
            return state

class Selector(Node, Generic[BehaviorTree]):
    def __init__(self, children=[]):
        Node.__init__(children=children)

    def Evaluate(self) -> NodeState:
        for node in self.children:
            match node.Evaluate():
                case NodeState.FAILURE:
                    continue
                case NodeState.SUCCESS:
                    state = NodeState.SUCCESS
                    return state
                case NodeState.RUNNING:
                    state = NodeState.RUNNING
                    return state
                case _:
                    continue
        state = NodeState.FAILURE
        return state