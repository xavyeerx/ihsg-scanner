# ============================================
# TELEGRAM BOT - SEND ALERTS
# ============================================

import requests
from typing import List
import logging
from datetime import datetime
import pytz

import sys
sys.path.append('..')
from config.settings import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

logger = logging.getLogger(__name__)

# Timezone
WIB = pytz.timezone('Asia/Jakarta')


def get_current_time_wib() -> str:
    """Get current time in WIB format"""
    now = datetime.now(WIB)
    return now.strftime("%d %b %Y, %H:%M WIB")


def send_telegram_message(message: str) -> bool:
    """
    Send message via Telegram Bot API
    
    Args:
        message: Message text (supports HTML formatting)
    
    Returns:
        True if successful, False otherwise
    """
    if TELEGRAM_BOT_TOKEN == "YOUR_BOT_TOKEN_HERE" or TELEGRAM_CHAT_ID == "YOUR_CHAT_ID_HERE":
        logger.warning("Telegram not configured. Message would be:")
        print("\n" + "="*50)
        print(message)
        print("="*50 + "\n")
        return True
    
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            'chat_id': TELEGRAM_CHAT_ID,
            'text': message,
            'parse_mode': 'HTML',
            'disable_web_page_preview': True
        }
        
        response = requests.post(url, json=payload, timeout=10)
        
        if response.status_code == 200:
            logger.info("Telegram message sent successfully")
            return True
        else:
            logger.error(f"Telegram error: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        logger.error(f"Error sending Telegram message: {str(e)}")
        return False


def format_bullish_break_message(results: List) -> str:
    """Format bullish break alert message"""
    if not results:
        return ""
    
    lines = [
        "━━━━━━━━━━━━━━━━━━━━━━━━━━",
        "🟢 <b>SUPERTREND BULLISH BREAK</b>",
        "━━━━━━━━━━━━━━━━━━━━━━━━━━",
        f"⏰ {get_current_time_wib()}",
        ""
    ]
    
    for r in results:
        ticker_clean = r.ticker.replace('.JK', '')
        change_str = f"+{r.change_percent:.1f}%" if r.change_percent >= 0 else f"{r.change_percent:.1f}%"
        lines.append(f"📈 <b>{ticker_clean}</b> | {r.price:,.0f} ({change_str})")
        lines.append(f"   └─ ST: {r.supertrend_value:,.0f} | Score: {r.score}")
    
    lines.append("")
    lines.append(f"━━━━━━━━━━━━━━━━━━━━━━━━━━")
    lines.append(f"Total: {len(results)} saham break bullish")
    
    return "\n".join(lines)


def format_bearish_break_message(results: List) -> str:
    """Format bearish break alert message"""
    if not results:
        return ""
    
    lines = [
        "━━━━━━━━━━━━━━━━━━━━━━━━━━",
        "🔴 <b>SUPERTREND BEARISH BREAK</b>",
        "━━━━━━━━━━━━━━━━━━━━━━━━━━",
        f"⏰ {get_current_time_wib()}",
        ""
    ]
    
    for r in results:
        ticker_clean = r.ticker.replace('.JK', '')
        change_str = f"{r.change_percent:.1f}%"
        lines.append(f"📉 <b>{ticker_clean}</b> | {r.price:,.0f} ({change_str})")
        lines.append(f"   └─ ST: {r.supertrend_value:,.0f} | Score: {r.score}")
    
    lines.append("")
    lines.append(f"━━━━━━━━━━━━━━━━━━━━━━━━━━")
    lines.append(f"Total: {len(results)} saham break bearish")
    
    return "\n".join(lines)


def format_stoch_crossover_message(results: List) -> str:
    """Format Stoch RSI Crossover alert message"""
    if not results:
        return ""
    
    lines = [
        "━━━━━━━━━━━━━━━━━━━━━━━━━━",
        "📈 <b>STOCH RSI CROSSOVER</b>",
        "━━━━━━━━━━━━━━━━━━━━━━━━━━",
        f"⏰ {get_current_time_wib()}",
        ""
    ]
    
    # Sort by stoch_k (lowest first = coming from oversold)
    sorted_results = sorted(results, key=lambda x: x.stoch_k)
    
    for r in sorted_results:
        ticker_clean = r.ticker.replace('.JK', '')
        change_str = f"+{r.change_percent:.1f}%" if r.change_percent >= 0 else f"{r.change_percent:.1f}%"
        lines.append(f"📊 <b>{ticker_clean}</b> | {r.price:,.0f} ({change_str})")
        lines.append(f"   └─ Stoch K: {r.stoch_k:.0f} ↗ D: {r.stoch_d:.0f}")
    
    lines.append("")
    lines.append(f"━━━━━━━━━━━━━━━━━━━━━━━━━━")
    lines.append("💡 <i>K crossed above D = bullish momentum!</i>")
    lines.append(f"Total: {len(results)} saham stoch crossover")
    
    return "\n".join(lines)


def format_accumulation_message(results: List) -> str:
    """Format accumulation signal message"""
    if not results:
        return ""
    
    lines = [
        "━━━━━━━━━━━━━━━━━━━━━━━━━━",
        "🔵 <b>ACCUMULATION SIGNAL</b>",
        "━━━━━━━━━━━━━━━━━━━━━━━━━━",
        f"⏰ {get_current_time_wib()}",
        ""
    ]
    
    for r in results:
        ticker_clean = r.ticker.replace('.JK', '')
        change_str = f"+{r.change_percent:.1f}%" if r.change_percent >= 0 else f"{r.change_percent:.1f}%"
        lines.append(f"📊 <b>{ticker_clean}</b> | {r.price:,.0f} ({change_str})")
        lines.append(f"   └─ Score: {r.score} | Vol: {r.volume_ratio:.1f}x | Stoch: {r.stoch_k:.0f}")
    
    lines.append("")
    lines.append(f"━━━━━━━━━━━━━━━━━━━━━━━━━━")
    lines.append(f"Total: {len(results)} saham accumulation")
    
    return "\n".join(lines)



def send_all_alerts(signals: dict) -> int:
    """
    Send all alert messages
    
    Args:
        signals: Dictionary of signal types and their results
    
    Returns:
        Number of messages sent
    """
    messages_sent = 0
    
    # Bullish break
    if signals.get('bullish_break'):
        msg = format_bullish_break_message(signals['bullish_break'])
        if send_telegram_message(msg):
            messages_sent += 1
    
    # Bearish break
    if signals.get('bearish_break'):
        msg = format_bearish_break_message(signals['bearish_break'])
        if send_telegram_message(msg):
            messages_sent += 1
    
    # Stoch RSI Crossover
    if signals.get('stoch_crossover'):
        msg = format_stoch_crossover_message(signals['stoch_crossover'])
        if send_telegram_message(msg):
            messages_sent += 1
    
    # Accumulation
    if signals.get('accumulation'):
        msg = format_accumulation_message(signals['accumulation'])
        if send_telegram_message(msg):
            messages_sent += 1
    
    # Early Entry (Serok Bawah)
    if signals.get('early_entry'):
        msg = format_early_entry_message(signals['early_entry'])
        if send_telegram_message(msg):
            messages_sent += 1
    
    return messages_sent


def format_early_entry_message(results: List) -> str:
    """
    Format Early Entry (Serok Bawah) message
    
    Signal detects:
    - Dry correction (4-12% drop with low volume)
    - Price holding (no lower low, range shrinking)
    - Early buying (volume increasing, price stable)
    """
    if not results:
        return ""
    
    lines = [
        "━━━━━━━━━━━━━━━━━━━━━━━━━━",
        "🎯 <b>EARLY ENTRY (SEROK BAWAH)</b>",
        "━━━━━━━━━━━━━━━━━━━━━━━━━━",
        f"⏰ {get_current_time_wib()}",
        ""
    ]
    
    # Sort by strength (highest first)
    sorted_results = sorted(results, key=lambda x: x.early_entry_strength, reverse=True)
    
    for r in sorted_results:
        ticker_clean = r.ticker.replace('.JK', '')
        change_str = f"+{r.change_percent:.1f}%" if r.change_percent >= 0 else f"{r.change_percent:.1f}%"
        
        # Strength indicator
        strength = r.early_entry_strength
        emoji = "🔥" if strength >= 5 else "💎" if strength >= 3 else "📍"
        
        lines.append(f"{emoji} <b>{ticker_clean}</b> | {r.price:,.0f} ({change_str})")
        lines.append(f"   └─ Koreksi: {r.correction_percent:.1f}% | Strength: {strength}/7")
    
    lines.append("")
    lines.append(f"━━━━━━━━━━━━━━━━━━━━━━━━━━")
    lines.append("⚠️ <i>Sinyal dini - DYOR!</i>")
    lines.append(f"Total: {len(results)} saham early entry")
    
    return "\n".join(lines)


def send_startup_message():
    """Send startup notification"""
    msg = f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━
🤖 <b>IHSG SCANNER STARTED</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━
⏰ {get_current_time_wib()}

Scanner is now running.
Alerts will be sent every 5 minutes.
━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    send_telegram_message(msg.strip())


def send_scan_complete_message(total_stocks: int, signals_count: dict):
    """Send scan completion summary (optional)"""
    total_signals = sum(len(v) for v in signals_count.values())
    
    if total_signals == 0:
        return  # Don't send if no signals
    
    msg = f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 <b>SCAN COMPLETE</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━
⏰ {get_current_time_wib()}

Scanned: {total_stocks} stocks
Signals found: {total_signals}
━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    # Uncomment below if you want scan complete notifications
    # send_telegram_message(msg.strip())


def send_daily_recap_message(daily_summary: dict):
    """
    Send end-of-day recap message with ALL stocks that triggered signals today.
    
    Args:
        daily_summary: Dictionary with signal types and their stocks
            {'date': '2026-01-26', 'bullish_break': ['BBCA.JK', ...], ...}
    """
    lines = [
        "━━━━━━━━━━━━━━━━━━━━━━━━━━",
        "📋 <b>REKAP HARIAN - END OF DAY</b>",
        "━━━━━━━━━━━━━━━━━━━━━━━━━━",
        f"📅 {daily_summary.get('date', 'N/A')}",
        f"⏰ {get_current_time_wib()}",
        ""
    ]
    
    total_signals = 0
    
    # Bullish Break
    bullish = daily_summary.get('bullish_break', [])
    if bullish:
        lines.append(f"🟢 <b>BULLISH BREAK</b> ({len(bullish)} saham)")
        tickers = [t.replace('.JK', '') for t in bullish]
        lines.append(f"   {', '.join(tickers)}")
        lines.append("")
        total_signals += len(bullish)
    
    # Bearish Break
    bearish = daily_summary.get('bearish_break', [])
    if bearish:
        lines.append(f"🔴 <b>BEARISH BREAK</b> ({len(bearish)} saham)")
        tickers = [t.replace('.JK', '') for t in bearish]
        lines.append(f"   {', '.join(tickers)}")
        lines.append("")
        total_signals += len(bearish)
    
    # Stoch Crossover
    stoch = daily_summary.get('stoch_crossover', [])
    if stoch:
        lines.append(f"📈 <b>STOCH CROSSOVER</b> ({len(stoch)} saham)")
        tickers = [t.replace('.JK', '') for t in stoch]
        lines.append(f"   {', '.join(tickers)}")
        lines.append("")
        total_signals += len(stoch)
    
    # Accumulation
    acc = daily_summary.get('accumulation', [])
    if acc:
        lines.append(f"🔵 <b>ACCUMULATION</b> ({len(acc)} saham)")
        tickers = [t.replace('.JK', '') for t in acc]
        lines.append(f"   {', '.join(tickers)}")
        lines.append("")
        total_signals += len(acc)
    
    # Early Entry
    early = daily_summary.get('early_entry', [])
    if early:
        lines.append(f"🎯 <b>EARLY ENTRY</b> ({len(early)} saham)")
        tickers = [t.replace('.JK', '') for t in early]
        lines.append(f"   {', '.join(tickers)}")
        lines.append("")
        total_signals += len(early)
    
    # Footer
    lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━")
    lines.append(f"📊 Total: {total_signals} sinyal hari ini")
    lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━")
    
    message = "\n".join(lines)
    send_telegram_message(message)


def send_morning_recap_message(signals: dict):
    """
    Send morning recap message at 08:00 with ALL stocks matching screener criteria.
    
    Args:
        signals: Dictionary with categories and list of ScanResult objects
            {'strong_buy': [...], 'accumulation': [...], 'bullish': [...], 'early_entry': [...], 'stoch_crossover': [...], 'bearish_watch': [...]}
    """
    lines = [
        "━━━━━━━━━━━━━━━━━━━━━━━━━━",
        "☀️ <b>MORNING SCAN - 08:00</b>",
        "━━━━━━━━━━━━━━━━━━━━━━━━━━",
        f"⏰ {get_current_time_wib()}",
        ""
    ]
    
    total_signals = 0
    
    # Strong Buy (highest priority)
    strong_buy = signals.get('strong_buy', [])
    if strong_buy:
        lines.append(f"🔥 <b>STRONG BUY</b> ({len(strong_buy)} saham)")
        for r in strong_buy[:10]:  # Limit to 10
            ticker_clean = r.ticker.replace('.JK', '')
            lines.append(f"   • {ticker_clean} | {r.price:,.0f} | Score: {r.score}")
        if len(strong_buy) > 10:
            lines.append(f"   ... dan {len(strong_buy) - 10} lainnya")
        lines.append("")
        total_signals += len(strong_buy)
    
    # Accumulation
    acc = signals.get('accumulation', [])
    if acc:
        lines.append(f"🔵 <b>ACCUMULATION</b> ({len(acc)} saham)")
        for r in acc[:10]:
            ticker_clean = r.ticker.replace('.JK', '')
            lines.append(f"   • {ticker_clean} | {r.price:,.0f} | Score: {r.score}")
        if len(acc) > 10:
            lines.append(f"   ... dan {len(acc) - 10} lainnya")
        lines.append("")
        total_signals += len(acc)
    
    # Bullish
    bullish = signals.get('bullish', [])
    if bullish:
        lines.append(f"🟢 <b>BULLISH</b> ({len(bullish)} saham)")
        tickers = [r.ticker.replace('.JK', '') for r in bullish[:15]]
        lines.append(f"   {', '.join(tickers)}")
        if len(bullish) > 15:
            lines.append(f"   ... dan {len(bullish) - 15} lainnya")
        lines.append("")
        total_signals += len(bullish)
    
    # Early Entry (Serok Bawah)
    early = signals.get('early_entry', [])
    if early:
        lines.append(f"🎯 <b>EARLY ENTRY</b> ({len(early)} saham)")
        for r in early[:8]:
            ticker_clean = r.ticker.replace('.JK', '')
            lines.append(f"   • {ticker_clean} | {r.price:,.0f} | Koreksi: {r.correction_percent:.1f}%")
        if len(early) > 8:
            lines.append(f"   ... dan {len(early) - 8} lainnya")
        lines.append("")
        total_signals += len(early)
    
    # Stoch Crossover
    stoch = signals.get('stoch_crossover', [])
    if stoch:
        lines.append(f"📈 <b>STOCH CROSSOVER</b> ({len(stoch)} saham)")
        tickers = [r.ticker.replace('.JK', '') for r in stoch[:15]]
        lines.append(f"   {', '.join(tickers)}")
        if len(stoch) > 15:
            lines.append(f"   ... dan {len(stoch) - 15} lainnya")
        lines.append("")
        total_signals += len(stoch)
    
    # Bearish Watch (warning)
    bearish = signals.get('bearish_watch', [])
    if bearish:
        lines.append(f"⚠️ <b>BEARISH WATCH</b> ({len(bearish)} saham)")
        tickers = [r.ticker.replace('.JK', '') for r in bearish[:10]]
        lines.append(f"   {', '.join(tickers)}")
        lines.append("")
        total_signals += len(bearish)
    
    # Footer
    lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━")
    lines.append(f"📊 Total: {total_signals} saham dalam radar")
    lines.append("💡 <i>Scan lengkap sebelum market buka</i>")
    lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━")
    
    message = "\n".join(lines)
    send_telegram_message(message)
