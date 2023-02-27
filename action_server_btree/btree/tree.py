from node import Node, NodeState
from itertools import islice
from node_class import non_leaf_node, leaf_node

non_leaf_dict = ["pickup", "hello"]
leaf_dict = ["tip_availability","tip"]

class Tree:
    _root: Node = None #type: ignore

    def Start(self):
        Tree._root = self.SetupTree()
        current_node = Node.children[0]
    
    def Update(self):
        if Tree._root!=None:
            Tree._root.Evaluate()
    
    def SetupTree(self):
        ...

class Sequence(Node):
    def __init__(self, children):
        super().__init__(children)

    def Evaluate(self, _node, _timestamp) -> NodeState:
        anychildisrunning = False
        for node in islice(Node.children, None, Node.children.index(_node)+1):
            if node in leaf_dict:
                match leaf_node().Evaluate(_node, _timestamp):
                    case NodeState.FAILURE:
                        state = NodeState.FAILURE
                        return state
                    case NodeState.SUCCESS:
                        state = NodeState.SUCCESS
                        continue
                    
            elif node in non_leaf_dict:
                match non_leaf_node().Evaluate(_node, _timestamp):
                    case NodeState.FAILURE:
                        state = NodeState.FAILURE
                        continue
                    case NodeState.SUCCESS:
                        state = NodeState.SUCCESS
                        return state
                    case NodeState.RUNNING:
                        anychildisrunning = True
                        continue
        state = NodeState.RUNNING if anychildisrunning else NodeState.SUCCESS
        return state
    

class Selector(Node):
    def __init__(self, children):
        super().__init__(children)

    def Evaluate(self, _node, _timestamp) -> NodeState:
        anychildisrunning = False

        for node in islice(Node.children, None, Node.children.index(_node)+1):
            if node in non_leaf_dict:
                match non_leaf_node().Evaluate(node = _node, timestamp=_timestamp):
                    case NodeState.FAILURE:
                        state = NodeState.FAILURE
                        return state
                    case NodeState.SUCCESS:
                        state = NodeState.SUCCESS
                        continue
                    case NodeState.RUNNING:
                        anychildisrunning = True
                        continue
                    
            elif node in leaf_dict:
                match leaf_node().Evaluate(node = _node, timestamp=_timestamp):
                    case NodeState.FAILURE:
                        state = NodeState.FAILURE
                        continue
                    case NodeState.SUCCESS:
                        state = NodeState.SUCCESS
                        return NodeState.SUCCESS
        state = NodeState.RUNNING if anychildisrunning else NodeState.FAILURE
        return state