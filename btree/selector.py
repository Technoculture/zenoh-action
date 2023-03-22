from btree.node import Node, NodeState

class Selector(Node):
    """
    Evaluate the children which needs hardware validation.
    """
    def __init__(self, children) -> None:
        super().__init__(children)
    
    def Evaluate(self) -> NodeState:
        for child in self.children:
            childStatus = child.Evaluate()
            if childStatus == NodeState.FAILURE:
                continue
            elif childStatus == NodeState.SUCCESS:
                state = NodeState.SUCCESS
                return state
            elif childStatus == NodeState.RUNNING:
                state = NodeState.RUNNING
                return state
            else:
                continue
        state = NodeState.FAILURE
        return state