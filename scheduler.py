# ============================================
# SCHEDULER - RUN SCAN EVERY 5 MINUTES
# ============================================

import schedule
import time
import logging
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import run_scan, is_trading_hours, send_end_of_day_recap, is_end_of_trading
from database.state_manager import StateManager
from notifications.telegram_bot import send_startup_message, send_telegram_message

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('logs/scheduler.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

# Global state manager
state_manager = None


def scheduled_scan():
    """Run scheduled scan"""
    global state_manager
    
    if not is_trading_hours():
        logger.info("Outside trading hours. Waiting...")
        return
    
    try:
        # Check if it's end of trading (16:00) - send recap instead
        if is_end_of_trading():
            logger.info("End of trading session. Sending daily recap...")
            send_end_of_day_recap(state_manager)
        else:
            run_scan(state_manager, force=False)
    except Exception as e:
        logger.error(f"Error during scheduled scan: {str(e)}")
        send_telegram_message(f"⚠️ Scanner Error: {str(e)}")


def main():
    """Main scheduler loop"""
    global state_manager
    
    # Ensure directories exist
    os.makedirs('logs', exist_ok=True)
    os.makedirs('database', exist_ok=True)
    
    logger.info("="*50)
    logger.info("IHSG SUPERTREND SCANNER - SCHEDULER")
    logger.info("="*50)
    logger.info("Scan interval: 5 minutes")
    logger.info("Trading hours: 09:00 - 16:00 WIB")
    logger.info("="*50)
    
    # Initialize state manager
    state_manager = StateManager()
    
    # Send startup notification
    send_startup_message()
    
    # Run initial scan
    logger.info("Running initial scan...")
    run_scan(state_manager, force=True)
    
    # Schedule scans every 5 minutes
    # Run at :00, :05, :10, :15, :20, :25, :30, :35, :40, :45, :50, :55
    for minute in range(0, 60, 5):
        schedule.every().hour.at(f":{minute:02d}").do(scheduled_scan)
    
    logger.info("Scheduler started. Waiting for next scan...")
    
    # Main loop
    while True:
        try:
            schedule.run_pending()
            time.sleep(30)  # Check every 30 seconds
        except KeyboardInterrupt:
            logger.info("Scheduler stopped by user")
            send_telegram_message("🛑 IHSG Scanner stopped")
            break
        except Exception as e:
            logger.error(f"Scheduler error: {str(e)}")
            time.sleep(60)  # Wait 1 minute before retrying


if __name__ == "__main__":
    main()
