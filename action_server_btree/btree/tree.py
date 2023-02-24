from node import Node, NodeState

class Tree:
    _root: Node = None

    def Start(self):
        Tree._root = self.SetupTree()
    
    def Update(self):
        if Tree._root!=None:
            Tree._root.Evaluate()
    
    def SetupTree(self):
        ...

stack = []

class Sequence(Node):
    def __init__(self, children):
        super().__init__(children)

    def Evaluate(self) -> NodeState:
        anychildisrunning = False
        for node in Node.children:
            match node.Evaluate():
                case NodeState.FAILURE:
                    state = NodeState.FAILURE
                    return "Rejected"
                case NodeState.SUCCESS:
                    return "Accepted"
                case NodeState.RUNNING:
                    anychildisrunning = True
                    Node.parent=node
                    return "Running"
                case _ :
                    state = NodeState.SUCCESS
                    return "Accepted"
        state = "Running" if anychildisrunning else "Accepted"
        return state
    
class Selector(Node):
    def __init__(self, children):
        super().__init__(children)

    def Evaluate(self) -> NodeState:
        anychildisrunning = False
        for node in Node.children:
            match node.Evaluate():
                case NodeState.FAILURE:
                    stack.append(node)
                    return "Rejected"
                case NodeState.SUCCESS:
                    state = NodeState.SUCCESS
                    return "Accepted"
                case NodeState.RUNNING:
                    anychildisrunning = True
                    Node.parent=node
                    return "Running"
                case _ :
                    state = NodeState.SUCCESS
                    return "Accepted"
        state = "Running" if anychildisrunning else "Rejected"
        return state