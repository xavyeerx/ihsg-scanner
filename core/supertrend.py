# ============================================
# SUPERTREND CALCULATION
# ============================================
# Matches Pine Script v3 logic exactly

import pandas as pd
import numpy as np


def calculate_supertrend(df: pd.DataFrame, period: int = 10, multiplier: float = 3.0) -> pd.DataFrame:
    """
    Calculate Supertrend indicator (matching Pine Script ta.supertrend)
    
    Args:
        df: DataFrame with 'high', 'low', 'close' columns
        period: ATR period (default 10)
        multiplier: ATR multiplier (default 3.0)
    
    Returns:
        DataFrame with additional columns:
        - supertrend: Supertrend value
        - direction: 1 for bullish (green), -1 for bearish (red)
        - bullish_break: True when price crosses above supertrend
        - bearish_break: True when price crosses below supertrend
    """
    df = df.copy()
    
    # Reset index if it's a DatetimeIndex (for safer iteration)
    original_index = df.index
    df = df.reset_index(drop=True)
    
    # Calculate ATR
    df['tr1'] = df['high'] - df['low']
    df['tr2'] = abs(df['high'] - df['close'].shift(1))
    df['tr3'] = abs(df['low'] - df['close'].shift(1))
    df['tr'] = df[['tr1', 'tr2', 'tr3']].max(axis=1)
    df['atr'] = df['tr'].rolling(window=period).mean()
    
    # Calculate basic upper and lower bands
    hl2 = (df['high'] + df['low']) / 2
    basic_upper = (hl2 + (multiplier * df['atr'])).values
    basic_lower = (hl2 - (multiplier * df['atr'])).values
    
    # Use lists for iteration (more reliable than pandas loc)
    n = len(df)
    upper_band = basic_upper.copy()
    lower_band = basic_lower.copy()
    direction = np.ones(n, dtype=int)  # Start with bullish
    close = df['close'].values
    
    for i in range(1, n):
        # Skip if ATR not yet available (NaN)
        if pd.isna(basic_upper[i]) or pd.isna(upper_band[i-1]):
            continue
            
        # Upper band logic
        if basic_upper[i] < upper_band[i-1] or close[i-1] > upper_band[i-1]:
            upper_band[i] = basic_upper[i]
        else:
            upper_band[i] = upper_band[i-1]
        
        # Lower band logic
        if basic_lower[i] > lower_band[i-1] or close[i-1] < lower_band[i-1]:
            lower_band[i] = basic_lower[i]
        else:
            lower_band[i] = lower_band[i-1]
        
        # Direction logic
        if direction[i-1] == -1:  # Was bearish
            if close[i] > upper_band[i-1]:
                direction[i] = 1  # Switch to bullish
            else:
                direction[i] = -1
        else:  # Was bullish
            if close[i] < lower_band[i-1]:
                direction[i] = -1  # Switch to bearish
            else:
                direction[i] = 1
    
    df['upper_band'] = upper_band
    df['lower_band'] = lower_band
    df['direction'] = direction
    
    # Set supertrend value based on direction
    df['supertrend'] = np.where(direction == 1, lower_band, upper_band)
    
    # Detect breakouts using CROSSOVER logic (matching Pine Script)
    # breakoutUp = ta.crossover(close, supertrend)
    # breakoutDown = ta.crossunder(close, supertrend)
    supertrend = df['supertrend'].values
    prev_close = np.roll(close, 1)
    prev_supertrend = np.roll(supertrend, 1)
    
    # Bullish break: previous close was below/equal supertrend, current close is above
    df['bullish_break'] = (prev_close <= prev_supertrend) & (close > supertrend)
    df['bearish_break'] = (prev_close >= prev_supertrend) & (close < supertrend)
    
    # First bar can't have a break
    df.loc[0, 'bullish_break'] = False
    df.loc[0, 'bearish_break'] = False
    
    # Direction change detection
    df['supertrend_changed'] = df['direction'] != df['direction'].shift(1)
    
    # Clean up intermediate columns
    df = df.drop(columns=['tr1', 'tr2', 'tr3', 'tr'], errors='ignore')
    
    # Restore original index
    df.index = original_index
    
    return df


def is_bullish(df: pd.DataFrame) -> bool:
    """Check if current trend is bullish"""
    if len(df) == 0:
        return False
    return df['direction'].iloc[-1] == 1


def is_bearish(df: pd.DataFrame) -> bool:
    """Check if current trend is bearish"""
    if len(df) == 0:
        return True
    return df['direction'].iloc[-1] == -1


def get_supertrend_value(df: pd.DataFrame) -> float:
    """Get current supertrend value"""
    if len(df) == 0:
        return 0.0
    return df['supertrend'].iloc[-1]


def just_turned_bullish(df: pd.DataFrame) -> bool:
    """Check if supertrend just turned bullish (break up)"""
    if len(df) < 2:
        return False
    return bool(df['bullish_break'].iloc[-1])


def just_turned_bearish(df: pd.DataFrame) -> bool:
    """Check if supertrend just turned bearish (break down)"""
    if len(df) < 2:
        return False
    return bool(df['bearish_break'].iloc[-1])
