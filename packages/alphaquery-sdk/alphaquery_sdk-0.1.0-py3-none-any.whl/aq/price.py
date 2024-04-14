import pandas as pd
import requests
from aq.util import URL

def price_history(symbol: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Get daily historical price data for a symbol."""
    r = requests.get(f'{URL}/stock-price-chart?ticker={symbol}')
    r.raise_for_status()
    adjusted = r.json()['adjusted']
    unadjusted = r.json()['unadjusted']

    return (pd.DataFrame(adjusted), pd.DataFrame(unadjusted))