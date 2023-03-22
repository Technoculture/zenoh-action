from typing import Protocol, Iterator
from contextlib import contextmanager
import module_tree
import logging
import time
import zenoh  # type: ignore

logging.getLogger().setLevel(logging.DEBUG)

class Orchestrator(Protocol):
    def pick_up(self) -> str:
        ...
    def caught_tip_firm_and_orient(self) -> str:
        ...
    def go_to_discard_position(self) -> str:
        ...
    def discard_tip_success(self) -> str:
        ...

class Orchestrator_:
    def pick_up(self) -> str:
        return "Accepted"
    
    def caught_tip_firm_and_orient(self) -> str:
        caughttipfirmandorient = module_tree.Caught_tip_firm_and_orient()
        root = caughttipfirmandorient.SetUpTree()
        result = root.Evaluate()
        if result == module_tree.node.NodeState.SUCCESS:
            return "Accepted"
        else:
            return result

    def go_to_discard_position(self) -> str:
        return "Accepted"
    
    def discard_tip_success(self) -> str:
        discardtipsuccess = module_tree.Discard_tip_success()
        root = discardtipsuccess.SetUpTree()
        result = root.Evaluate()
        if result == module_tree.node.NodeState.SUCCESS:
            return "Accepted"
        else:
            return result

class Queryable:
    def __init__(self, orchestrator: Orchestrator) -> None:
        self.orchestrator = orchestrator
        
    def check_status(self, node: Orchestrator, event: str) -> str:
        return node.__getattribute__(event)()

    def trigger_queryable_handler(self, query: zenoh.Query) -> None:
        try:
            logging.debug("Received query: {}".format(query.selector))
            event = query.selector.decode_parameters()
            result = self.check_status(self.orchestrator, event.event)
            if result == "Accepted":
                payload = {"response_type":"Accepted","response":"Successfully executed."}
            else:
                payload = {"response_type":"Rejected","response":result}
        except ValueError as e:
            payload = {"response_type":"Rejected","response":e}
        query.reply(zenoh.Sample("Orchestrator/trigger", payload))


class Session:
    def __init__(self, handler: Queryable) -> None:
        self.handler = handler
    def open(self):
        self.config = zenoh.Config()
        self.session = zenoh.open(self.config)
        self.trigger_queryable = self.session.declare_queryable("Orchestrator/trigger", self.handler.trigger_queryable_handler)
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
    orchestrator = Orchestrator_()
    handler = Queryable(orchestrator)
    with session_manager(handler) as session:
        logging.debug("Orchestrator Started...")
        while True:
            time.sleep(1)