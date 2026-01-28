# ============================================
# SCANNER - MAIN SCANNING LOGIC
# ============================================

import pandas as pd
from typing import Dict, List, Tuple
import logging

from config.settings import MIN_DAILY_TURNOVER
from .supertrend import calculate_supertrend, is_bullish, just_turned_bullish, just_turned_bearish
from .indicators import calculate_all_indicators
from .scoring import calculate_total_score

logger = logging.getLogger(__name__)


class ScanResult:
    """Container for scan results"""
    def __init__(self, ticker: str):
        self.ticker = ticker
        self.price = 0.0
        self.change_percent = 0.0
        self.supertrend_value = 0.0
        self.is_bullish = False
        self.score = 0
        self.status = "UNKNOWN"
        self.status_emoji = "⚪"
        
        # Signals
        self.bullish_break = False
        self.bearish_break = False
        self.is_stoch_crossover = False  # Stoch RSI Crossover signal
        self.stoch_k = 0.0  # Current Stoch K value
        self.stoch_d = 0.0  # Current Stoch D value
        self.is_accumulation = False
        self.is_early_entry = False  # Early Entry (Serok Bawah) signal
        self.correction_percent = 0.0  # Price correction from high
        self.early_entry_strength = 0  # Signal strength score
        
        # Additional info
        self.volume_ratio = 0.0
        self.stoch_k = 0.0
        self.daily_turnover = 0.0
        self.avg_turnover_5d = 0.0


