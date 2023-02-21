from typing import TypeVar, Generic, List
from enum import Enum, auto

BehaviorTree = TypeVar("BehaviorTree")

class NodeState(Enum):
    SUCCESS = auto()
    FAILURE = auto()
    RUNNING = auto()

class Node(Generic[BehaviorTree]):
    state: NodeState
    def __init__(self, child = [], parent = None):
        self.parent: Node = parent
        self.children: List[Node] = []
        self.datacontext: dict[str, object] = {}
        if child != []:
            self.AddChild(child)

    def AddChild(self, child) -> None:
        for child_ in child:
            self.AttachChild(child_)
    
    def AttachChild(self, child) -> None:
        self.children.append(child)
        self.parent = child
    
    def Evaluate(self, node, timestamp) -> str:
        ...
    
    def setData(self, key: str, value: object) -> None:
        self.datacontext[key] = value

    def getData(self, key:str):
        value: object = None
        if (self.datacontext.get(key) != None):
            value = self.datacontext.get(key)
            return value
        
        node = self.parent
        while node != None:
            value = node.getData(key)
            if value != None:
                return value
            node = node.parent
        return None

    def clearData(self, key: str) -> bool:
        if self.datacontext.get(key) != None:
            self.datacontext.pop(key)
            return True
        node = self.parent
        while node != None:
            cleared = node.clearData(key)
            if cleared:
                return True
            node = node.parent
        return False
        

