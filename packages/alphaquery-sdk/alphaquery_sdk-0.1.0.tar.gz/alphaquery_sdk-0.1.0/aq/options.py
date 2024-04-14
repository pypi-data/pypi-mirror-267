
# https://www.alphaquery.com/data/option-statistic-chart?ticker=MSFT&perType=30-Day&identifier=historical-volatility
import pandas as pd
import requests
from aq.util import URL

def option_statistic_chart(symbol: str, perType: str = "30-Day", identifier: str = "historical-volatility") -> tuple[pd.DataFrame, pd.DataFrame]:
    r = requests.get(f'{URL}/option-statistic-chart?ticker={symbol}&perType={perType}&identifier={identifier}')
    r.raise_for_status()
    return pd.DataFrame(r.json())

def historical_volatility(symbol: str, window: int = 30) -> pd.DataFrame:
    """Calculate the historical volatility of a symbol."""
    return option_statistic_chart(symbol, perType=f'{window}-Day', identifier=f'historical-volatility')

def parkinson_volatility(symbol: str, window: int = 30) -> pd.DataFrame:
    """Calculate the Parkinson volatility of a symbol."""
    return option_statistic_chart(symbol, perType=f'{window}-Day', identifier='parkinson-historical-volatility')

def implied_volatility_calls(symbol: str, window: int = 30) -> pd.DataFrame:
    """Calculate the implied volatility of a symbol."""
    return option_statistic_chart(symbol, perType=f'{window}-Day', identifier='iv-call')

def implied_volatility_puts(symbol: str, window: int = 30) -> pd.DataFrame:
    """Calculate the implied volatility of a symbol."""
    return option_statistic_chart(symbol, perType=f'{window}-Day', identifier='iv-put')

def implied_volatility(symbol: str, window: int = 30) -> pd.DataFrame:
    """Calculate the implied volatility of a symbol."""
    return option_statistic_chart(symbol, perType=f'{window}-Day', identifier='iv-mean')


