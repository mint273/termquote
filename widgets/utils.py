from typing import Iterable
import termcolor












def transpose(matrix: Iterable[Iterable]) -> list[list]:

    return [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]






def pad_symbols(s: Iterable[str]) -> list[str]:

    max_width = len(max(s, key=len))
    padded_symbols = []

    for symbol in s:

        width_diff = max_width - len(symbol)

        lpad = width_diff // 2
        rpad = width_diff - lpad
        
        padded_symbols.append(' ' * lpad + symbol + ' ' * rpad)


    return padded_symbols






class DecoratedString(str):

    def __new__(cls, s: str, color: str | None=None, attrs: Iterable[str] | None=None):

        obj = super().__new__(cls, s)
        obj.s_decorated = termcolor.colored(s, color, attrs)

        return obj
    

    def __str__(self) -> str:

        return self.s_decorated





