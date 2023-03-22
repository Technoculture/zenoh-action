from btree import tree, selector, sequence
import GetTip

class SetTree(tree.Tree):
    def SetupTree(self):
        root = sequence.Sequence([
            selector.Selector([GetTip.TipAvailable()]),
            sequence.Sequence([
                selector.Selector([GetTip.TipAvailableInTray()]),
                selector.Selector([GetTip.MoveTipSliderToPos()])
            ]),
            sequence.Sequence([
                selector.Selector([GetTip.PickUp()]),
                selector.Selector([GetTip.CaughtTipFirmAndOriented()])
            ]),
            selector.Selector([GetTip.PickupSuccess()])
        ])
        return root