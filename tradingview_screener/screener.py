from __future__ import annotations

import json
from enum import Enum
from typing import Iterable

import requests
import pandas as pd


URL = 'https://scanner.tradingview.com/america/scan'
HEADERS = {
    'authority': 'scanner.tradingview.com',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
    'accept': 'text/plain, */*; q=0.01',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'sec-ch-ua-mobile': '?0',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/98.0.4758.102 Safari/537.36',
    'sec-ch-ua-platform': '"Windows"',
    'origin': 'https://www.tradingview.com',
    'sec-fetch-site': 'same-site',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://www.tradingview.com/',
    'accept-language': 'en-US,en;q=0.9,it;q=0.8',
}
COLUMNS = {
    '1-Month High': 'High.1M',
    '1-Month Low': 'Low.1M',
    '1-Year Beta': 'beta_1_year',
    '3-Month High': 'High.3M',
    '3-Month Low': 'Low.3M',
    '3-Month Performance': 'Perf.3M',
    '52 Week High': 'price_52_week_high',
    '52 Week Low': 'price_52_week_low',
    '5Y Performance': 'Perf.5Y',
    '6-Month High': 'High.6M',
    '6-Month Low': 'Low.6M',
    '6-Month Performance': 'Perf.6M',
    'All Time High': 'High.All',
    'All Time Low': 'Low.All',
    'All Time Performance': 'Perf.All',
    'Aroon Down (14)': 'Aroon.Down',
    'Aroon Up (14)': 'Aroon.Up',
    'Average Day Range (14)': 'ADR',
    'Average Directional Index (14)': 'ADX',
    'Average True Range (14)': 'ATR',
    'Average Volume (10 day)': 'average_volume_10d_calc',
    'Average Volume (30 day)': 'average_volume_30d_calc',
    'Average Volume (60 day)': 'average_volume_60d_calc',
    'Average Volume (90 day)': 'average_volume_90d_calc',
    'Awesome Oscillator': 'AO',
    'Basic EPS (FY)': 'basic_eps_net_income',
    'Basic EPS (TTM)': 'earnings_per_share_basic_ttm',
    'Bollinger Lower Band (20)': 'BB.lower',
    'Bollinger Upper Band (20)': 'BB.upper',
    'Bull Bear Power': 'BBPower',
    'Cash & Equivalents (FY)': 'cash_n_equivalents_fy',
    'Cash & Equivalents (MRQ)': 'cash_n_equivalents_fq',
    'Cash and short term investments (FY)': 'cash_n_short_term_invest_fy',
    'Cash and short term investments (MRQ)': 'cash_n_short_term_invest_fq',
    'Chaikin Money Flow (20)': 'ChaikinMoneyFlow',
    'Change': 'change_abs',
    'Change %': 'change',
    'Change 15m': 'change_abs.15',
    'Change 15m, %': 'change.15',
    'Change 1h': 'change_abs.60',
    'Change 1h, %': 'change.60',
    'Change 1m': 'change_abs.1',
    'Change 1M': 'change_abs.1M',
    'Change 1m, %': 'change.1',
    'Change 1M, %': 'change.1M',
    'Change 1W': 'change_abs.1W',
    'Change 1W, %': 'change.1W',
    'Change 4h': 'change_abs.240',
    'Change 4h, %': 'change.240',
    'Change 5m': 'change_abs.5',
    'Change 5m, %': 'change.5',
    'Change from Open': 'change_from_open_abs',
    'Change from Open %': 'change_from_open',
    'Commodity Channel Index (20)': 'CCI20',
    'Country': 'country',
    'Current Ratio (MRQ)': 'current_ratio',
    'Debt to Equity Ratio (MRQ)': 'debt_to_equity',
    'Dividend Yield Forward': 'dividend_yield_recent',
    'Dividends Paid (FY)': 'dividends_paid',
    'Dividends per share (Annual YoY Growth)': 'dps_common_stock_prim_issue_yoy_growth_fy',
    'Dividends per Share (FY)': 'dps_common_stock_prim_issue_fy',
    'Dividends per Share (MRQ)': 'dividends_per_share_fq',
    'Donchian Channels Lower Band (20)': 'DonchCh20.Lower',
    'Donchian Channels Upper Band (20)': 'DonchCh20.Upper',
    'EBITDA (Annual YoY Growth)': 'ebitda_yoy_growth_fy',
    'EBITDA (Quarterly QoQ Growth)': 'ebitda_qoq_growth_fq',
    'EBITDA (Quarterly YoY Growth)': 'ebitda_yoy_growth_fq',
    'EBITDA (TTM YoY Growth)': 'ebitda_yoy_growth_ttm',
    'EBITDA (TTM)': 'ebitda',
    'Enterprise Value (MRQ)': 'enterprise_value_fq',
    'Enterprise Value/EBITDA (TTM)': 'enterprise_value_ebitda_ttm',
    'EPS Diluted (Annual YoY Growth)': 'earnings_per_share_diluted_yoy_growth_fy',
    'EPS Diluted (FY)': 'last_annual_eps',
    'EPS Diluted (MRQ)': 'earnings_per_share_fq',
    'EPS Diluted (Quarterly QoQ Growth)': 'earnings_per_share_diluted_qoq_growth_fq',
    'EPS Diluted (Quarterly YoY Growth)': 'earnings_per_share_diluted_yoy_growth_fq',
    'EPS Diluted (TTM YoY Growth)': 'earnings_per_share_diluted_yoy_growth_ttm',
    'EPS Diluted (TTM)': 'earnings_per_share_diluted_ttm',
    'EPS Forecast (MRQ)': 'earnings_per_share_forecast_next_fq',
    'Exchange': 'exchange',
    'Exponential Moving Average (10)': 'EMA10',
    'Exponential Moving Average (100)': 'EMA100',
    'Exponential Moving Average (20)': 'EMA20',
    'Exponential Moving Average (200)': 'EMA200',
    'Exponential Moving Average (30)': 'EMA30',
    'Exponential Moving Average (5)': 'EMA5',
    'Exponential Moving Average (50)': 'EMA50',
    'Free Cash Flow (Annual YoY Growth)': 'free_cash_flow_yoy_growth_fy',
    'Free Cash Flow (Quarterly QoQ Growth)': 'free_cash_flow_qoq_growth_fq',
    'Free Cash Flow (Quarterly YoY Growth)': 'free_cash_flow_yoy_growth_fq',
    'Free Cash Flow (TTM YoY Growth)': 'free_cash_flow_yoy_growth_ttm',
    'Free Cash Flow Margin (FY)': 'free_cash_flow_margin_fy',
    'Free Cash Flow Margin (TTM)': 'free_cash_flow_margin_ttm',
    'Gap %': 'gap',
    'Goodwill': 'goodwill',
    'Gross Margin (FY)': 'gross_profit_margin_fy',
    'Gross Margin (TTM)': 'gross_margin',
    'Gross Profit (Annual YoY Growth)': 'gross_profit_yoy_growth_fy',
    'Gross Profit (FY)': 'gross_profit',
    'Gross Profit (MRQ)': 'gross_profit_fq',
    'Gross Profit (Quarterly QoQ Growth)': 'gross_profit_qoq_growth_fq',
    'Gross Profit (Quarterly YoY Growth)': 'gross_profit_yoy_growth_fq',
    'Gross Profit (TTM YoY Growth)': 'gross_profit_yoy_growth_ttm',
    'High': 'high',
    'Hull Moving Average (9)': 'HullMA9',
    'Ichimoku Base Line (9, 26, 52, 26)': 'Ichimoku.BLine',
    'Ichimoku Conversion Line (9, 26, 52, 26)': 'Ichimoku.CLine',
    'Ichimoku Leading Span A (9, 26, 52, 26)': 'Ichimoku.Lead1',
    'Ichimoku Leading Span B (9, 26, 52, 26)': 'Ichimoku.Lead2',
    'Industry': 'industry',
    'Keltner Channels Lower Band (20)': 'KltChnl.lower',
    'Keltner Channels Upper Band (20)': 'KltChnl.upper',
    'Last Year Revenue (FY)': 'last_annual_revenue',
    'Low': 'low',
    'MACD Level (12, 26)': 'MACD.macd',
    'MACD Signal (12, 26)': 'MACD.signal',
    'Market Capitalization': 'market_cap_basic',
    'Momentum (10)': 'Mom',
    'Money Flow (14)': 'MoneyFlow',
    'Monthly Performance': 'Perf.1M',
    'Moving Averages Rating': 'Recommend.MA',
    'Negative Directional Indicator (14)': 'ADX-DI',
    'Net Debt (MRQ)': 'net_debt',
    'Net Income (Annual YoY Growth)': 'net_income_yoy_growth_fy',
    'Net Income (FY)': 'net_income',
    'Net Income (Quarterly QoQ Growth)': 'net_income_qoq_growth_fq',
    'Net Income (Quarterly YoY Growth)': 'net_income_yoy_growth_fq',
    'Net Income (TTM YoY Growth)': 'net_income_yoy_growth_ttm',
    'Net Margin (FY)': 'net_income_bef_disc_oper_margin_fy',
    'Net Margin (TTM)': 'after_tax_margin',
    'Number of Employees': 'number_of_employees',
    'Number of Shareholders': 'number_of_shareholders',
    'Open': 'open',
    'Operating Margin (FY)': 'oper_income_margin_fy',
    'Operating Margin (TTM)': 'operating_margin',
    'Oscillators Rating': 'Recommend.Other',
    'Parabolic SAR': 'P.SAR',
    'Pattern': 'candlestick',
    'Pivot Camarilla P': 'Pivot.M.Camarilla.Middle',
    'Pivot Camarilla R1': 'Pivot.M.Camarilla.R1',
    'Pivot Camarilla R2': 'Pivot.M.Camarilla.R2',
    'Pivot Camarilla R3': 'Pivot.M.Camarilla.R3',
    'Pivot Camarilla S1': 'Pivot.M.Camarilla.S1',
    'Pivot Camarilla S2': 'Pivot.M.Camarilla.S2',
    'Pivot Camarilla S3': 'Pivot.M.Camarilla.S3',
    'Pivot Classic P': 'Pivot.M.Classic.Middle',
    'Pivot Classic R1': 'Pivot.M.Classic.R1',
    'Pivot Classic R2': 'Pivot.M.Classic.R2',
    'Pivot Classic R3': 'Pivot.M.Classic.R3',
    'Pivot Classic S1': 'Pivot.M.Classic.S1',
    'Pivot Classic S2': 'Pivot.M.Classic.S2',
    'Pivot Classic S3': 'Pivot.M.Classic.S3',
    'Pivot DM P': 'Pivot.M.Demark.Middle',
    'Pivot DM R1': 'Pivot.M.Demark.R1',
    'Pivot DM S1': 'Pivot.M.Demark.S1',
    'Pivot Fibonacci P': 'Pivot.M.Fibonacci.Middle',
    'Pivot Fibonacci R1': 'Pivot.M.Fibonacci.R1',
    'Pivot Fibonacci R2': 'Pivot.M.Fibonacci.R2',
    'Pivot Fibonacci R3': 'Pivot.M.Fibonacci.R3',
    'Pivot Fibonacci S1': 'Pivot.M.Fibonacci.S1',
    'Pivot Fibonacci S2': 'Pivot.M.Fibonacci.S2',
    'Pivot Fibonacci S3': 'Pivot.M.Fibonacci.S3',
    'Pivot Woodie P': 'Pivot.M.Woodie.Middle',
    'Pivot Woodie R1': 'Pivot.M.Woodie.R1',
    'Pivot Woodie R2': 'Pivot.M.Woodie.R2',
    'Pivot Woodie R3': 'Pivot.M.Woodie.R3',
    'Pivot Woodie S1': 'Pivot.M.Woodie.S1',
    'Pivot Woodie S2': 'Pivot.M.Woodie.S2',
    'Pivot Woodie S3': 'Pivot.M.Woodie.S3',
    'Positive Directional Indicator (14)': 'ADX+DI',
    'Post-market Change': 'postmarket_change_abs',
    'Post-market Change %': 'postmarket_change',
    'Post-market Close': 'postmarket_close',
    'Post-market High': 'postmarket_high',
    'Post-market Low': 'postmarket_low',
    'Post-market Open': 'postmarket_open',
    'Post-market Volume': 'postmarket_volume',
    'Pre-market Change': 'premarket_change_abs',
    'Pre-market Change %': 'premarket_change',
    'Pre-market Change from Open': 'premarket_change_from_open_abs',
    'Pre-market Change from Open %': 'premarket_change_from_open',
    'Pre-market Close': 'premarket_close',
    'Pre-market Gap %': 'premarket_gap',
    'Pre-market High': 'premarket_high',
    'Pre-market Low': 'premarket_low',
    'Pre-market Open': 'premarket_open',
    'Pre-market Volume': 'premarket_volume',
    'Pretax Margin (TTM)': 'pre_tax_margin',
    'Price': 'close',
    'Price to Book (FY)': 'price_book_ratio',
    'Price to Book (MRQ)': 'price_book_fq',
    'Price to Earnings Ratio (TTM)': 'price_earnings_ttm',
    'Price to Free Cash Flow (TTM)': 'price_free_cash_flow_ttm',
    'Price to Revenue Ratio (TTM)': 'price_revenue_ttm',
    'Price to Sales (FY)': 'price_sales_ratio',
    'Quick Ratio (MRQ)': 'quick_ratio',
    'Rate Of Change (9)': 'ROC',
    'Recent Earnings Date': 'earnings_release_date',
    'Relative Strength Index (14)': 'RSI',
    'Relative Strength Index (7)': 'RSI7',
    'Relative Volume': 'relative_volume_10d_calc',
    'Relative Volume at Time': 'relative_volume_intraday|5',  # replaced '.' with '|'
    'Research & development Ratio (FY)': 'research_and_dev_ratio_fy',
    'Research & development Ratio (TTM)': 'research_and_dev_ratio_ttm',
    'Return on Assets (TTM)': 'return_on_assets',
    'Return on Equity (TTM)': 'return_on_equity',
    'Return on Invested Capital (TTM)': 'return_on_invested_capital',
    'Revenue (Annual YoY Growth)': 'total_revenue_yoy_growth_fy',
    'Revenue (Quarterly QoQ Growth)': 'total_revenue_qoq_growth_fq',
    'Revenue (Quarterly YoY Growth)': 'total_revenue_yoy_growth_fq',
    'Revenue (TTM YoY Growth)': 'total_revenue_yoy_growth_ttm',
    'Revenue per Employee (FY)': 'revenue_per_employee',
    'Sector': 'sector',
    'Selling General & Admin expenses Ratio (FY)': 'sell_gen_admin_exp_other_ratio_fy',
    'Selling General & Admin expenses Ratio (TTM)': 'sell_gen_admin_exp_other_ratio_ttm',
    'Shares Float': 'float_shares_outstanding',
    'Simple Moving Average (10)': 'SMA10',
    'Simple Moving Average (100)': 'SMA100',
    'Simple Moving Average (20)': 'SMA20',
    'Simple Moving Average (200)': 'SMA200',
    'Simple Moving Average (30)': 'SMA30',
    'Simple Moving Average (5)': 'SMA5',
    'Simple Moving Average (50)': 'SMA50',
    'Stochastic %D (14, 3, 3)': 'Stoch.D',
    'Stochastic %K (14, 3, 3)': 'Stoch.K',
    'Stochastic RSI Fast (3, 3, 14, 14)': 'Stoch.RSI.K',
    'Stochastic RSI Slow (3, 3, 14, 14)': 'Stoch.RSI.D',
    'Submarket': 'submarket',
    'Technical Rating': 'Recommend.All',
    'Total Assets (Annual YoY Growth)': 'total_assets_yoy_growth_fy',
    'Total Assets (MRQ)': 'total_assets',
    'Total Assets (Quarterly QoQ Growth)': 'total_assets_qoq_growth_fq',
    'Total Assets (Quarterly YoY Growth)': 'total_assets_yoy_growth_fq',
    'Total Current Assets (MRQ)': 'total_current_assets',
    'Total Debt (Annual YoY Growth)': 'total_debt_yoy_growth_fy',
    'Total Debt (MRQ)': 'total_debt',
    'Total Debt (Quarterly QoQ Growth)': 'total_debt_qoq_growth_fq',
    'Total Debt (Quarterly YoY Growth)': 'total_debt_yoy_growth_fq',
    'Total Liabilities (FY)': 'total_liabilities_fy',
    'Total Liabilities (MRQ)': 'total_liabilities_fq',
    'Total Revenue (FY)': 'total_revenue',
    'Total Shares Outstanding': 'total_shares_outstanding_fundamental',
    'Ultimate Oscillator (7, 14, 28)': 'UO',
    'Upcoming Earnings Date': 'earnings_release_next_date',
    'Volatility': 'Volatility.D',
    'Volatility Month': 'Volatility.M',
    'Volatility Week': 'Volatility.W',
    'Volume': 'volume',
    'Volume Weighted Average Price': 'VWAP',
    'Volume Weighted Moving Average (20)': 'VWMA',
    'Volume*Price': 'Value.Traded',
    'Weekly Performance': 'Perf.W',
    'Williams Percent Range (14)': 'W.R',
    'Yearly Performance': 'Perf.Y',
    'YTD Performance': 'Perf.YTD',
    'type': 'type',
    'subtype': 'subtype',
    'name': 'name',
    'logoid': 'logoid',
}  # TODO: test all columns
API_SETTINGS = {
    'filter': [{'left': 'type', 'operation': 'equal', 'right': 'stock'},
               {'left': 'subtype', 'operation': 'in_range', 'right': ['common', 'foreign-issuer']},
               {'left': 'exchange', 'operation': 'in_range', 'right': ['AMEX', 'NASDAQ', 'NYSE']}],
    'options': {'lang': 'en'},
    'markets': ['america'],
    'symbols': {'query': {'types': []}, 'tickers': []},
    'columns': ['name', 'close', 'volume', 'market_cap_basic'],
    # 'sort': {},  # the sortBy value should be replaced with a column name
    'range': [0, 50]
}


