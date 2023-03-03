from tree import Tree, Selector, Sequence

class SetTree(Tree):
    def SetupTree(self):
        # Create the tree structure
        root = Selector(["get_tip"])
        level1 = Sequence(["prepare_tray", "discard_success", Selector(["tip_available"]), Selector(["pickup_success"])])
        level2_1 = Selector(["tip_available_in_tray"])
        level3_1 = Sequence(["discard_current_tray", Selector(["discard_success"])])
        level3_2 = Sequence(["pick_up", Selector(["pickup_success"])])
        return root

if __name__ == "__main__":
    tree = SetTree()
    root = tree.SetupTree()
    print(root.children)