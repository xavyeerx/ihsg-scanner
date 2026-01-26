# ============================================
# SCORING SYSTEM
# ============================================
# Matches Pine Script v3 scoring logic exactly

import pandas as pd
import numpy as np
from typing import Tuple

import sys
sys.path.append('..')
from config.settings import *


def calculate_trend_score(df: pd.DataFrame) -> float:
    """Calculate trend score (max 25 points)"""
    if len(df) == 0:
        return 0.0
    
    row = df.iloc[-1]
    score = 0.0
    
    # Bullish trend: +10
    if row.get('direction', -1) == 1:
        score += 10.0
    
    # EMA alignment bullish: +10
    if row.get('ema_bullish_alignment', False):
        score += 10.0
    
    # Trend aligned (simplified - always true if bullish): +5
    if row.get('direction', -1) == 1:
        score += 5.0
    
    return min(score, 25.0)


def calculate_regime_score(df: pd.DataFrame) -> float:
    """Calculate market regime score (max 15 points)"""
    if len(df) == 0:
        return 0.0
    
    row = df.iloc[-1]
    score = 0.0
    
    # Trending market: +10
    if row.get('is_trending', False):
        score += 10.0
    
    # Volatile enough: +5
    if row.get('is_volatile_enough', False):
        score += 5.0
    
    return min(score, 15.0)


def calculate_volume_score(df: pd.DataFrame) -> float:
    """Calculate volume score (max 20 points)"""
    if len(df) == 0:
        return 0.0
    
    row = df.iloc[-1]
    score = 0.0
    
    # High volume: +5 (simplified - if volume > avg)
    if row.get('volume_ratio', 0) > 1.0:
        score += 5.0
    
    # Volume spike: +7
    if row.get('is_volume_spike', False):
        score += 7.0
    
    # Unusual volume: +8
    if row.get('is_unusual_volume', False):
        score += 8.0
    
    # Volume bias bullish + bullish trend: +5
    if row.get('volume_bias_bullish', False) and row.get('direction', -1) == 1:
        score += 5.0
    
    return min(score, 20.0)


def calculate_momentum_score(df: pd.DataFrame) -> float:
    """Calculate momentum score (max 22 points)"""
    if len(df) == 0:
        return 0.0
    
    row = df.iloc[-1]
    score = 0.0
    
    # Positive momentum: +10
    if row.get('is_positive_momentum', False):
        score += 10.0
    
    # Strong momentum + positive: +7
    if row.get('is_strong_momentum', False) and row.get('is_positive_momentum', False):
        score += 7.0
    
    # Stoch conditions
    if row.get('stoch_neutral', False):
        score += 5.0
    elif row.get('stoch_oversold', False) and row.get('direction', -1) == 1:
        score += 10.0
    
    return min(score, 22.0)


def calculate_position_score(df: pd.DataFrame) -> float:
    """Calculate position score (max 18 points)"""
    if len(df) == 0:
        return 0.0
    
    row = df.iloc[-1]
    score = 0.0
    
    # Price above EMA200: +8
    if row.get('price_above_ema200', False):
        score += 8.0
    
    # Price above EMA50: +6
    if row.get('price_above_ema50', False):
        score += 6.0
    
    # Price above EMA20: +4
    if row.get('price_above_ema20', False):
        score += 4.0
    
    return min(score, 18.0)


def calculate_total_score(df: pd.DataFrame) -> Tuple[int, str, str]:
    """
    Calculate total score and determine status
    
    Returns:
        Tuple of (score, status, status_emoji)
    """
    if len(df) == 0:
        return 0, "AVOID", "🔴"
    
    trend = calculate_trend_score(df)
    regime = calculate_regime_score(df)
    volume = calculate_volume_score(df)
    momentum = calculate_momentum_score(df)
    position = calculate_position_score(df)
    
    total = trend + regime + volume + momentum + position
    
    # Apply sideways penalty
    row = df.iloc[-1]
    if row.get('is_sideways', True) and not row.get('is_unusual_volume', False):
        total = total * 0.7
    
    final_score = int(round(total))
    is_trending = row.get('is_trending', False)
    
    # Determine status
    if final_score >= BUY_THRESHOLD and is_trending:
        return final_score, "STRONG BUY", "🟢"
    elif final_score >= ACCUMULATE_THRESHOLD:
        return final_score, "ACCUMULATE", "🔵"
    elif final_score >= HOLD_THRESHOLD:
        return final_score, "HOLD", "🟡"
    else:
        return final_score, "AVOID", "🔴"


def get_score_breakdown(df: pd.DataFrame) -> dict:
    """Get detailed score breakdown"""
    return {
        'trend': calculate_trend_score(df),
        'regime': calculate_regime_score(df),
        'volume': calculate_volume_score(df),
        'momentum': calculate_momentum_score(df),
        'position': calculate_position_score(df)
    }
