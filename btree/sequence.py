from btree.node import Node, NodeState # type: ignore

class Sequence(Node):
    """
    Evaluate the children which doesn't need hardware validation.
    """
    def __init__(self, children) -> None:
        super().__init__(children)

    def Evaluate(self) -> NodeState:
        anychildisrunning = False
        for child in self.children:
            childStatus = child.Evaluate()
            if childStatus == NodeState.FAILURE:
                state = NodeState.FAILURE
                return state
            elif childStatus == NodeState.SUCCESS:
                continue
            elif childStatus == NodeState.RUNNING:
                anychildisrunning = True
                continue
            else:
                state = NodeState.SUCCESS
                return state
            
        state = NodeState.RUNNING if anychildisrunning else NodeState.SUCCESS
        return state