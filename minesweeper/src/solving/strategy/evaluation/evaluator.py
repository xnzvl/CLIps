from functools import partial
from multiprocessing import Process, Pipe
from multiprocessing.connection import Connection
from multiprocessing.managers import SharedMemoryManager
from multiprocessing.pool import Pool
from multiprocessing.shared_memory import ShareableList
from random import randint, choice
from time import sleep
from typing import Dict, List, Tuple

from src.common import Dimensions, SweeperConfiguration
from src.game.sweeper import Result, GameState
from src.solving.bot import BotFactory
from src.solving.strategy import Strategy
from src.solving.strategy.evaluation.throbber import Throbber
from src.utils import Repeater

from .console_output import ConsoleOutput
from .types import (
    Difficulty,
    Evaluation,
    RecordPosition, RecordUpdate,
    Summary, SummaryEntry
)


# TODO: refactor the whole module
# TODO: fix bug - overall winrate is wrong


class Evaluator:
    @staticmethod
    def _submit_progress_update(
            progress_updates_sender: Connection,
            strategy_index: int,
            difficulty_index: int,
            result: Result
    ) -> None:
        progress_updates_sender.send(
            RecordUpdate(
                strategy_index=strategy_index,
                difficulty_index=difficulty_index,
                result=result
            )
        )

    def __init__(
            self,
            strategies: List[Tuple[str, Strategy]],
            dimensions: Dimensions = Dimensions(24, 24),
            testing_batch_size: int = 10
    ) -> None:
        self._strategies = strategies

        self._dimensions = dimensions
        self._testing_batch_size = testing_batch_size

        self._console = ConsoleOutput(strategies, testing_batch_size)

    def _create_active_throbber(self, record_position: RecordPosition) -> Repeater:
        repeater = Repeater(
            0.05,
            lambda throbber: self._console.write_throbber_char(
                record_position,
                throbber.get_and_progress()
            ),
            Throbber(2)
        )

        repeater.start()
        return repeater

    def _throbber_updater(
            self,
            throbber_updates_receiver: Connection,
            throbber_ack_sender: Connection
    ) -> None:
        diff_len = len(Difficulty)

        throbbers = [
            self._create_active_throbber(
                RecordPosition(
                    strategy_index=i // diff_len,
                    difficulty_index=i % diff_len,
                )
            )
            for i in range(len(self._strategies) * diff_len)
        ]

        update = throbber_updates_receiver.recv()
        while update is not None:
            throbbers[update.strategy_index * diff_len + update.difficulty_index].stop()
            sleep(0.075)
            throbber_ack_sender.send(None)

            update = throbber_updates_receiver.recv()

    def _progress_updater(  # TODO: refactor
            self,
            progress_updates_receiver: Connection,
            throbber_updates_sender: Connection,
            throbber_ack_receiver: Connection,
            victories: ShareableList[int]
    ) -> None:
        diff_len = len(Difficulty)

        tests_completed = [ 0 for _ in range(len(self._strategies) * diff_len) ]

        update = progress_updates_receiver.recv()
        while update is not None:
            self._console.move_to_record_difficulty(update)

            i = update.strategy_index * diff_len + update.difficulty_index

            if update.result == GameState.VICTORY:
                victories[i] += 1

            tests_completed[i] += 1
            tests_done = tests_completed[i]

            if tests_done != self._testing_batch_size:
                self._console.write_progress(tests_done)
            else:
                throbber_updates_sender.send(update)
                throbber_ack_receiver.recv()

                self._console.write_winrate(victories[i] / self._testing_batch_size * 100)

            self._console.move_from_record_difficulty(update)
            self._console.flush()

            update = progress_updates_receiver.recv()

    def _to_evaluations(self, victories: ShareableList[int]) -> List[Evaluation]:
        evaluations: List[Evaluation] = list()
        diff_len = len(Difficulty)

        for strategy_index, (strategy_name, _) in enumerate(self._strategies):
            per_difficulty: Dict[Difficulty, float] = dict()

            for difficulty_index, difficulty in enumerate(Difficulty):
                per_difficulty[difficulty] = victories[strategy_index * diff_len + difficulty_index] \
                    / self._testing_batch_size * 100

            evaluations.append(
                Evaluation(
                    strategy_name=strategy_name,
                    winrate_per_difficulty=per_difficulty
                )
            )

        return evaluations

    def _evaluate_strategy(
            self,
            pool: Pool,
            progress_updates_sender: Connection,
            strategy_index: int
    ) -> None:
        strategy_name, strategy = self._strategies[strategy_index]

        for difficulty in Difficulty:
            diff_index, diff_coefficient = difficulty.value

            bot = BotFactory.get_minefield_bot(
                SweeperConfiguration(
                    dimensions=self._dimensions,
                    mines=int((self._dimensions.width * self._dimensions.height) / diff_coefficient),
                    question_marks=False
                ),
                strategy,
                f'evaluator::{strategy_name}',
            )

            for _ in range(self._testing_batch_size):
                pool.apply_async(
                    func=demanding_calculation,  # bot.solve,  # TODO: uncomment
                    callback=partial(
                        Evaluator._submit_progress_update,
                        progress_updates_sender,
                        strategy_index,
                        diff_index
                    )
                )

    def _evaluate_strategies(self, max_workers: int) -> List[Evaluation]:  # TODO: refactor
        smm = SharedMemoryManager()
        smm.start()

        victories = smm.ShareableList(
            [0 for _ in range(len(self._strategies) * len(Difficulty))]
        )

        progress_updates_receiver, progress_updates_sender = Pipe(False)
        throbber_updates_receiver, throbber_updates_sender = Pipe(False)
        throbber_ack_receiver,     throbber_ack_sender     = Pipe(False)

        progress_updater_process = Process(
            target=self._progress_updater,
            args=(progress_updates_receiver, throbber_updates_sender, throbber_ack_receiver, victories)
        )
        progress_updater_process.start()

        throbber_updater_process = Process(
            target=self._throbber_updater,
            args=(throbber_updates_receiver, throbber_ack_sender)
        )
        throbber_updater_process.start()

        pool = Pool(
            processes=max_workers
        )
        for strategy_index in range(len(self._strategies)):
            self._evaluate_strategy(pool, progress_updates_sender, strategy_index)
        pool.close()
        pool.join()

        progress_updates_sender.send(None)
        progress_updater_process.join()

        throbber_updates_sender.send(None)
        throbber_updater_process.join()

        progress_updates_receiver.close()
        progress_updates_sender.close()
        throbber_updates_receiver.close()
        throbber_updates_sender.close()
        throbber_ack_receiver.close()
        throbber_ack_sender.close()

        evaluations = self._to_evaluations(victories)

        smm.shutdown()
        smm.join()

        return evaluations

    def _summarise(self, evaluations: List[Evaluation]) -> Summary:  # TODO: refactor
        best_per_difficulty: Dict[Difficulty, SummaryEntry] = dict()
        best_overall: SummaryEntry | None = None

        for evaluation in evaluations:
            winrate_sum = 0.0

            for difficulty, winrate in evaluation.winrate_per_difficulty.items():
                best_so_far = best_per_difficulty.get(difficulty)

                if best_so_far is None or best_so_far.winrate < winrate:
                    best_per_difficulty[difficulty] = SummaryEntry(
                        strategy_name=evaluation.strategy_name,
                        winrate=winrate,
                        is_alone_at_top=True
                    )
                elif best_so_far.winrate == winrate:
                    best_per_difficulty[difficulty] = SummaryEntry(
                        strategy_name=best_so_far.strategy_name,
                        winrate=best_so_far.winrate,
                        is_alone_at_top=False
                    )

                winrate_sum += winrate

            winrate_overall = winrate_sum / 3

            if best_overall is None or best_overall.winrate < winrate_overall:
                best_overall = SummaryEntry(
                    strategy_name=evaluation.strategy_name,
                    winrate=winrate_overall,
                    is_alone_at_top=True
                )
            elif best_overall.winrate == winrate_overall:
                best_overall = SummaryEntry(
                    strategy_name=best_overall.strategy_name,
                    winrate=best_overall.winrate,
                    is_alone_at_top=False
                )

        assert best_overall is not None
        return Summary(
            best_per_difficulty=best_per_difficulty,
            best_overall=best_overall
        )

    def run(self, max_workers: int = 16) -> None:
        with self._console.hidden_cursor():
            self._console.prepare_evaluation_records()

            summary = self._summarise(
                self._evaluate_strategies(max_workers)
            )

            self._console.move_to_records_end()
            self._console.write_summary(summary)


def demanding_calculation() -> Result:
    sleep(randint(1, 10) / 10)
    return choice([GameState.VICTORY, GameState.FAILURE])
