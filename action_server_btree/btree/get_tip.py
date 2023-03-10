from contextlib import contextmanager
from setTree import SetTree
from typing import Iterator
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
        logging.debug("Received query: {}".format(query.selector))
        event = query.selector.decode_parameters()
        if event == {}:
            payload = {"response_type":"Rejected", "response":"No Arguments given."}
        elif event.get("event") == None or event.get("timestamp") == "":
            payload = {"response_type":"Rejected", "response":"Agruments are not valid."}
        else:
            root = self.tree.SetupTree()
            value = root.Evaluate(event.get("event"), event.get("timestamp"))
            if value == NodeState.SUCCESS:
                payload = {"response_type":"Accepted", "response":"Get Tip Success."}
            else:
                payload = {"response_type":"Rejected", "response":"Get Tip Failure."}
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