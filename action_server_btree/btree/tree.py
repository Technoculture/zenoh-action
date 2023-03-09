from node import Node, NodeState
from typing import List
from itertools import islice
from node_class import non_leaf_node, leaf_node

"""Global Variables"""

non_leaf_nodes: List[str] = ["prepare_tip_for_pickup", "pick_up_using_orchestrator", "move_tip_slider_to_pos", "tip_available_in_tray", "caught_tip_firm_and_orient", "load_new_tray", "discard_tip", "discard_tip_success"]
leaf_nodes: List[str] = ["tip_available", "pickup_success", "discard_success", "tray_available", "load_success", "slider_reached", "discard_tip_success", "retry_Count_below_threshold","pick_up", "discard_current_tray", "move_tip_slider", "slider_move_load", "load_next_tray", "goto_discard_pos", "prepare_to_discard", "eject_tip"]
decision_nodes: List[str] = ["tip_available", "pickup_success", "discard_success", "tray_available", "load_success", "slider_reached", "discard_tip_success", "retry_Count_below_threshold"]
current_node: int = 0

class Tree:
    _root: Node = None #type: ignore

    def Start(self):
        Tree._root = self.SetupTree()
    
    def Update(self):
        if Tree._root!=None:
            Tree._root.Evaluate()
    
    def SetupTree(self):
        ...    

class Selector(Node):
    """
    Note:
    Add the returned state to the datacontext dictionary.
    remove loop from the evaluate function.
    return state from the evaluate function.
    """
    def __init__(self, children) -> None:
        super().__init__(children)

    def Evaluate(self, _node, _timestamp) -> NodeState:
        anychildisrunning = False
        global current_node
        print("Current Node: ", current_node)
        for node in islice(Node.children, current_node, Node.children.index(_node)+1):
            """Runs the loop for all the nodes from starting till the given event/node."""
            print(node)
            if node in non_leaf_nodes and type(node) == str:
                """Checks if the given node is non-leaf node. If yes, then it triggers the evaluate function of non-leaf node and returns the state of the non-leaf node."""
                match non_leaf_node().Evaluate(node = _node, timestamp=_timestamp):
                    case NodeState.SUCCESS:
                        state = NodeState.SUCCESS
                        return state
                    case NodeState.RUNNING:
                        anychildisrunning = True
                        state = NodeState.SUCCESS
                        return state
                    case NodeState.ERROR:
                        state = NodeState.ERROR
                        return state
                    case NodeState.EXCEPTION:
                        value = Node().getData("retry_count")
                        if value < 3:
                            Node().setData("retry_count",  value+1)
                            state = NodeState.EXCEPTION
                        else:
                            state = NodeState.ERROR
                        return state

            elif node in leaf_nodes:
                """Checks if the given node is leaf node. If yes, then it triggers the evaluate function of leaf node and returns the state of the leaf node."""
                print(node)
                match leaf_node().Evaluate(node = _node, timestamp=_timestamp):
                    case NodeState.SUCCESS:
                        state = NodeState.SUCCESS
                        return NodeState.SUCCESS
                    case NodeState.ERROR:
                        state = NodeState.ERROR
                        return state
                    case NodeState.EXCEPTION:
                        value = Node().getData("retry_count")
                        if value < 3:
                            Node().setData("retry_count",  value+1)
                            state = NodeState.EXCEPTION
                        else:
                            state = NodeState.ERROR
                        return state
        state = NodeState.RUNNING if anychildisrunning else NodeState.FAILURE
        current_node = Node.children.index(_node)
        print("Current Node: ", current_node)
        return state