def analyze_stock(ticker: str, df: pd.DataFrame, previous_state: dict = None) -> ScanResult:
    """
    Analyze a single stock and detect signals
    
    Args:
        ticker: Stock ticker
        df: OHLCV DataFrame
        previous_state: Previous state from state manager
    
    Returns:
        ScanResult with all signals detected
    """
    result = ScanResult(ticker)
    
    if df is None or len(df) < 50:
        return result
    
    try:
        # Calculate turnover (Price * Volume)
        # Use 5-day average turnover to filter liquid stocks
        df['turnover'] = df['close'] * df['volume']
        avg_turnover_5d = df['turnover'].rolling(window=5).mean().iloc[-1]
        
        result.daily_turnover = df['turnover'].iloc[-1]
        result.avg_turnover_5d = avg_turnover_5d
        
        # Filter by liquidity
        if avg_turnover_5d < MIN_DAILY_TURNOVER:
            # We still analyze it for state-keeping purposes, but we could skip alerts
            # Or we can mark it as illiquid
            pass
            
        # Calculate all indicators
        df = calculate_supertrend(df)
        df = calculate_all_indicators(df)
        
        latest = df.iloc[-1]
        
        # Basic info
        result.price = latest['close']
        result.supertrend_value = latest['supertrend']
        result.is_bullish = latest['direction'] == 1
        result.volume_ratio = latest.get('volume_ratio', 1.0)
        result.stoch_k = latest.get('stoch_k', 50.0)
        
        # Price change
        if len(df) >= 2:
            prev_close = df['close'].iloc[-2]
            if prev_close > 0:
                result.change_percent = ((result.price - prev_close) / prev_close) * 100
        
        # Score and status
        result.score, result.status, result.status_emoji = calculate_total_score(df)
        
        # === SIGNAL DETECTION (ALL DAILY TF) ===
        
        # 1. Supertrend break (Daily)
        result.bullish_break = just_turned_bullish(df)
        result.bearish_break = just_turned_bearish(df)
        
        # 2. STOCH RSI CROSSOVER Signal
        # Logic: Stoch K crosses above Stoch D (bullish crossover)
        # Best when happening in oversold area or after pullback
        stoch_k = latest.get('stoch_k', 50.0)
        stoch_d = latest.get('stoch_d', 50.0)
        stoch_k_cross_up = latest.get('stoch_k_cross_up', False)
        
        result.stoch_k = stoch_k
        result.stoch_d = stoch_d
        
        # Stoch Crossover conditions:
        # 1. K just crossed above D (crossover)
        # 2. Stock still in bullish trend
        if result.is_bullish and stoch_k_cross_up:
            result.is_stoch_crossover = True
        
        # 3. ACC Signal (Daily) - Accumulation Detection
        # Conditions: Bullish + Bullish Candle (green) + Volume Spike + Not Sideways
        # Bullish candle filters out distribution (red candle with volume like AMMN)
        is_volume_signal = latest.get('is_volume_spike', False) or latest.get('is_unusual_volume', False)
        is_bullish_candle = latest.get('close', 0) > latest.get('open', 0) if 'open' in df.columns else False
        is_not_sideways = not latest.get('is_sideways', False)
        
        # ACC = Bullish + Green candle + Volume spike + Not sideways
        if result.is_bullish and is_bullish_candle and is_volume_signal and is_not_sideways:
            result.is_accumulation = True


        # 4. EARLY ENTRY (Serok Bawah) Signal - Anomaly-based Detection
        # GOAL: Find stocks that dropped enough WITHOUT selling pressure,
        #       then showing signs of price defense or early buying
        
        # Calculate drop from PREVIOUS CLOSE (not from high)
        if len(df) >= 2:
            prev_close = df['close'].iloc[-2]
            current_close = latest.get('close', 0)
            drop_from_prev_close = ((prev_close - current_close) / prev_close) * 100
        else:
            drop_from_prev_close = 0
        
        is_healthy_correction = latest.get('is_healthy_correction', False)
        result.correction_percent = drop_from_prev_close
        
        # Condition 1: DRY CORRECTION (3-12% drop from previous close)
        is_dry_correction = (3 <= drop_from_prev_close <= 12) and is_healthy_correction
        
        # Condition 2: PRICE HOLDING (Daily check)
        # No new lower low = today's low >= yesterday's low
        if len(df) >= 2:
            no_lower_low = df['low'].iloc[-1] >= df['low'].iloc[-2]
            # Range shrinking = today's range < yesterday's range
            today_range = (df['high'].iloc[-1] - df['low'].iloc[-1]) / df['close'].iloc[-1] * 100
            yesterday_range = (df['high'].iloc[-2] - df['low'].iloc[-2]) / df['close'].iloc[-2] * 100
            range_shrinking = today_range < yesterday_range
            # Price defended = lows within 1.5%
            low_diff = abs(df['low'].iloc[-1] - df['low'].iloc[-2]) / df['close'].iloc[-1] * 100
            price_defended = low_diff < 1.5
        else:
            no_lower_low = False
            range_shrinking = False
            price_defended = False
        
        is_price_holding = no_lower_low or price_defended or range_shrinking
        
        # Condition 3: EARLY BUYING PRESSURE
        # Volume increasing vs yesterday (not waiting for big spike)
        if len(df) >= 2:
            volume_increasing = df['volume'].iloc[-1] > df['volume'].iloc[-2]
        else:
            volume_increasing = False
        # Price stable or up
        price_stable_or_up = latest.get('close', 0) >= df['close'].iloc[-2] if len(df) >= 2 else False
        # Green candle
        is_green_candle = latest.get('close', 0) > latest.get('open', 0) if 'open' in df.columns else False
        # Lower wick rejection
        body_size = abs(latest.get('close', 0) - latest.get('open', 0))
        lower_wick = min(latest.get('close', 0), latest.get('open', 0)) - latest.get('low', 0)
        has_wick_rejection = lower_wick > body_size * 0.5 if body_size > 0 else False
        
        has_early_buying = volume_increasing or price_stable_or_up or is_green_candle or has_wick_rejection
        
        # Signal strength (count how many conditions are met)
        strength = sum([
            is_dry_correction,
            no_lower_low,
            price_defended,
            range_shrinking,
            volume_increasing,
            is_green_candle,
            has_wick_rejection
        ])
        result.early_entry_strength = strength
        
        # EARLY ENTRY = Bullish + Dry Correction + (Price Holding OR Early Buying)
        if result.is_bullish and is_dry_correction and (is_price_holding or has_early_buying):
            result.is_early_entry = True

        
    except Exception as e:
        logger.error(f"Error analyzing {ticker}: {str(e)}")
    
    return result


