from tree import Tree, Selector, Sequence

class SetTree(Tree):
    def SetupTree(self):
        # Create the tree structure
        load_new_tray = Selector(["tray_available", Sequence(["slider_move_to_load", "load_next_tray"])])
        discard_tip = Sequence(["goto_discard_position", "prepare_to_discard", "eject_tip", Selector(["discard_tip_success", "retry_count_below_threshold"])])
        tip_available_in_tray = Selector(["load_success", Sequence([load_new_tray, Selector(["discard_success", "discard_current_tray"])])])
        move_tip_slider_to_pos = Selector(["already_in_pos", Sequence(["move_tip_slider", Selector(["slider_reached"])])])
        caught_tip_firm_and_orient = Sequence([discard_tip])
        prepare_tip_for_pickup = Selector([tip_available_in_tray, move_tip_slider_to_pos])
        pickup_using_orchestrator = Sequence(["pickup", Selector([caught_tip_firm_and_orient])])
        root = Selector(["tip_available", Sequence([prepare_tip_for_pickup, pickup_using_orchestrator]), Selector(["pickup_success"])])

        return root
    
if __name__ == "__main__":
    # Create the tree
    tree = SetTree()
    root = tree.SetupTree()
    child = root.children
    print(child)