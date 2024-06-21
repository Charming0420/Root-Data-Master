import os
import pandas as pd
from catchVCInvestmentToken import main as catchVCInvestmentToken_main
from catchVCInvestment import main as catchVCInvestment_main
from catchProjectExchange import main as catchProjectExchange_main
from utils import get_title, update_dataframe, save_dataframe

def main(url):
    # 確保 URL 沒有 /zh/
    if "com/zh/" in url:
        url = url.replace("com/zh/", "com/")
    
    # Step 1: Get title for the filename
    title = get_title(url)
    
    # Step 2: Run catchVCInvestmentToken.py
    catchVCInvestmentToken_main(url)
    
    # Load the CSV file
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'Data')
    progress_csv_path = os.path.join(data_dir, '[ignore]Progress.csv')
    df = pd.read_csv(progress_csv_path)
    
    # Step 3: Run catchVCInvestment.py
    investment_data = catchVCInvestment_main(url)
    
    # Step 4: Run catchProjectExchange.py
    exchange_data = catchProjectExchange_main(url)
    
    # Step 5: Clean and integrate data
    df, new_items, updated_items = update_dataframe(df, investment_data, exchange_data)
    
    # Step 6: Save the updated CSV file with title
    save_dataframe(df, title)

    print(f"Total items in CSV: {len(df)}")
    # print(f"New items added: {new_items}")
    # print(f"Updated items with description: {updated_items}")

if __name__ == "__main__":
    url = input("Please enter the URL: ").strip()
    main(url)