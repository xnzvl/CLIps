from dataclasses import dataclass
from enum import Enum
from typing import Literal


# TODO: include in __init__.py


class Action(Enum):
    UNCOVER       = 'UNCOVER'
    FLAG          = 'FLAG'
    QUESTION_MARK = 'QUESTION_MARK'
    CLEAR         = 'CLEAR'
    RESET         = 'RESET'
    QUIT          = 'QUIT'


MoveAction = Literal[
    Action.UNCOVER,
    Action.FLAG,
    Action.QUESTION_MARK,
    Action.CLEAR
]

MovelessAction = Literal[
    Action.RESET,
    Action.QUIT
]


@dataclass(frozen=True)
class Point:
    x: int
    y: int


@dataclass(frozen=True)
class Dimensions:
    width: int
    height: int


@dataclass(frozen=True)
class SweeperConfiguration:
    dimensions: Dimensions
    mines: int
    question_marks: bool


@dataclass(frozen=True)
class WebPageSweeperConfiguration(SweeperConfiguration):  # TODO: adapt (mines)
    offsets: Point


@dataclass(frozen=True)
class Move:
    action: MoveAction
    point: Point


class Dimensioned:
    def __init__(self, dimensions: Dimensions) -> None:
        self._dimensions = dimensions

    def get_dimensions(self) -> Dimensions:
        return self._dimensions  # TODO: turn into property
