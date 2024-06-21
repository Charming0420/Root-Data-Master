import os
import pandas as pd
import time
from catchVCInvestmentToken import main as catchVCInvestmentToken_main
from catchVCInvestment import main as catchVCInvestment_main
from catchProjectExchange import main as catchProjectExchange_main

def main(url):
    # Step 1: Run catchVCInvestmentToken.py
    catchVCInvestmentToken_main(url)
    
    # Load the CSV file
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'Data')
    progress_csv_path = os.path.join(data_dir, '[ignore]Progress.csv')
    df = pd.read_csv(progress_csv_path)
    
    # Step 2: Run catchVCInvestment.py
    investment_data = catchVCInvestment_main(url)
    
    # Step 3: Clean and integrate data
    # Remove rows where Name is missing
    df['Name'] = df['Name'].fillna(df['Token'])

    # Add new rows from investment_data to df
    existing_names = df['Name'].str.lower().tolist()
    new_items = 0
    updated_items = 0
    for item in investment_data:
        item_name = item['name'].replace('*', '')
        if item_name.lower() not in existing_names:
            new_row = {
                'Token': '',
                'Name': item_name,
                'Sector': '',
                'Date': '',
                'Round': '',
                'Total Funding': '',
                'Valuation': '',
                'Price': '',
                'MC': '',
                'FDV': '',
                'Exchange': '',
                'Description': item['description']
            }
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            new_items += 1
        else:
            index = df[df['Name'].str.lower() == item_name.lower()].index[0]
            df.at[index, 'Description'] = item['description']
            updated_items += 1

    # Remove duplicate rows based on the 'Name' column
    df.drop_duplicates(subset='Name', keep='first', inplace=True)

    # Step 4: Run catchProjectExchange.py and integrate the data
    exchange_data = catchProjectExchange_main(url)
    
    # Add new columns for exchange data
    df.insert(10, 'Exchange Amount', 0)
    df.insert(11, 'Binance', 0)
    df.insert(12, 'OKX', 0)
    df.insert(13, 'Coinbase', 0)
    df.insert(14, 'Bybit', 0)
    
    for exchange_item in exchange_data:
        token_name = exchange_item['name_value']
        if token_name in df['Token'].values:
            index = df[df['Token'] == token_name].index[0]
            # Convert more_value to integer safely
            try:
                exchange_amount = int(exchange_item['more_value'].replace(',', '').replace('+', '').strip())
            except ValueError:
                exchange_amount = 0
            df.at[index, 'Exchange Amount'] = exchange_amount
            df.at[index, 'Binance'] = exchange_item['Binance']
            df.at[index, 'OKX'] = exchange_item['OKX']
            df.at[index, 'Coinbase'] = exchange_item['Coinbase']
            df.at[index, 'Bybit'] = exchange_item['Bybit']

    # Save the updated CSV file
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    output_file_path = os.path.join(data_dir, f'projects_{timestamp}.csv')
    df.to_csv(output_file_path, index=False)
    print(f"CSV file '{output_file_path}' created successfully.")

    print(f"Total items in CSV: {len(df)}")
    print(f"New items added: {new_items}")
    print(f"Updated items with description: {updated_items}")

if __name__ == "__main__":
    url = input("Please enter the URL: ").strip()
    if "com/zh/" in url:
        url = url.replace("com/zh/", "com/")
    main(url)