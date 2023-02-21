from tree import Monobehaviour, Sequence, Selector #type: ignore

class SetTree(Monobehaviour):
    def SetupTree(self):
        discard_tip_success = Selector(["retry_count_below_threshold"])
        discard_tip = Sequence(["goto_discard_position", "prepare_to_discard", "eject_tip", discard_tip_success])
        load_new_tray = Sequence(["slider_move_to_load", "load_next_tray, tray_avaialble"])
        tip_available_in_tray = Sequence(["discard_current_tip", "discard_sucess", load_new_tray, "load_sucess"])
        move_tip_slider_to_pos = Selector(["slider_reached", "move_tip_slider", "already_in_pos"])
        caught_tip_firm_and_orient = Sequence([discard_tip])
        prepare_tip_for_pickup = Sequence([move_tip_slider_to_pos, tip_available_in_tray])
        pickup_using_orchestrator = Sequence([caught_tip_firm_and_orient, "pick_up"])
        get_Tip = Sequence(["pickup_success", pickup_using_orchestrator, prepare_tip_for_pickup, "tip_available"])
        return get_Tip
