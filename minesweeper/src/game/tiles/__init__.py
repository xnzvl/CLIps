from typing import Literal, Union


Sign = Literal[
    'COVERED',
    'FLAG',
    'QUESTION_MARK',
    'EXPLODED_MINE',
    'MINE',
    'BAD_MINE',
    'EMPTY'
]

Symbol = Union[Sign, Literal['NUMBER']]


COVERED_SYMBOLS = {'COVERED', 'FLAG', 'QUESTION_MARK'}
