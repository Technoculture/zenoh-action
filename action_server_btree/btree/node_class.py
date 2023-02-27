from typing import Any
from node import Node, NodeState

"""Global Variables"""
leaf_dict: list = []

class non_leaf_node(Node):
    def __init__(self) -> None:
        super().__init__()

    def Evaluate(self, node: Any, timestamp: str) -> NodeState:
        if Node().getData(node) == "NodeState.RUNNING":
            leaf_node_exists = Node.children[Node.children.index(node) + 1]
            if leaf_node_exists in leaf_dict:
                Node().setData(node, "NodeState.SUCCESS")
                return NodeState.SUCCESS
            return NodeState.RUNNING
        elif Node().getData(node) == None:
            Node().setData(node, "NodeState.RUNNING")
            return NodeState.RUNNING
        else:
            Node().setData(node, "NodeState.FAILURE")
            return NodeState.FAILURE
        
class leaf_node(Node):
    def __init__(self) -> None:
        super().__init__()

    def Evaluate(self, node: Any, timestamp: Any) -> NodeState:
        return NodeState.SUCCESS
    
