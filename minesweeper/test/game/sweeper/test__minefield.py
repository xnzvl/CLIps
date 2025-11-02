from pytest import fixture

from src.common import Action, Dimensions, Move, Point, SweeperConfiguration
from src.game.sweeper import Minefield

from .utils import compare_grid_with_shape


SEED = 'testing'
SMALL_DEFAULT_SHAPE = [
    'OOOOOOOOO',
    'OOOOOOOOO',
    'OOO222OOO',
    'OOO1 112O',
    'OOO1   11',
    'OOO1     ',
    'OOO1     ',
    'OOO1 111 ',
    'OOO1 1O1 '
]


@fixture
def opened_minefield() -> Minefield:
    minefield = Minefield(
        SweeperConfiguration(
            dimensions=Dimensions(9, 9),
            mines=10,
            question_marks=False
        ),
        SEED
    )
    minefield.play(
        Move(
            action=Action.UNCOVER,
            point=Point(4, 4),
        )
    )
    return minefield


class TestPlay:
    def test_seeding(self, opened_minefield: Minefield) -> None:
        assert compare_grid_with_shape(
            opened_minefield.obtain_grid(),
            SMALL_DEFAULT_SHAPE
        )

    def test_uncover_on_empty(self, opened_minefield: Minefield) -> None:
        opened_minefield.play(
            Move(
                action=Action.UNCOVER,
                point=Point(4, 4),
            )
        )

        assert compare_grid_with_shape(
            opened_minefield.obtain_grid(),
            SMALL_DEFAULT_SHAPE
        )

    def test_uncover_on_number(self, opened_minefield: Minefield) -> None:
        opened_minefield.play(
            Move(
                action=Action.UNCOVER,
                point=Point(3, 2),
            )
        )

        assert compare_grid_with_shape(
            opened_minefield.obtain_grid(),
            SMALL_DEFAULT_SHAPE
        )

    def test_uncover_on_covered(self, opened_minefield: Minefield) -> None:
        opened_minefield.play(
            Move(
                action=Action.UNCOVER,
                point=Point(7, 2),
            )
        )

        assert compare_grid_with_shape(
            opened_minefield.obtain_grid(),
            [
                'OOOOOOOOO',
                'OOOOOOOOO',
                'OOO222O2O',
                'OOO1 112O',
                'OOO1   11',
                'OOO1     ',
                'OOO1     ',
                'OOO1 111 ',
                'OOO1 1O1 '
            ]
        )

    def test_flag_on_empty(self, opened_minefield: Minefield) -> None:
        opened_minefield.play(
            Move(
                action=Action.FLAG,
                point=Point(4, 4),
            )
        )

        assert compare_grid_with_shape(
            opened_minefield.obtain_grid(),
            SMALL_DEFAULT_SHAPE
        )

    def test_flag_on_number(self, opened_minefield: Minefield) -> None:
        opened_minefield.play(
            Move(
                action=Action.FLAG,
                point=Point(3, 2),
            )
        )

        assert compare_grid_with_shape(
            opened_minefield.obtain_grid(),
            SMALL_DEFAULT_SHAPE
        )

    def test_flag_on_covered(self, opened_minefield: Minefield) -> None:
        opened_minefield.play(
            Move(
                action=Action.FLAG,
                point=Point(6, 8),
            )
        )

        assert compare_grid_with_shape(
            opened_minefield.obtain_grid(),
            [
                'OOOOOOOOO',
                'OOOOOOOOO',
                'OOO222OOO',
                'OOO1 112O',
                'OOO1   11',
                'OOO1     ',
                'OOO1     ',
                'OOO1 111 ',
                'OOO1 1F1 '
            ]
        )
