import py_trees
class MaintenanceError(Exception):
    def __init__(self, error_type: str="Tray", msg: str = "It required maintenance.") -> None:
        self.error = error_type
        self.msg = msg
        super().__init__(f"{self.error} {self.msg}")

class RestockError(Exception):
    def __init__(self, error_type: str="Stock", msg: str = "It required restock.") -> None:
        self.error = error_type
        self.msg = msg
        super().__init__(f"{self.error} {self.msg}")

class RetryException(Exception):
    def __init__(self) -> None:
        retry_count = py_trees.blackboard.Blackboard().get("RETRY")
        py_trees.blackboard.Blackboard().set("RETRY", retry_count+1)
        super().__init__(f"You have retried {retry_count} times.")
