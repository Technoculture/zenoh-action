from tree import Tree, Selector, Sequence

class SetTree(Tree):
    def SetupTree(self):
        # Create the tree structure
        n = Selector(["tip_availability"])
        root = Sequence([n,"tip", "pickup", "hello"])
        return root
    
if __name__ == "__main__":
    # Create the tree
    tree = SetTree()
    root = tree.SetupTree()
    child = root.children
    print(child)
    print(root.Evaluate("pickup", "0"))