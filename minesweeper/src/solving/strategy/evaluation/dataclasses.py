from dataclasses import dataclass
from typing import Dict

from src.game.sweeper import Result

from .difficulty import Difficulty


@dataclass(frozen=True)
class Evaluation:
    strategy_name: str
    winrate_per_difficulty: Dict[Difficulty, float]


@dataclass(frozen=True)
class FormLocation:   # TODO: better name
    strategy_index: int
    difficulty_index: int


@dataclass(frozen=True)
class FormUpdate(FormLocation):   # TODO: better name
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
