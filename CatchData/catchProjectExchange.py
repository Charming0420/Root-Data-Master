# catchProjectExchange.py

import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--lang=en-US")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
    return driver

def convert_special_string(value):
    value = value.replace('$', '').strip()
    if value.endswith('K'):
        return float(value[:-1]) * 1_000
    elif value.endswith('M'):
        return float(value[:-1]) * 1_000_000
    elif value.endswith('B'):
        return float(value[:-1]) * 1_000_000_000
    else:
        return float(value)

def parse_table_page(driver, page_number):
    items = []
    try:
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "table")))
        rows = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")
        # print(f"Found {len(rows)} rows on page {page_number}")

        for row in rows:
            try:
                tds = row.find_elements(By.TAG_NAME, "td")
                name_value = tds[0].find_element(By.CLASS_NAME, "ml-1").text.strip()
                
                try:
                    more_value = tds[8].find_element(By.CLASS_NAME, "more.d-flex.align-center.justify-center.ml-1").text.strip()
                except:
                    more_value = '0'

                # 找到 class="el-tooltip investor" 並抓取兩個 img 的 alt
                img_elements = tds[8].find_elements(By.CLASS_NAME, "el-tooltip.investor")
                exchange1 = img_elements[0].get_attribute("alt").replace("{'", "").replace("'}", "") if len(img_elements) > 0 else ""
                exchange2 = img_elements[1].get_attribute("alt").replace("{'", "").replace("'}", "") if len(img_elements) > 1 else ""

                # 計算 Binance、OKX、Coinbase 和 Bybit 的次數
                binance_count = 1 if exchange1.lower() == 'binance' or exchange2.lower() == 'binance' else 0
                okx_count = 1 if exchange1.lower() == 'okx' or exchange2.lower() == 'okx' else 0
                coinbase_count = 1 if exchange1.lower() == 'coinbase' or exchange2.lower() == 'coinbase' else 0
                bybit_count = 1 if exchange1.lower() == 'bybit' or exchange2.lower() == 'bybit' else 0

                # 抓取 price, mc, fdv 資料
                try:
                    price = convert_special_string(tds[1].text.strip())
                except:
                    price = 0
                
                try:
                    mc = convert_special_string(tds[4].text.strip())
                except:
                    mc = 0

                try:
                    fdv = convert_special_string(tds[6].text.strip())
                except:
                    fdv = 0

                items.append({
                    'name_value': name_value,
                    'more_value': more_value,
                    'exchange1': exchange1,
                    'exchange2': exchange2,
                    'Binance': binance_count,
                    'OKX': okx_count,
                    'Coinbase': coinbase_count,
                    'Bybit': bybit_count,
                    'Price': price,
                    'MC': mc,
                    'FDV': fdv
                })
            except Exception as e:
               e
               # print(f"Error parsing row on page {page_number}: {e}")
        # print(f"Successfully parsed {len(items)} items on page {page_number}")
    except Exception as e:
        print(f"Error parsing table on page {page_number}: {e}")

    return items

def click_next_page(driver, is_investor):
    try:
        if is_investor:
            next_button_js = """
            document.querySelector("#app > div > main > div > div > div.row.detail.common_detail.justify-start.justify-md-center > div.detail_l.col-sm-12.col-md-8.col-lg-9.col-xl-9.col-12 > div.v-window.v-item-group.theme--light.v-tabs-items > div > div > div.investment > div.tokens-list > div.pagination-container.d-flex.justify-center > div > button.btn-next").click();
            """
        else:
            next_button_js = """
            document.querySelector("#app > div > main > div > div > div.row.detail.common_detail.justify-start.justify-md-center > div.detail_l.col-sm-12.col-md-8.col-lg-9.col-xl-9.col-12 > div.v-window.detail_tab_items.v-item-group.theme--light.v-tabs-items > div > div > div.investment > div.tokens-list > div.pagination-container.d-flex.justify-center > div > button.btn-next").click();
            """
        driver.execute_script(next_button_js)
        # print("Next button clicked successfully.")
        return True
    except Exception as e:
        print(f"Failed to click next button: {e}")
        return False

