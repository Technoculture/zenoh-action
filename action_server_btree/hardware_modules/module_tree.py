from btree import Tree, selector, sequence
import module_class

class Tip_Available_In_Tray(Tree):
    def SetUpTree(self):
        root = sequence.Sequence([
            selector.Selector([module_class.DiscardCurrentTray()]),
            selector.Selector([module_class.DiscardSuccess()]),
            sequence.Sequence([
                selector.Selector([module_class.TrayAvailable()]),
                selector.Selector([module_class.SliderMoveToLoad()]),
                selector.Selector([module_class.LoadNextTray()])
            ]),
            selector.Selector([module_class.LoadSuccess()]),
        ])
        return root

class Move_tip_slider_to_pos(Tree):
    def SetUpTree(self):
        root = sequence.Sequence([
            selector.Selector([module_class.AlreadyInPos()]),
            selector.Selector([module_class.MoveTipSlider()]),
            selector.Selector([module_class.SliderReached()])
        ])

        return root

class Discard_tip_success(Tree):
    def SetUpTree(self):
        root = selector.Selector([module_class.RetryCountBelowThreshold()])
        return root

class Caught_tip_firm_and_orient(Tree):
    def SetUpTree(self):
        root = selector.Selector([
            sequence.Sequence([
                selector.Selector([module_class.GoToDiscardPos()]),
                selector.Selector([module_class.PrepareToDiscard()]),
                selector.Selector([module_class.EjectTip()]),
                selector.Selector([module_class.DiscardTipSuccess()])
            ])
        ])
        return root
