import pandas as pd

from .utils import intersect

from ..utils import pad_symbols, transpose, DecoratedString
from ..widget import BaseWidget
from ..axis import get_x_axis, get_y_axis
from ..status import get_status_bar






class CandlestickChart(BaseWidget):

    def __init__(self, 
                 height: int=40, 
                 body_char: str='┃', 
                 wick_char: str='│', 
                 current_char: str='⋯',
                 color_up: str | None='green', 
                 color_down: str | None='red', 
                 color_current: str | None='blue',
                 include_current: bool=False,
                 include_status_bar: bool=False,
                 ):

        body, wick, fill = pad_symbols([body_char, wick_char, ''])

        self.height = height

        self.body = body
        self.wick = wick
        self.fill = fill

        self.color_up = color_up
        self.color_down = color_down
        
        self.current_char = DecoratedString(current_char, color=color_current) if include_current else ''
        self.include_status_bar = include_status_bar


    def __call__(self, src: pd.DataFrame, prev_close: float) -> list[list[str]]:

        bucket_size = (src.High.max() - (floor := src.Low.min())) / self.height
        current_close = src.iloc[-1].Close
        matrix = []
        
        for index in src.index:

            column = []

            is_positive = src.loc[index].Close > src.loc[index].Open
            color = self.color_up if is_positive else self.color_down

            for n_bucket in range(self.height):

                bucket = ((s := n_bucket * bucket_size + floor), s + bucket_size)

                body_upper = max(src.loc[index].Open, src.loc[index].Close)
                body_lower = min(src.loc[index].Open, src.loc[index].Close)

                upper_wick  = (intersect((body_upper, src.loc[index].High), bucket), DecoratedString(self.wick, color=color))
                candle_body = (intersect((body_lower, body_upper), bucket), DecoratedString(self.body, color=color))
                lower_wick  = (intersect((src.loc[index].Low, body_lower), bucket), DecoratedString(self.wick, color=color))
                
                k, symbol = max([upper_wick, candle_body, lower_wick], key=lambda x: x[0])

                column.append(symbol if k > 0 else (self.current_char if bucket[0] <= current_close <= bucket[1] else self.fill))

            matrix.append(column)

        y_axis = get_y_axis(src, height=self.height)
        y_axis_padding = len(y_axis[0]) - 2

        x_axis = get_x_axis(src, width=len(self.body), lpad=y_axis_padding, align_timestamps='center', n_ticks=10)
        

        matrix.insert(0, y_axis)

        transposed_matrix = transpose(matrix)
        transposed_matrix.reverse()

        transposed_matrix.append(x_axis[0])
        transposed_matrix.append(x_axis[1])

        if self.include_status_bar:
            status_bar = get_status_bar(src, prev_close, lpad=y_axis_padding)
            transposed_matrix.insert(0, status_bar)


        return transposed_matrix










