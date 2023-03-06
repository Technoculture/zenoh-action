from tree import Tree, Selector, Sequence

class SetTree(Tree):
    def SetupTree(self):
        # Create the tree structure
        level1 = Sequence(["get_tip"])
        level1.AddChild([Selector(["tip_available", "prepare_tip_for_pickup", "tip_available_in_tray", "discard_current_tray"]), Selector(["pick_up", "move_tip_slider"])])
        level1_2.AddChild([])
        return level1

if __name__ == "__main__":
    tree = SetTree()
    root = tree.SetupTree()
    print(root.children)