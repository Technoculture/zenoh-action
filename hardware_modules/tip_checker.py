from typing import Protocol, Iterator
from contextlib import AbstractContextManager
import module_tree
import logging
import time
import zenoh # type: ignore

logging.getLogger().setLevel(logging.DEBUG)

class TipChecker(Protocol):
    def caught_tip_firm_and_orient(self) -> str:
        ... 
    def discard_tip_success(self) -> str:
        ...

class Tip_checker:
    def caught_tip_firm_and_orient(self) -> str:
        caughttipfirmandorient = module_tree.Caught_tip_firm_and_orient()
        root = caughttipfirmandorient.SetUpTree()
        result = root.Evaluate()
        if result == module_tree.node.NodeState.SUCCESS:
            return "Accepted"
        else:
            return result
        
    def discard_tip_success(self) -> str:
        discardtipsuccess = module_tree.Discard_tip_success()
        root = discardtipsuccess.SetUpTree()
        result = root.Evaluate()
        if result == module_tree.node.NodeState.SUCCESS:
            return "Accepted"
        else:
            return result

class Queryable:
    def __init__(self, tip_checker: TipChecker) -> None:
        self.tip_checker = tip_checker
        
    def check_status(self, node: TipChecker, event: str) -> str:
        return node.__getattribute__(event)()

    def trigger_queryable_handler(self, query: zenoh.Query) -> None:
        try:
            logging.debug("Received query: {}".format(query.selector))
            event = query.selector.decode_parameters()
            result = self.check_status(self.tip_checker, event['event'])
            if result == "Accepted":
                payload = {"response_type":"Accepted","response":"Successfully executed."}
            else:
                payload = {"response_type":"Rejected","response":result}
        except ValueError as e:
            payload = {"response_type":"Rejected","response":"Timestamp or event is not Valid or the arguments are missing."}
        query.reply(zenoh.Sample("TipChecker/trigger", payload))


class Session:
    def __init__(self, handler: Queryable) -> None:
        self.handler = handler
    def open(self):
        self.config = zenoh.Config()
        self.session = zenoh.open(self.config)
        self.trigger_queryable = self.session.declare_queryable("TipChecker/trigger", self.handler.trigger_queryable_handler)
        
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
    tip_checker = Tip_checker()
    handler = Queryable(tip_checker)
    with session_manager(handler) as session:
        logging.debug("Tip Checker Started...")
        while True:
            time.sleep(1)