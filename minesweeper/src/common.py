from dataclasses import dataclass
from typing import Literal


Action = Literal['UNCOVER', 'FLAG', 'QUESTION_MARK', 'CLEAR']  # TODO: enumerate


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
    action: Action
    point: Point  # TODO: rename to 'point'
