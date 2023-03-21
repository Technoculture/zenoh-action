from btree import Tree, selector, sequence
import GetTip

class SetTree(Tree):
    def SetupTree(self):
        root = sequence.Sequence([
            selector.Selector([GetTip.TipAvailable()]),
            sequence.Sequence([
                selector.Selector([GetTip.TipAvailableInTray()]), 
                GetTip.MoveTipSliderToPos()
            ]),
            sequence.Sequence([
                selector.Selector([GetTip.PickUp()]),
                selector.Selector([GetTip.CaughtTipFirmAndOriented()]),
            ]),
            selector.Selector([GetTip.PickupSuccess()])
        ])

if __name__ == "__main__":
    tree = SetTree()
    print(tree.SetupTree())
    
    