def scan_all_stocks(stock_data: Dict[str, pd.DataFrame], previous_states: dict = None) -> Dict[str, ScanResult]:
    """
    Scan all stocks and return results
    
    Args:
        stock_data: Dictionary of {ticker: DataFrame}
        previous_states: Previous states for all stocks
    
    Returns:
        Dictionary of {ticker: ScanResult}
    """
    results = {}
    previous_states = previous_states or {}
    
    for ticker, df in stock_data.items():
        prev_state = previous_states.get(ticker, {})
        result = analyze_stock(ticker, df, prev_state)
        results[ticker] = result
    
    return results


def filter_signals(results: Dict[str, ScanResult]) -> Dict[str, List[ScanResult]]:
    """
    Filter and categorize signals
    
    Returns:
        Dictionary with signal types as keys and list of results as values
    """
    signals = {
        'bullish_break': [],
        'bearish_break': [],
        'stoch_crossover': [],  # Stoch RSI Crossover signal
        'accumulation': [],
        'early_entry': []  # Serok Bawah signal
    }
    
    for ticker, result in results.items():
        # Only process signals if stock is liquid (> 5B turnover)
        if result.avg_turnover_5d < MIN_DAILY_TURNOVER:
            continue
            
        if result.bullish_break:
            signals['bullish_break'].append(result)
        if result.bearish_break:
            signals['bearish_break'].append(result)
        if result.is_stoch_crossover:
            signals['stoch_crossover'].append(result)
        if result.is_accumulation:
            signals['accumulation'].append(result)
        if result.is_early_entry:
            signals['early_entry'].append(result)
    
    return signals


def filter_all_current_signals(results: Dict[str, ScanResult]) -> Dict[str, List[ScanResult]]:
    """
    Filter stocks by their CURRENT status for morning recap.
    Unlike filter_signals which looks for transitions, this shows ALL stocks
    that are currently in a favorable state.
    
    Categories:
    - strong_buy: Score >= 7, Bullish, High volume
    - accumulation: Is accumulation signal OR (Bullish + score >= 5)
    - bullish: Currently bullish but not in above categories
    - early_entry: Early entry signal detected
    - bearish_break: Just broke bearish (warning)
    
    Returns:
        Dictionary with categories and list of results
    """
    categories = {
        'strong_buy': [],      # Best picks - high score, bullish, volume
        'accumulation': [],    # ACC signal or good setup
        'bullish': [],         # Currently bullish
        'early_entry': [],     # Serok bawah opportunities  
        'stoch_crossover': [], # Stoch RSI crossover
        'bearish_watch': []    # Just broke bearish - caution
    }
    
    for ticker, result in results.items():
        # Only process signals if stock is liquid (> 5B turnover)
        if result.avg_turnover_5d < MIN_DAILY_TURNOVER:
            continue
        
        # Strong Buy: Score >= 7, Bullish, Volume ratio > 1.5
        if result.is_bullish and result.score >= 7 and result.volume_ratio >= 1.5:
            categories['strong_buy'].append(result)
        # Accumulation: ACC signal or (Bullish + Score >= 5)
        elif result.is_accumulation:
            categories['accumulation'].append(result)
        elif result.is_bullish and result.score >= 5:
            categories['accumulation'].append(result)
        # Bullish: Currently bullish with decent score
        elif result.is_bullish and result.score >= 3:
            categories['bullish'].append(result)
        
        # Early Entry (can overlap with above)
        if result.is_early_entry:
            categories['early_entry'].append(result)
        
        # Stoch Crossover (can overlap)
        if result.is_stoch_crossover:
            categories['stoch_crossover'].append(result)
            
        # Bearish Break (warning)
        if result.bearish_break:
            categories['bearish_watch'].append(result)
    
    # Sort by score (highest first)
    for key in categories:
        categories[key] = sorted(categories[key], key=lambda x: x.score, reverse=True)
    
    return categories


def has_any_signal(signals: Dict[str, List[ScanResult]]) -> bool:
    """Check if there are any signals to send"""
    return any(len(v) > 0 for v in signals.values())
