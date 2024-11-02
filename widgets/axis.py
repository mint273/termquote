import pandas as pd
from typing import Literal







def get_y_axis(src: pd.DataFrame, height: int=40, n_ticks: int=5, axis_char: str='│', tick_char: str='┤', rpad: int=1, lpad: int=1, prefix: str=None, suffix: str=None, include_tick: bool=True, decimals: int=2) -> list[str]:

    bucket_size = (src.High.max() - (floor := src.Low.min())) / height
    max_width = (len(prefix) if prefix else 0) + (len(suffix) if suffix else 0) + len(str(int(src.Close.iloc[-1]))) + (decimals + 1 if decimals else 0) + (1 if include_tick else 0) + rpad + lpad + 2
    
    column = []

    for n_bucket in range(height):

        if n_bucket % n_ticks == 0:
            
            bucket_mean = n_bucket * bucket_size + floor + (bucket_size / 2)
            column.append(((prefix if prefix else '') + (' ' * rpad) + str(round(bucket_mean, decimals)) + (f' {tick_char}' if include_tick else ' ') + (prefix if prefix else '') + (' ' * rpad)).rjust(max_width))

        else:
            column.append((axis_char + (' ' * rpad)).rjust(max_width))


    return column




def get_x_axis(src: pd.DataFrame, width: int=3, n_ticks: int=5, lpad: int=1, axis_char: str='─', tick_char: str='┬', include_tick: bool=True, tformat: str='%H:%M', align_timestamps: Literal['left', 'center', 'right']='center') -> list[list[str]]:

    length = len(src) * width

    timestamp_width = len(src.index[0].strftime(tformat))
    axis, timestamps = [], []

    for n_bucket in range(length):

        if n_bucket % (n_ticks * width) == 0:

            axis.append(tick_char if include_tick else axis_char)
            timestamp = src.index[n_bucket // width].strftime(tformat)

            del timestamps[n_bucket - (timestamp_width - 1): n_bucket]
            
            for c in timestamp:
                timestamps.append(c)

        else:
            axis.append(axis_char)
            timestamps.append(' ')


    for _ in range(lpad):
        axis.insert(0, ' ')
        timestamps.insert(0, ' ')

    if align_timestamps == 'left':
        timestamps = timestamps[timestamp_width - 1:]

    elif align_timestamps == 'center':
        timestamps = timestamps[timestamp_width // 2:]
        



    return [axis, timestamps]



