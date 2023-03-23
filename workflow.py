from typing import Iterator, Dict
from contextlib import contextmanager
import json
import logging
import time
import zenoh # type: ignore

logging.getLogger().setLevel(logging.DEBUG)

workflow = ["GetTip"]

class Queryable:

    def get_status(self, key_expression: str) -> Dict[str, str]:
        """
        Get status of the node from hardware modules through zenoh.
        """
        session = zenoh.open(zenoh.Config())
        replies = session.get(key_expression, zenoh.Queue(), zenoh.QueryTarget.ALL())
        for reply in replies:
            try:
                value = json.loads(reply.ok.payload.decode("utf-8"))
            except:
                value = json.loads(reply.err.payload.decode("utf-8"))
            return value
        return {}

    def check_status(self, event) -> Dict[str, str]:
        keyexpression = "{}/trigger?timestamp={}".format(event, time.time())
        result = self.get_status(keyexpression)
        return result
    
    def trigger_queryable_handler(self, query: zenoh.Query) -> None:
        global workflow
        try:
            logging.debug("Received query: {}".format(query.selector))
            for event in workflow:
                result = self.check_status(event)
                if result != {}:
                    if result["response_type"] == "Accepted":
                        payload = {"response_type":"Accepted","response":result["response"]}
                    else:
                        payload = {"response_type":"Rejected","response":result["response"]}
                        break
                else:
                    payload = {"response_type":"Rejected","response":"{} Module is not responding. Please check Connection.".format(event)}
                    break
        except ValueError as e:
            payload = {"response_type":"Rejected", "response": "{}".format(e)}
        query.reply(zenoh.Sample("Workflow/trigger", payload))

class Session:
    def __init__(self, handler: Queryable) -> None:
        self.handler = handler
    
    def open(self):
        global keyexpression
        self.config = zenoh.Config()
        self.session = zenoh.open(self.config)
        self.trigger_queryable = self.session.declare_queryable("Workflow/trigger", self.handler.trigger_queryable_handler)
        
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