class Scanner(dict, Enum):
    premarket_gainers = {'sortBy': 'premarket_change', 'sortOrder': 'desc'}
    premarket_losers = {'sortBy': 'premarket_change', 'sortOrder': 'asc'}
    premarket_most_active = {'sortBy': 'premarket_volume', 'sortOrder': 'desc'}
    premarket_gappers = {'sortBy': 'premarket_gap', 'sortOrder': 'desc'}

    postmarket_gainers = {'sortBy': 'postmarket_change', 'sortOrder': 'desc'}
    postmarket_losers = {'sortBy': 'postmarket_change', 'sortOrder': 'asc'}
    postmarket_most_active = {'sortBy': 'postmarket_volume', 'sortOrder': 'desc'}

    @classmethod
    def names(cls) -> list[str]:
        return [x.name for x in cls]

    def get_data(self, **kwargs) -> pd.DataFrame:
        cols = API_SETTINGS['columns'].copy()
        cols.insert(1, self.value['sortBy'])  # insert the column that we are sorting by, right after the symbol column
        kwargs.setdefault('columns', cols)  # use `setdefault()` so the user can override this
        return get_scanner_data(sort=self.value, **kwargs)[1]


def get_scanner_data(**kwargs) -> tuple[int, pd.DataFrame]:
    """
    Get a dataframe with the scanner data directly from the API

    :param kwargs: kwargs to override fields in the `local_settings` dictionary
    :return: Pandas DataFrame
    """
    local_settings = API_SETTINGS.copy()  # copy() to avoid modifying the global settings
    local_settings.update(**kwargs)

    r = requests.post(URL, headers=HEADERS, data=json.dumps(local_settings))
    r.raise_for_status()

    json_obj = r.json()
    rows_count = json_obj['totalCount']
    data = json_obj['data']

    if data is None:
        return rows_count, pd.DataFrame(columns=local_settings['columns'])
    return rows_count, pd.DataFrame(data=(row['d'] for row in data), columns=local_settings['columns'])


def get_all_symbols(exchanges: Iterable[str] = ('AMEX', 'OTC', 'NYSE', 'NASDAQ')) -> list[str]:
    """
    Get a list with all the symbols filtered by a given exchange.

    Valid exchanges: {'AMEX', 'OTC', 'NYSE', 'NASDAQ'}

    :param exchanges: a set which contains the exchanges you want to keep (all the rest will be ignored)
    :return: list of symbols
    """
    exchanges = {x.upper() for x in exchanges}
    r = requests.get(URL)
    data = r.json()['data']  # [{'s': 'NYSE:HKD', 'd': []}, {'s': 'NASDAQ:ALTY', 'd': []}...]

    symbols = []
    for dct in data:
        exchange, symbol = dct['s'].split(':')
        if exchange in exchanges:
            symbols.append(symbol)
    return symbols