def main(url):
    is_investor = "Investors/detail" in url
    driver = setup_driver()
    driver.get(url)

    time.sleep(3)

    current_url = driver.current_url
    if "zh" in current_url:
        driver.get(url)
        # print("Redirected to the correct URL.")
        time.sleep(3)

    try:
        if is_investor:
            initial_button_js = """
            document.querySelector("#app > div > main > div > div > div.row.detail.common_detail.justify-start.justify-md-center > div.detail_l.col-sm-12.col-md-8.col-lg-9.col-xl-9.col-12 > div.v-window.v-item-group.theme--light.v-tabs-items > div > div > div.investment > div.d-flex.flex-row.align-center.justify-space-between > div.d-flex.flex-column.flex-md-row.align-end.align-md-center > div > button:nth-child(3)").click();
            """
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#app > div > main > div > div > div.row.detail.common_detail.justify-start.justify-md-center > div.detail_l.col-sm-12.col-md-8.col-lg-9.col-xl-9.col-12 > div.v-window.v-item-group.theme--light.v-tabs-items > div > div > div.investment > div.d-flex.flex-row.align-center.justify-space-between > div.d-flex.flex-column.flex-md-row.align-end.align-md-center > div > button:nth-child(3)")))
        else:
            initial_button_js = """
            document.querySelector("#app > div > main > div > div > div.row.detail.common_detail.justify-start.justify-md-center > div.detail_l.col-sm-12.col-md-8.col-lg-9.col-xl-9.col-12 > div.v-window.detail_tab_items.v-item-group.theme--light.v-tabs-items > div > div > div.investment > div.d-flex.flex-row.align-center.justify-space-between > div.d-flex.flex-column.flex-md-row.align-end.align-md-center > div > button:nth-child(3)").click();
            """
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#app > div > main > div > div > div.row.detail.common_detail.justify-start.justify-md-center > div.detail_l.col-sm-12.col-md-8.col-lg-9.col-xl-9.col-12 > div.v-window.detail_tab_items.v-item-group.theme--light.v-tabs-items > div > div > div.investment > div.d-flex.flex-row.align-center.justify-space-between > div.d-flex.flex-column.flex-md-row.align-end.align-md-center > div > button:nth-child(2)")))
        driver.execute_script(initial_button_js)
        # print("Initial button clicked successfully.")
        time.sleep(2)
    except Exception as e:
        print(f"Failed to click initial button: {e}")
        driver.quit()
        return

    all_items = []
    page_number = 1

    while True:
        try:
            # print(f"Parsing page {page_number}")
            items = parse_table_page(driver, page_number)
            if not items:
                # print("No items found on this page, stopping.")
                break
            all_items.extend(items)

            if len(items) < 20:
                # print(f"Stopping as the row count is {len(items)}.")
                break

            prev_rows = len(driver.find_elements(By.CSS_SELECTOR, "table tbody tr"))
            if not click_next_page(driver, is_investor):
                break
            time.sleep(1)  # 增加等待時間，確保頁面完全加載
           
            # print(f"Successfully navigated to page {page_number + 1}")
            page_number += 1
        except Exception as e:
            print(f"An error occurred while parsing page {page_number}: {e}")
            break

    driver.quit()

    return all_items

if __name__ == "__main__":
    url = input

    # for item in items:
    #     print(f"Name: {item['name_value']}")
    #     print(f"More Value: {item['more_value']}")
    #     print(f"Exchange 1: {item['exchange1']}")
    #     print(f"Exchange 2: {item['exchange2']}")
    #     print(f"Binance: {item['Binance']}")
    #     print(f"OKX: {item['OKX']}")
    #     print(f"Coinbase: {item['Coinbase']}")
    #     print(f"Bybit: {item['Bybit']}")
    #     print(f"Price: {item['Price']}")
    #     print(f"MC: {item['MC']}")
    #     print(f"FDV: {item['FDV']}")
    #     print("-" * 20)