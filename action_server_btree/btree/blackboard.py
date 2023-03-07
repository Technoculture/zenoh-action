class Blackboard:
    def __init__(self):
        self._data = {}
        self.current_node = None
        self.non_leaf_nodes = []
        self.success_nodes = []
        self.decision_nodes = []
        self.retry_count = 0

    def set(self, key, value):
        self._data[key] = value

    def get(self, key):
        return self._data[key]

    def has_key(self, key):
        return key in self._data