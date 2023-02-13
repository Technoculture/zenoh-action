from typing import Protocol, Iterator
import logging
import zenoh
from contextlib import contextmanager
import time

class Orchestrator(Protocol):
    def pick_up(self) -> str:
        ...
    def caught_tip_firm_and_orient(self) -> str:
        ...
    def go_to_discard_position(self) -> str:
        ...
    def goto_discard_position(self) -> str:
        ...

class Orchestrator_:
    def pick_up(self) -> str:
        return "Pick Up"
    def caught_tip_firm_and_orient(self) -> str:
        return "Caught Tip Firm and Orient"
    def go_to_discard_position(self) -> str:
        return "Go to Discard Position"
    def goto_discard_position(self) -> str:
        return "Go to Discard Position"

class Queryable:
    def __init__(self, orchestrator: Orchestrator) -> None:
        self.orchestrator = orchestrator
        
    def check_status(self, node: Orchestrator, event: str) -> bool:
        return node.__getattribute__(event)()

    def trigger_queryable_handler(self, query: zenoh.Query) -> None:
        logging.debug("Received query: {}".format(query.selector))
        event = query.selector.decode_parameters()
        result = self.check_status(self.orchestrator, event)
        payload = {"response_type":"accepted", "response":result}
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
        logging.debug("Tip Checker Started...")
        while True:
            time.sleep(1)