from tree import Tree, Selector, Sequence
from node import Node, NodeState

stack: dict = {"pickup":0, "tip_availability":0, "tip": 0}
waiting: int = 0

class pickup(Node):
    def __init__(self):
        super().__init__()
    
    def Evaluate(self) -> NodeState:
        global waiting
        if stack.get("pickup") == 0:
            state = NodeState.RUNNING
            waiting += 1
        elif waiting < 10:
            state = NodeState.RUNNING
            waiting += 1
        elif stack.get("pickup") == 1:
            state = NodeState.SUCCESS
        elif waiting > 10:
            state = NodeState.FAILURE
            waiting = 0
        return state

class tip_availability(Node):
    def __init__(self):
        super().__init__()
    
    def Evaluate(self) -> NodeState:
        global waiting
        if stack.get("tip_availability") == 0:
            stack["pickup"] = 1
            state = NodeState.RUNNING
            waiting += 1
        elif stack.get("tip_availability") == 1:
            state = NodeState.SUCCESS
        elif waiting > 10:
            state = NodeState.FAILURE
            waiting = 0
        elif waiting < 10:
            state = NodeState.RUNNING
            waiting += 1
        return state
    
class tip(Node):
    def __init__(self):
        super().__init__()
    
    def Evaluate(self) -> NodeState:
        global waiting
        if stack.get("tip") == 0:
            stack["tip_availability"] = 1
            state = NodeState.RUNNING
            waiting += 1
        elif stack.get("tip") == 1:
            state = NodeState.SUCCESS
        elif waiting > 10:
            state = NodeState.FAILURE
            waiting = 0
        elif waiting < 10:
            state = NodeState.RUNNING
            waiting += 1
        return state
    
class SetTree(Tree):
    def SetupTree(self):
        # Create the tree structure
        root = Selector([pickup(), 
                         Sequence([tip_availability(), tip()])])
        return root