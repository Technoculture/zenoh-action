from typing import Protocol, Iterator
import logging
import zenoh
from contextlib import contextmanager
import time

logging.getLogger().setLevel(logging.DEBUG)

class Pipette(Protocol):
    def discard_success(self) -> str:
        ...
    def load_success(self) -> str:
        ...
    def eject_tip(self) -> str:
        ...
    def discard_tip_success(self) -> str:
        ...

class Pipette_:
    def discard_success(self) -> str:
        return "Discard Success"

    def load_success(self) -> str:
        return "Load Success"

    def eject_tip(self) -> str:
        return "Eject Tip"

    def discard_tip_success(self) -> str:
        return "Discard Tip Success"

class Queryable:
    def __init__(self, pipette: Pipette) -> None:
        self.pipette = pipette
        
    def check_status(self, node: Pipette, event: str) -> bool:
        return node.__getattribute__(event)()

    def trigger_queryable_handler(self, query: zenoh.Query) -> None:
        logging.debug("Received query: {}".format(query.selector))
        event = query.selector.decode_parameters()
        result = self.check_status(self.pipette, event)
        payload = {"response_type":"accepted", "response":result}
        query.reply(zenoh.Sample("Pipette/trigger", payload))

class Session:
    def __init__(self, handler: Queryable) -> None:
        self.handler = handler
    def open(self):
        self.config = zenoh.Config()
        self.session = zenoh.open(self.config)
        self.trigger_queryable = self.session.declare_queryable("Pipette/trigger", self.handler.trigger_queryable_handler)
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
    pipette = Pipette_()
    handler = Queryable(pipette)
    with session_manager(handler) as session:
        logging.debug("Tip Checker Started...")
        while True:
            time.sleep(1)