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

    def __init__(self, name=""):
        # Initialize the node.

        self.name = name
        Node.parent = None

    def _Attach(self, node):
        # Attach a child node to this node.
        for child in node.name:
            Node.children.append(child)
        if node.parent == None:
            Node.parent = self
    
    def AddChild(self, children):
        # Add a child node to this node.
        for child in children:
            self._Attach(child)

    def Evaluate(self, _node, _timestamp) -> NodeState:
        # Evaluate the node. Overidden Function
        ...
    
    def setData(self, key: str, value: Union[object, int]) -> None:
        # Set the data in the datacontext.
        Node._datacontext[key] = value

    def getData(self, key: str) -> Union[object, int]:
        # Get the data from the datacontext.
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
        return 0
    
    def clearData(self) -> None:
        # Clear the data in the datacontext.
        Node._datacontext.clear()