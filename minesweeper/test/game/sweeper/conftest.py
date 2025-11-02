from pytest import fixture

from src.common import Action, Dimensions, Move, Point, SweeperConfiguration
from src.game.sweeper import Minefield

from .constant import SEED


@fixture
def default_minefield() -> Minefield:  # TODO: would be worth to create a Minefield from data symbols?
    return Minefield(
        SweeperConfiguration(
            dimensions=Dimensions(9, 9),
            mines=10,
            question_marks=False
        ),
        SEED
    )


@fixture
def opened_minefield(default_minefield: Minefield) -> Minefield:
    default_minefield.play(
        Move(
            action=Action.UNCOVER,
            point=Point(4, 4),
        )
    )
    return default_minefield


@fixture
def failure_minefield(opened_minefield: Minefield) -> Minefield:
    opened_minefield.play(
        Move(
            action=Action.UNCOVER,
            point=Point(6, 8),
        )
    )
    return opened_minefield


@fixture
def victory_minefield(opened_minefield: Minefield) -> Minefield:
    points_to_uncover = [
        Point(0, 0), Point(1, 0), Point(2, 0), Point(3, 0), Point(4, 0),
        Point(8, 0), Point(0, 1), Point(2, 1), Point(0, 2), Point(1, 2),
        Point(2, 2), Point(0, 3), Point(1, 3), Point(2, 3), Point(1, 4),
        Point(0, 5), Point(1, 5), Point(2, 5), Point(1, 6), Point(2, 6),
        Point(0, 8), Point(2, 8)
    ]

    for point_to_uncover in points_to_uncover:
        opened_minefield.play(
            Move(
                action=Action.UNCOVER,
                point=point_to_uncover
            )
        )

    return opened_minefield
