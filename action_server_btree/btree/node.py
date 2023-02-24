from enum import Enum

class NodeState(Enum):
    """The state of a node."""
    RUNNING = 0
    SUCCESS = 1
    FAILURE = 2

class Node:
    "A node in behaviour tree."
    state: NodeState
    parent: object
    children: list = []
    _datacontext: dict[str, object] = {}

    def __init__(self, children = []):
        Node.parent = None
        for c in children:
            self._Attach(c)

    def _Attach(self, node):
        Node.parent = self
        Node.children.append(node)
    
    def Evaluate(self) -> NodeState:
        ...
    
    def setData(self, key: str, value: object) -> None:
        Node._datacontext[key] = value

    def getData(self, key: str) -> object:
        value = None
        _value = Node._datacontext.get(key)
        if _value != None:
            value = _value
            return value
        
        node = Node.parent
        while node != None:
            value = node.getData(key)
            if value != None:
                return value
            node = node.parent
        return None
    

