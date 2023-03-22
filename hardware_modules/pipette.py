from typing import Protocol, Iterator
from contextlib import contextmanager
from pydantic import ValidationError    #type: ignore
from triggervalidator import Event
import logging
import time
import zenoh # type: ignore

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
        return "Accepted"

    def load_success(self) -> str:
        return "Accepted"

    def eject_tip(self) -> str:
        return "Accepted"

    def discard_tip_success(self) -> str:
        return "Accepted"

class Queryable:
    def __init__(self, pipette: Pipette) -> None:
        self.pipette = pipette
        
    def check_status(self, node: Pipette, event: str) -> str:
        return node.__getattribute__(event)()

    def trigger_queryable_handler(self, query: zenoh.Query) -> None:
        try:
            logging.debug("Received query: {}".format(query.selector))
            event = query.selector.decode_parameters()
            event = Event(**query.selector.decode_parameters())
            result = self.check_status(self.pipette, event.event)
            payload = {"response_type":"Accepted","response":result}
        except (ValueError, ValidationError) as e:
            payload = {"response_type":"Rejected","response":"Timestamp or event is not Valid or the arguments are missing."}
        query.reply(zenoh.Sample("TipRM/trigger", payload))

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
        logging.debug("Pipette Started...")
        while True:
            time.sleep(1)