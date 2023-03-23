from btree import tree, selector, sequence #type: ignore
from btree import btree_classes

class SetTree(tree.Tree):
    def SetupTree(self):
        root = sequence.Sequence([
            selector.Selector([btree_classes.TipAvailable()]),
            sequence.Sequence([
                selector.Selector([btree_classes.TipAvailableInTray()]),
                selector.Selector([btree_classes.MoveTipSliderToPos()])
            ]),
            sequence.Sequence([
                selector.Selector([btree_classes.PickUp()]),
                selector.Selector([btree_classes.CaughtTipFirmAndOriented()])
            ]),
            selector.Selector([btree_classes.PickupSuccess()])
        ])
        return root

class Tip_Available_In_Tray(tree.Tree):
    def SetUpTree(self):
        root = sequence.Sequence([
            selector.Selector([btree_classes.DiscardCurrentTray()]),
            selector.Selector([btree_classes.DiscardSuccess()]),
            sequence.Sequence([
                selector.Selector([btree_classes.TrayAvailable()]),
                selector.Selector([btree_classes.SliderMoveToLoad()]),
                selector.Selector([btree_classes.LoadNextTray()])
            ]),
            selector.Selector([btree_classes.LoadSuccess()]),
        ])
        return root

class Move_tip_slider_to_pos(tree.Tree):
    def SetUpTree(self):
        root = sequence.Sequence([
            selector.Selector([btree_classes.AlreadyInPos()]),
            selector.Selector([btree_classes.MoveTipSlider()]),
            selector.Selector([btree_classes.SliderReached()])
        ])
        return root

class Discard_tip_success(tree.Tree):
    def SetUpTree(self):
        root = selector.Selector([btree_classes.RetryCountBelowThreshold()])
        return root

class Caught_tip_firm_and_orient(tree.Tree):
    def SetUpTree(self):
        root = selector.Selector([
            sequence.Sequence([
                selector.Selector([btree_classes.GoToDiscardPos()]),
                selector.Selector([btree_classes.PrepareToDiscard()]),
                selector.Selector([btree_classes.EjectTip()]),
                selector.Selector([btree_classes.DiscardTipSuccess()])
            ])
        ])
        return root

