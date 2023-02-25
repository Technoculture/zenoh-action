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

class Sequence(Node):
    def __init__(self, children):
        super().__init__(children)

    def Evaluate(self) -> NodeState:
        anychildisrunning = False
        for node in Node.children:
            match node.Evaluate():
                case NodeState.FAILURE:
                    state = NodeState.FAILURE
                    return state
                case NodeState.SUCCESS:
                    return NodeState.SUCCESS
                case NodeState.RUNNING:
                    anychildisrunning = True
                    Node.parent=node
                    continue
                case _ :
                    state = NodeState.SUCCESS
                    return state
        state = NodeState.RUNNING if anychildisrunning else NodeState.SUCCESS
        return state
class Selector(Node):
    def __init__(self, children):
        super().__init__(children)

    def Evaluate(self) -> NodeState:
        anychildisrunning = False
        for node in Node.children:
            match node.Evaluate():
                case NodeState.FAILURE:
                    return NodeState.FAILURE
                case NodeState.SUCCESS:
                    state = NodeState.SUCCESS
                    return NodeState.SUCCESS
                case NodeState.RUNNING:
                    anychildisrunning = True
                    continue
                case _ :
                    state = NodeState.SUCCESS
                    return NodeState.SUCCESS
        state = NodeState.RUNNING if anychildisrunning else NodeState.FAILURE
        return state