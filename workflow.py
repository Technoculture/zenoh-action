from typing import Iterator, Dict
from contextlib import contextmanager
import json
import logging
import time
import zenoh # type: ignore

logging.getLogger().setLevel(logging.DEBUG)

keyexpression:str = "workflow/trigger"

class Queryable:

    def get_status(self, key_expression: str) -> Dict[str, str]:
        """
        Get status of the node from hardware modules through zenoh.
        """
        session = zenoh.open(zenoh.Config())
        replies = session.get(key_expression, zenoh.Queue(), zenoh.QueryTarget.ALL())
        for reply in replies:
            return json.loads(reply.ok.payload.decode("utf-8"))
        return {}

    def check_status(self, event) -> Dict[str, str]:
        keyexpression = "{}/trigger?timestamp={}&event={}".format(event.workflow, event.timestamp, event.event)
        result = self.get_status(keyexpression)
        return result
    
    def trigger_queryable_handler(self, query: zenoh.Query) -> None:
        try:
            logging.debug("Received query: {}".format(query.selector))
            event = Workflow(**query.selector.decode_parameters())
            logging.debug("Events: {}".format(event))
            result = self.check_status(event)
            if result != {}:
                if result["response_type"] == "Accepted":
                    payload = {"response_type":"Accepted","response":result["response"]}
                else:
                    payload = {"response_type":"Rejected","response":result["response"]}
            else:
                payload = {"response_type":"Rejected","response":"Workflow not found."}
        except Exception as e:
            payload = {"response_type":"Rejected","response":"Timestamp, event or workflow is not Valid or the arguments are missing."}
        query.reply(zenoh.Sample(keyexpression, payload))

class Session:
    def __init__(self, handler: Queryable) -> None:
        self.handler = handler
    def open(self):
        global keyexpression
        self.config = zenoh.Config()
        self.session = zenoh.open(self.config)
        self.trigger_queryable = self.session.declare_queryable(keyexpression, self.handler.trigger_queryable_handler)
        
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
    handler = Queryable()
    with session_manager(handler) as session:
        logging.debug("Workflow Started...")
        while True:
            time.sleep(1)