class Node(object):

    _key: int
    _dist: float
    _visited: bool

    def __init__(self, key: int):
        self._key = key
        self._dist = -1
        self._visited = False

    def get_key(self) -> int:
        return self._key

    def get_dist(self) -> float:
        return self._dist

    def set_dist(self, dist: float) -> None:
        self._dist = dist

    def get_visited(self) -> float:
        return self._visited

    def set_visited(self, visited: bool) -> None:
        self._visited = visited
