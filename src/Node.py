class Node(object):
    _key: int
    _dist: float
    _visited: bool
    _component: int
    _pos: tuple

    def __init__(self, key: int, pos: tuple = None):
        self._pos = pos
        self._key = key
        self._dist = float('inf')
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

    def get_component(self) -> int:
        return self._component

    def set_component(self, component: int) -> None:
        self._component = component

    def get_pos(self) -> tuple:
        return self._pos

    def set_pos(self, pos: tuple) -> None:
        self._pos = pos

    def get_x(self) -> float:
        return self._pos[0]

    def get_y(self) -> float:
        return self._pos[1]

    def get_pos_str(self) -> str:
        return f'{self._pos[0]},{self._pos[1]},{self._pos[2]}'

    def __repr__(self):
        return f'id: {self._key}, pos: {self._pos}'

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self.get_key() == other.get_key() and self.get_pos() == other.get_pos()
