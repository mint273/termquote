import yfinance as yf
from widgets import CandlestickChart
import argparse








if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument('symbol', type=str, help='Stock Ticker')
    parser.add_argument('-i', '--interval', type=str, default='2m', help='Interval')
    parser.add_argument('-p', '--period', type=str, default='1d', help='Period')
    parser.add_argument('-c', '--exclude-current', action='store_true', help='Exclude Current Price Line')
    parser.add_argument('-s', '--exclude-status-bar', action='store_true', help='Exclude Current Quote')

    args = parser.parse_args()



    candlestick_chart = CandlestickChart(color_up='green', color_down='red', include_current=not args.exclude_current, include_status_bar=not args.exclude_status_bar)


    src = yf.Ticker(args.symbol).history(period=args.period, interval=args.interval)
    prev_close = yf.Ticker(args.symbol).history(period='5d', interval='1d').Close.iloc[-2] if not args.exclude_status_bar else None



    candlestick_chart.plot(src, prev_close)


