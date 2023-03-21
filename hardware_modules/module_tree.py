from btree import Tree, selector, sequence

class Tip_Available_In_Tray(Tree):
    def SetUpTree(self):
        root = sequence.Sequence([
            selector.Selector([DiscardCurrentTray()]),
            selector.Selector([DiscardSuccess()]),
            sequence.Sequence([
                selector.Selector([TrayAvailable()]),
                selector.Selector([SliderMoveToLoad()]),
                selector.Selector([LoadNextTray()])
            ]),
            selector.Selector([LoadSuccess()]),
        ])
        return root

class Move_tip_slider_to_pos(Tree):
    def SetUpTree(self):
        root = sequence.Sequence([
            selector.Selector([AlreadyInPos()]),
            selector.Selector([MoveTipSlider()]),
            selector.Selector([SliderReached()])
        ])

        return root

class Discard_tip_success(Tree):
    def SetUpTree(self):
        root = selector.Selector([RetryCountBelowThreshold()])
        return root

class Caught_tip_firm_and_orient(Tree):
    def SetUpTree(self):
        root = selector.Selector([
            sequence.Sequence([
                selector.Selector([GoToDiscardPos()]),
                selector.Selector([PrepareToDiscard()]),
                selector.Selector([EjectTip()]),
                selector.Selector([DiscardTipSuccess()])
            ])
        ])
        return root
