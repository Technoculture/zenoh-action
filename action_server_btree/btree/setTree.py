from tree import Tree, Selector, Sequence
from node import Node, NodeState

class pickup(Node):
    def __init__(self):
        super().__init__()
    
    def Evaluate(self) -> NodeState:
        print("pickup")
        state = NodeState.RUNNING
        return state

class tip_availability(Node):
    def __init__(self):
        super().__init__()
    
    def Evaluate(self) -> NodeState:
        print("tip_availability")
        count = 1
        if count == 0:
            state = NodeState.SUCCESS
        else:
            state = NodeState.RUNNING
        return state
    
class tip(Node):
    def __init__(self):
        super().__init__()
    
    def Evaluate(self) -> NodeState:
        print("tip")
        count = 1
        if count == 0:
            state = NodeState.SUCCESS
        else:
            state = NodeState.RUNNING
        return state

class SetTree(Tree):
    def SetupTree(self):
        # Create the tree structure
        root = Selector([pickup(), 
                         Sequence([tip_availability(), tip()])])
        return root

if __name__ == "__main__":
    tree = SetTree()
    tree.Start()
    root = tree.SetupTree()
    value = root.Evaluate()
    print(value)
    _value = root.Evaluate()
    print(_value)