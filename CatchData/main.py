import os
import pandas as pd
import sys
import threading
from catchVCInvestmentToken import main as catchVCInvestmentToken_main
from catchVCInvestment import main as catchVCInvestment_main
from catchProjectExchange import main as catchProjectExchange_main
from utils import get_title, update_dataframe, save_dataframe, setup_driver, display_spinner

def run_with_spinner(func, *args, **kwargs):
    stop_event = threading.Event()
    spinner_thread = threading.Thread(target=display_spinner, args=(stop_event,))
    spinner_thread.start()

    try:
        result = func(*args, **kwargs)
    finally:
        stop_event.set()
        spinner_thread.join()
        # 清除上一行的 "Loading... " 字符串
        sys.stdout.write('\r' + ' ' * 80 + '\r')
    return result

def main(url):
    # 確保 URL 沒有 /zh/
    if "com/zh/" in url:
        url = url.replace("com/zh/", "com/")
    
    # Step 1: Get title for the filename
    title = get_title(url)
    
    # Step 2: Run catchVCInvestmentToken.py
    print("\nRunning catchVCInvestmentToken...")
    run_with_spinner(catchVCInvestmentToken_main, url)
    
    # Load the CSV file
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'Data')
    progress_csv_path = os.path.join(data_dir, '[ignore]Progress.csv')
    df = pd.read_csv(progress_csv_path)
    
    # Step 3: Run catchVCInvestment.py
    print("\nRunning catchVCInvestment...")
    investment_data = run_with_spinner(catchVCInvestment_main, url)
    
    # Step 4: Run catchProjectExchange.py
    print("\nRunning catchProjectExchange...")
    exchange_data = run_with_spinner(catchProjectExchange_main, url)
    
    # Step 5: Clean and integrate data
    print("\nUpdating dataframe...")
    df, new_items, updated_items = update_dataframe(df, investment_data, exchange_data)
    
    # Step 6: Save the updated CSV file with title
    save_dataframe(df, title)
    

    # print(f"\nTotal items in CSV: {len(df)}")

if __name__ == "__main__":
    url = input("Please enter the URL: ").strip()
    main(url)