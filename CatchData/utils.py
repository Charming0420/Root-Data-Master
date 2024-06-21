# utils.py

import time
import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from tqdm import tqdm

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--lang=en-US")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
    return driver

def get_title(url):
    driver = setup_driver()
    driver.get(url)
    time.sleep(3)

    try:
        title_element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#app > div > main > div > div > div.row.detail.common_detail.justify-start.justify-md-center > div.detail_l.col-sm-12.col-md-8.col-lg-9.col-xl-9.col-12 > div.base_info > div:nth-child(1) > div.detail_info_head.d-flex.flex-row.justify-space-between.align-center.mt-md-11.mt-lg-11.mt-xl-11 > div.d-flex.flex-row.align-center > div > div > h1"))
        )
        title = title_element.text.strip()
    except Exception as e:
        print(f"Error fetching title: {e}")
        title = "output"
    driver.quit()
    return title

def update_dataframe(df, investment_data, exchange_data):
    df['Name'] = df['Name'].fillna(df['Token'])

    existing_names = df['Name'].str.lower().tolist()
    new_items = 0
    updated_items = 0

    for item in tqdm(investment_data, desc="Integrating investment data"):
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
                'Description': item['description']
            }
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            new_items += 1
        else:
            index = df[df['Name'].str.lower() == item_name.lower()].index[0]
            df.at[index, 'Description'] = item['description']
            updated_items += 1

    df.drop_duplicates(subset='Name', keep='first', inplace=True)

    if 'Price' not in df.columns:
        df.insert(7, 'Price', 0)
    if 'MC' not in df.columns:
        df.insert(8, 'MC', 0)
    if 'FDV' not in df.columns:
        df.insert(9, 'FDV', 0)
    if 'Exchange Amount' not in df.columns:
        df.insert(10, 'Exchange Amount', 0)
    if 'Binance' not in df.columns:
        df.insert(11, 'Binance', 0)
    if 'OKX' not in df.columns:
        df.insert(12, 'OKX', 0)
    if 'Coinbase' not in df.columns:
        df.insert(13, 'Coinbase', 0)
    if 'Bybit' not in df.columns:
        df.insert(14, 'Bybit', 0)

    for exchange_item in tqdm(exchange_data, desc="Integrating exchange data"):
        token_name = exchange_item['name_value']
        if token_name in df['Token'].values:
            index = df[df['Token'] == token_name].index[0]
            try:
                exchange_amount = int(exchange_item['more_value'].replace(',', '').replace('+', '').strip())
            except ValueError:
                exchange_amount = 0
            df.at[index, 'Exchange Amount'] = exchange_amount
            df.at[index, 'Binance'] = exchange_item['Binance']
            df.at[index, 'OKX'] = exchange_item['OKX']
            df.at[index, 'Coinbase'] = exchange_item['Coinbase']
            df.at[index, 'Bybit'] = exchange_item['Bybit']
            df.at[index, 'Price'] = exchange_item['Price']
            df.at[index, 'MC'] = exchange_item['MC']
            df.at[index, 'FDV'] = exchange_item['FDV']

    return df, new_items, updated_items

def save_dataframe(df, title):
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'Data')
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    output_file_path = os.path.join(data_dir, f'{title}_{timestamp}.csv')
    df.to_csv(output_file_path, index=False)
    print(f"⎷ CSV file '{title}_{timestamp}.csv' created successfully.")
    return output_file_path