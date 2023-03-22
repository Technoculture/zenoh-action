from typing import Protocol, Iterator
from contextlib import contextmanager
import module_tree
import logging
import time
import zenoh # type: ignore

logging.getLogger().setLevel(logging.DEBUG)

class TipRM(Protocol):
    def tip_available(self) -> str:
        ...

    def tip_available_in_tray(self) -> str:
        ...

    def discard_current_tray(self) -> str:
        ...

    def tray_available(self) -> str:
        ...

    def slider_move_to_load(self) -> str:
        ...

    def load_next_tray(self) -> str:
        ...
    
    def prepare_to_discard(self) -> str:
        ...

    def move_tip_slider(self) -> str:
        ...
    
    def pickup_success(self) -> str:
        ...
    
    def move_tip_slider_to_pos(self) -> str:
        ...
    
    def slider_reached(self) -> str:
        ...
    
    def already_in_pos(self) -> str:
        ...

class Tip_rm:
    def tip_available(self) -> str:
        if module_tree.node.Node.getData("Tipcount") > 0:
            return "Accepted"
        else:
            return "No tips available."

    def tip_available_in_tray(self) -> str:
        if module_tree.node.Node.getData("TipTraycount") > 0:
            tipavailableintray = module_tree.Tip_available_in_tray()
            root = tipavailableintray.SetUpTree()
            result = root.Evaluate()
            if result == module_tree.node.NodeState.SUCCESS:
                return "Accepted"
            else:
                return result
        else:
            return "No tips available in tray."

    def discard_current_tray(self) -> str:
        return "Accepted"

    def tray_available(self) -> str:
        if module_tree.node.Node.getData("Traycount") > 0:
            return "Accepted"
        else:
            return "No trays available."

    def slider_move_to_load(self) -> str:
        return "Accepted"

    def load_next_tray(self) -> str:
        return "Accepted"
    
    def prepare_to_discard(self) -> str:
        return "Accepted"

    def move_tip_slider_to_pos(self) -> str:
        movetipslidertopos = module_tree.Move_tip_slider_to_pos()
        root = movetipslidertopos.SetUpTree()
        result = root.Evaluate()
        if result == module_tree.node.NodeState.SUCCESS:
            return "Accepted"
        else:
            return "Problem in moving tip slider to position."
    
    def pickup_success(self) -> str:
        return "Accepted"
    
    def move_tip_slider(self) -> str:
        return "Accepted"
    
    def slider_reached(self) -> str:
        return "Accepted"
    
    def already_in_pos(self) -> str:
        return "Accepted"

class Queryable:
    def __init__(self, Tip_rm: TipRM) -> None:
        self.Tip_rm = Tip_rm
        
    def check_status(self, node: TipRM, event: str) -> str:
        return node.__getattribute__(event)()

    def trigger_queryable_handler(self, query: zenoh.Query) -> None:
        try:
            logging.debug("Received query: {}".format(query.selector))
            event = query.selector.decode_parameters()
            result = self.check_status(self.Tip_rm, event['event'])
            if result == "Accepted":
                payload = {"response_type":"Accepted","response":result}
            else:
                raise ValueError(result)
        except ValueError as e:
            payload = {"response_type":"Rejected","response":"{}".format(e)}
        query.reply(zenoh.Sample("TipRM/trigger", payload))

class Session:
    def __init__(self, handler: Queryable) -> None:
        self.handler = handler
    def open(self):
        self.config = zenoh.Config()
        self.session = zenoh.open(self.config)
        self.trigger_queryable = self.session.declare_queryable("TipRM/trigger", self.handler.trigger_queryable_handler)
    def close(self):
        self.session.close()
        self.trigger_queryable.undeclare()    
    
@contextmanager
def session_manager(handler: Queryable) -> Iterator[Session]:
    try:
        session = Session(handler)
        session.open()
        yield session
    except KeyboardInterrupt:
        logging.error("Interrupted by user")
    finally:
        session.close()

if __name__ == "__main__":
    tip_rm = Tip_rm()
    handler = Queryable(tip_rm)
    with session_manager(handler) as session:
        logging.debug("Tip RM Started...")
        while True:
            time.sleep(1)