from dataclasses import dataclass
from enum import Enum, unique
from typing import Dict

from src.game.sweeper import Result


@unique
class Difficulty(Enum):
    # difficulty | mine coefficient
    EASY         = (0, 8.1)
    INTERMEDIATE = (1, 6.4)
    HARD         = (2, 4.8)


@dataclass(frozen=True)
class Evaluation:
    strategy_name: str
    winrate_per_difficulty: Dict[Difficulty, float]


@dataclass(frozen=True)
class RecordPosition:   # TODO: better name
    strategy_index: int
    difficulty_index: int


@dataclass(frozen=True)
class RecordUpdate(RecordPosition):   # TODO: better name
    result: Result


@dataclass(frozen=True)
class SummaryEntry:
    strategy_name: str
    winrate: float
    is_alone_at_top: bool


@dataclass(frozen=True)
class Summary:
    best_per_difficulty: Dict[Difficulty, SummaryEntry]
    best_overall: SummaryEntry
