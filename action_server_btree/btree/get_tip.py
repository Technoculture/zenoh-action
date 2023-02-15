from typing import Protocol, Iterator
import zenoh
import logging
from contextlib import contextmanager
import time

logging.getLogger().setLevel(logging.DEBUG)

class GetTip(Protocol):
    def prepare_tip_for_pickup(self) -> str:
        ...
    def pick_up_using_orchestraror(self) -> str:
        ...
    def load_new_tray(self) -> str:
        ...
    def discard_tip(self) -> str:
        ...
    def retry_count_below_threshold(self) -> str:
        ...

class Get_Tip:
    def prepare_tip_for_pickup(self) -> str:
        return "Prepare Tip for Pickup"

    def pick_up_using_orchestraror(self) -> str:
        return "Pick Up Using Orchestrator"

    def load_new_tray(self) -> str:
        return "Load New Tray"

    def discard_tip(self) -> str:
        return "Discard Tip"

    def retry_count_below_threshold(self) -> str:
        return "Retry Count Below Threshold"

class Queryable:
    def __init__(self, GetTip: GetTip) -> None:
        self.GetTip = GetTip

    def check_status(self, node: GetTip, event: str) -> str:
        return node.__getattribute__(event)()

    def trigger_queryable_handler(self, query: zenoh.Query) -> None:
        logging.debug("Received query: {}".format(query.selector))
        event = query.selector.decode_parameters()
        if event == {}:
            payload = {"response_type":"Rejected", "response":"No Arguments given."}
        elif event.get("event") == None or event.get("timestamp") == "":
            payload = {"response_type":"Rejected", "response":"Agruments are not valid."}
        else:
            result = self.check_status(self.GetTip, event['event'])
            payload = {"response_type":"accepted","response":result}
        query.reply(zenoh.Sample("GetTip/trigger", payload))

class Session:
    def __init__(self, handler: Queryable) -> None:
        self.handler = handler
    def open(self):
        self.config = zenoh.Config()
        self.session = zenoh.open(self.config)
        self.trigger_queryable = self.session.declare_queryable("GetTip/trigger", self.handler.trigger_queryable_handler)
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
    get_tip = Get_Tip()
    handler = Queryable(get_tip)
    with session_manager(handler) as session:
        logging.debug("Get Tip Started...")
        while True:
            time.sleep(1)