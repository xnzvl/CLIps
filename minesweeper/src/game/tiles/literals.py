from typing import Literal


NumberSymbol = Literal['NUMBER']
MineSymbol   = Literal['MINE']
EmptySymbol  = Literal['EMPTY']

DataSymbols = Literal[MineSymbol, NumberSymbol, EmptySymbol]

InGameNonNumberSymbol = Literal['COVERED', 'FLAG', 'QUESTION_MARK', EmptySymbol]
InGameSymbol          = Literal[InGameNonNumberSymbol, NumberSymbol]

PostGameSymbol = Literal[MineSymbol, 'EXPLODED_MINE', 'WRONG_FLAG']

NonNumberSymbol = Literal[InGameNonNumberSymbol, PostGameSymbol]
Symbol          = Literal[InGameSymbol, PostGameSymbol]
