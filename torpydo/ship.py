from enum import Enum
from typing import List

class Color(Enum):
    CADET_BLUE = 1
    CHARTREUSE = 2
    ORANGE = 3
    RED = 4
    YELLOW = 5

class Letter(Enum):
    A = 1
    B = 2
    C = 3
    D = 4
    E = 5
    F = 6
    G = 7
    H = 8

class Position(object):
    def __init__(self, column: Letter, row: int):
        self.column = column
        self.row = row

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __str__(self):
        return f"{self.column.name}{self.row}"

    @classmethod
    def from_str(cls, value: str):
        letter = Letter[value.upper()[:1]]
        number = int(value[1:])

        if number < 1 or number > 8:
            raise ValueError(f"row {number} is not in range [1, 8].")

        return cls(letter, number)

    __repr__ = __str__

class Ship(object):
    def __init__(self, name: str, size: int, color: Color):
        self.name = name
        self.size = size
        self.color = color
        self.positions: List[Position] = []

    def add_position(self, input: str):
        self.positions.append(Position.from_str(input))

    def __str__(self):
        return f"{self.color.name} {self.name} ({self.size}): {self.positions}"

    __repr__ = __str__
