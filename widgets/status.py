import pandas as pd
from .utils import DecoratedString









def get_status_bar(src: pd.DataFrame, 
               prev_close: float,
               lpad: int=1,
               decimals: int=2,
               color_up: str='green',
               color_down: str='red',
               prefix: str='│',
               ) -> str:
    
    change = round(src.Close.iloc[-1] - prev_close, decimals)
    pct_change = round((src.Close.iloc[-1] - prev_close) / prev_close * 100, decimals)
    
    c = lambda s: DecoratedString(s, color=(color_up if change > 0 else color_down))

    return f'{" " * lpad}{prefix} O: {c(round(src.Open.iloc[-1], decimals))} C: {c(round(src.Close.iloc[-1], decimals))} L: {c(round(src.Low.iloc[-1], decimals))} H: {c(round(src.High.iloc[-1], decimals))} | {c(f"{change} ({pct_change}%)")}'


