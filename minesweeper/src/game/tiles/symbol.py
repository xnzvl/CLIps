from enum import Enum


class Symbol(Enum):
    NUMBER        = 'NUMBER'
    MINE          = 'MINE'
    EMPTY         = 'EMPTY'
    COVER         = 'COVER'
    FLAG          = 'FLAG'
    QUESTION_MARK = 'QUESTION_MARK'
    EXPLODED_MINE = 'EXPLODED_MINE'
    WRONG_FLAG    = 'WRONG_FLAG'
