from enum import Enum
from typing import Union

class NodeState(Enum):
    """The state of a node."""
    RUNNING = 0
    SUCCESS = 1
    FAILURE = 2
    EXCEPTION =3
    ERROR = 4

class Node:
    "A node in behaviour tree."
    state: NodeState
    parent: object
    children: list = []
    _datacontext: dict[str, Union[object, int]] = {}

    def __init__(self, children = []):
        Node.parent = None
        for c in children:
            self._Attach(c)

    def _Attach(self, node):
        Node.parent = self
        Node.children.append(node)
    
    def Evaluate(self, _node, _timestamp) -> NodeState:
        ...
    
    def setData(self, key: str, value: Union[object, int]) -> None:
        Node._datacontext[key] = value

    def getData(self, key: str) -> Union[object, int]:
        value = None
        _value = Node._datacontext.get(key)
        if _value != None:
            value = _value
            return value
        
        node = Node.parent
        while node != None:
            value = node.getData(key) #type: ignore
            if value != None:
                return value
            node = node.parent #type: ignore
        return None
    
    def clearData(self) -> None:
        Node._datacontext.clear()