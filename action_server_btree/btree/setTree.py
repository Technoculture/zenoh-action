from tree import Tree, Selector
from node import Node

class SetTree(Tree):
    def SetupTree(self):
        # Define level nodes of tree
        root = Selector(["get_tip"])
        level1 = Selector(["tip_available"])
        level2 = Selector(["prepare_tip_for_pickup"])
        level2_1 = Selector(["tip_available_in_tray"])
        level2_1_1 = Selector(["discard_current_tray"])
        level2_1_2 = Selector(["discard_success"])
        level2_1_3 = Selector(["load_new_tray"])
        level2_1_3_1 = Selector(["tray_available"])
        level2_1_3_2 = Selector(["slider_move_to_load"])
        level2_1_3_3 = Selector(["load_next_tray"])
        level2_1_4 = Selector(["load_success"])
        level2_2 = Selector(["move_tip_slider_to_pos"])
        level2_2_1 = Selector(["already_in_position"])
        level2_2_2 = Selector(["move_tip_slider"])
        level2_2_3 = Selector(["slider_reached"])
        level3 = Selector(["pick_up_using_orchestrator"])
        level3_1 = Selector(["pickup"])
        level3_2 = Selector(["caught_tip_firm_and_orient"])
        level3_2_1 = Selector(["discard_tip"])
        level3_2_1_1 = Selector(["goto_discard_position"])
        level3_2_1_2 = Selector(["prepare_to_discard"])
        level3_2_1_3 = Selector(["eject_tip"])
        level3_2_1_4 = Selector(["discard_tip_success"])
        level3_2_1_4_1 = Selector(["retry_count_below_threshold"])
        level4 = Selector(["pickup_success"])

        # Setup parent-child relationships
        
        root.AddChild([root, level1, level2, level2_1, level2_1_1, level2_1_2, level2_1_3, 
                       level2_1_3_1, level2_1_3_2, level2_1_3_3, level2_1_4, level2_2, level2_2_1, 
                       level2_2_2, level2_2_3, level3, level3_1, level3_2, level3_2_1, level3_2_1_1, 
                       level3_2_1_2, level3_2_1_3, level3_2_1_4, level3_2_1_4_1, level4])
        
        return root

if __name__ == "__main__":
    tree = SetTree()
    value = 0
    root = tree.SetupTree()
    print(root.children)
    print(type(value))