from tree import Tree, Selector, Sequence

class SetTree(Tree):
    def SetupTree(self):
        # Create the tree structure
        level1 = Sequence(["get_tip"])
        level1.AddChild([Selector(["tip_available"])])
        level2 = Selector(["pickup_success"])
        level2.AddChild([Sequence(["move_to_tip", "pick_tip"])])
        return level1

if __name__ == "__main__":
    tree = SetTree()
    root = tree.SetupTree()
    print(root.children)