from typing import List
from itertools import islice
from node import Node, NodeState
from node_class import non_hardware_node, hardware_node

"""Global Variables"""

non_hardware_nodes: List[str] = ["get_tip", "prepare_tip_for_pickup", "pick_up_using_orchestrator", "move_tip_slider_to_pos", "tip_available_in_tray", "caught_tip_firm_and_orient", "load_new_tray", "discard_tip"]
hardware_nodes: List[str] = ["tip_available", "pickup_success", "discard_success", "tray_available", "load_success", "slider_reached", "discard_tip_success","pick_up", "discard_current_tray", "move_tip_slider", "slider_move_load", "load_next_tray", "goto_discard_pos", "prepare_to_discard", "eject_tip", "discard_tip_success"]
value: int = 0

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
        state = NodeState.FAILURE
        if _node in non_hardware_nodes:
            match non_hardware_node().Evaluate(_node, _timestamp):
                case NodeState.SUCCESS:
                    state = NodeState.SUCCESS
                case NodeState.FAILURE:
                    state = NodeState.FAILURE

        elif _node in hardware_nodes:
            match hardware_node().Evaluate(_node, _timestamp):
                case NodeState.SUCCESS:
                    state = NodeState.SUCCESS
                case NodeState.FAILURE:
                    state = NodeState.FAILURE
                case NodeState.ERROR:
                    state = NodeState.ERROR
                    self.clearData()
        return state

class Exception(Node):
    def __init__(self, children) -> None:
        super().__init__(children)

    def Evaluate(self, _node, _timestamp) -> NodeState:
        state = NodeState.FAILURE
        global value
        if self._datacontext == {}:
            return NodeState.FAILURE
        
        node_list = islice(self.children, 0, self.children.index(_node))

        for _node in node_list:
            if _node not in self._datacontext.keys():
                return NodeState.FAILURE
            
        value = self.getData("count") #type: ignore
        
        if value > 3:
            state = NodeState.ERROR
            self.clearData()
        else:
            self.setData("count", value+1)
            state = NodeState.SUCCESS
        return state