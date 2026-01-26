# ============================================
# DATA FETCHER - YAHOO FINANCE
# ============================================

import yfinance as yf
import pandas as pd
from typing import Optional, List
import time
import logging

logger = logging.getLogger(__name__)


def fetch_stock_data(ticker: str, period: str = "60d", interval: str = "15m") -> Optional[pd.DataFrame]:
    """
    Fetch stock data from Yahoo Finance
    
    Args:
        ticker: Stock ticker (e.g., 'BBCA.JK')
        period: Data period (e.g., '60d', '1mo')
        interval: Candlestick interval (e.g., '15m', '1h', '1d')
    
    Returns:
        DataFrame with OHLCV data or None if error
    """
    try:
        stock = yf.Ticker(ticker)
        df = stock.history(period=period, interval=interval)
        
        if df.empty:
            logger.warning(f"No data for {ticker}")
            return None
        
        # Standardize column names to lowercase
        df.columns = df.columns.str.lower()
        
        # Ensure required columns exist
        required_cols = ['open', 'high', 'low', 'close', 'volume']
        if not all(col in df.columns for col in required_cols):
            logger.warning(f"Missing columns for {ticker}")
            return None
        
        # Remove timezone info if present
        if df.index.tz is not None:
            df.index = df.index.tz_localize(None)
        
        return df
        
    except Exception as e:
        logger.error(f"Error fetching {ticker}: {str(e)}")
        return None


def fetch_multiple_stocks(tickers: List[str], period: str = "60d", interval: str = "15m", 
                          delay: float = 0.1) -> dict:
    """
    Fetch data for multiple stocks with rate limiting
    
    Args:
        tickers: List of stock tickers
        period: Data period
        interval: Candlestick interval
        delay: Delay between requests (seconds)
    
    Returns:
        Dictionary of {ticker: DataFrame}
    """
    results = {}
    total = len(tickers)
    
    for i, ticker in enumerate(tickers):
        if (i + 1) % 50 == 0:
            logger.info(f"Fetching progress: {i + 1}/{total}")
        
        df = fetch_stock_data(ticker, period, interval)
        if df is not None and len(df) > 0:
            results[ticker] = df
        
        # Rate limiting
        time.sleep(delay)
    
    logger.info(f"Successfully fetched {len(results)}/{total} stocks")
    return results


def get_latest_data(df: pd.DataFrame) -> dict:
    """Get latest candle data as dictionary"""
    if df is None or len(df) == 0:
        return {}
    
    latest = df.iloc[-1]
    return {
        'open': latest['open'],
        'high': latest['high'],
        'low': latest['low'],
        'close': latest['close'],
        'volume': latest['volume'],
        'timestamp': df.index[-1]
    }


def get_price_change(df: pd.DataFrame) -> float:
    """Calculate price change percentage from previous close"""
    if df is None or len(df) < 2:
        return 0.0
    
    current = df['close'].iloc[-1]
    previous = df['close'].iloc[-2]
    
    if previous == 0:
        return 0.0
    
    return ((current - previous) / previous) * 100
