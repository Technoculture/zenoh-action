from contextlib import contextmanager
from pydantic import ValidationError    #type: ignore
from typing import Iterator
from triggervalidator import Event
from setTree import SetTree
from node import NodeState
import logging
import time
import zenoh #type: ignore

logging.getLogger().setLevel(logging.DEBUG)

class Queryable:
    """Queryable class to handle the queries."""

    def __init__(self, tree) -> None:
        """Initialise variables."""
        self.tree = tree

    def trigger_queryable_handler(self, query: zenoh.Query) -> None:
        """ Handle the query for the trigger queryable."""
        try:
            logging.debug("Received query: {}".format(query.selector))
            event = Event(**query.selector.decode_parameters())
            root = self.tree.SetupTree()
            value = root.Evaluate(event.event, event.timestamp)
            if value == NodeState.SUCCESS:
                payload = {"response_type":"Accepted", "response":"Event Accepted and triggered."}
            else:
                payload = {"response_type":"Rejected", "response":"Event Not Accepted and Failed."}
        
        except (ValidationError, ValueError) as e:
            payload = {"response_type":"Rejected","response":"Timestamp or event is not Valid or the arguments are missing."}

        query.reply(zenoh.Sample("GetTip/trigger", payload))

class Session:
    """Session class to handle the session."""

    def __init__(self, handler: Queryable) -> None:
        """Initialise variables."""
        self.handler = handler

    def open(self) -> None:
        """Open the session."""
        self.config = zenoh.Config()
        self.session = zenoh.open(self.config)
        self.trigger_queryable = self.session.declare_queryable("GetTip/trigger", self.handler.trigger_queryable_handler)

    def close(self) -> None:
        """Close the session."""
        self.session.close()
        self.trigger_queryable.undeclare()    

@contextmanager
def session_manager(handler: Queryable) -> Iterator[Session]:
    """Context manager for the session.
        Returns: Iterator[Session]
    """
    try:
        session = Session(handler)
        session.open()
        yield session
    except KeyboardInterrupt:
        logging.error("Interrupted by user")
    finally:
        session.close()

if __name__ == "__main__":
    tree = SetTree()
    handler = Queryable(tree)
    with session_manager(handler) as session:
        logging.debug("Get Tip Started...")
        while True:
            time.sleep(1)