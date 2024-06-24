import os
import time
import re
import pandas as pd
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

def convert_to_number(value):
    if not value or not re.search(r'\$\s*\d', value):
        return value
    
    value = value.replace('$', '').strip()
    
    if 'K' in value:
        return int(float(value.replace('K', '')) * 1_000)
    elif 'M' in value:
        return int(float(value.replace('M', '')) * 1_000_000)
    elif 'B' in value:
        return int(float(value.replace('B', '')) * 1_000_000_000)
    else:
        return int(value)

def parse_table_page(driver, page_number):
    items = []
    try:
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "table")))
        rows = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")
        # print(f"Found {len(rows)} rows on page {page_number}")

        for row in rows:
            try:
                tds = row.find_elements(By.TAG_NAME, "td")
                project_name_element = tds[0].find_element(By.CSS_SELECTOR, ".el-tooltip.list_name.animation_underline")
                project_name_full = project_name_element.text.strip()
                token_name_element = tds[0].find_elements(By.CSS_SELECTOR, ".symbol.ml-1.d-none.d-md-inline")
                token_name = token_name_element[0].text.strip() if token_name_element else ""

                project_name_full_cleaned = project_name_full.replace("*", "").strip()

                if project_name_full_cleaned.lower().endswith(token_name.lower()) and project_name_full_cleaned.lower() != token_name.lower():
                    project_name = project_name_full_cleaned[:len(project_name_full_cleaned)-len(token_name)].strip()
                else:
                    project_name = project_name_full_cleaned.strip()
                

                funding_round = tds[1].text.strip()
                total_funding = tds[2].text.strip()
                valuation = tds[3].text.strip()
                last_funding_time = tds[4].text.strip()

                total_funding = convert_to_number(total_funding)
                valuation = convert_to_number(valuation)

                items.append({
                    'project_name': project_name,
                    'token_name': token_name,
                    'funding_round': funding_round,
                    'total_funding': total_funding,
                    'valuation': valuation,
                    'last_funding_time': last_funding_time
                })
            except Exception as e:
                print(f"Error parsing row on page {page_number}: {e}")
        # print(f"Successfully parsed {len(items)} items on page {page_number}")
    except Exception as e:
        print(f"Error parsing table on page {page_number}: {e}")

    return items

def click_next_page(driver, is_investor):
    try:
        if is_investor:
            next_button_js = """
            document.querySelector("#app > div > main > div > div > div.row.detail.common_detail.justify-start.justify-md-center > div.detail_l.col-sm-12.col-md-8.col-lg-9.col-xl-9.col-12 > div.v-window.v-item-group.theme--light.v-tabs-items > div > div > div.investment > div:nth-child(4) > div.pagination-container.d-flex.justify-center > div > button.btn-next").click();
            """
        else:
            next_button_js = """
            document.querySelector("#app > div > main > div > div > div.row.detail.common_detail.justify-start.justify-md-center > div.detail_l.col-sm-12.col-md-8.col-lg-9.col-xl-9.col-12 > div.v-window.detail_tab_items.v-item-group.theme--light.v-tabs-items > div > div > div.investment > div:nth-child(4) > div.pagination-container.d-flex.justify-center > div > button.btn-next").click();
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

    time.sleep(1.5)

    current_url = driver.current_url
    if "zh" in current_url:
        driver.get(url)
        # print("Redirected to the correct URL.")
        time.sleep(1.5)

    try:
        if is_investor:
            initial_button_js = """
            document.querySelector("#app > div > main > div > div > div.row.detail.common_detail.justify-start.justify-md-center > div.detail_l.col-sm-12.col-md-8.col-lg-9.col-xl-9.col-12 > div.v-window.v-item-group.theme--light.v-tabs-items > div > div > div.investment > div.d-flex.flex-row.align-center.justify-space-between > div.d-flex.flex-column.flex-md-row.align-end.align-md-center > div > button:nth-child(2)").click();
            """
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#app > div > main > div > div > div.row.detail.common_detail.justify-start.justify-md-center > div.detail_l.col-sm-12.col-md-8.col-lg-9.col-xl-9.col-12 > div.v-window.v-item-group.theme--light.v-tabs-items > div > div > div.investment > div.d-flex.flex-row.align-center.justify-space-between > div.d-flex.flex-column.flex-md-row.align-end.align-md-center > div > button:nth-child(2)")))
        else:
            initial_button_js = """
            document.querySelector("#app > div > main > div > div > div.row.detail.common_detail.justify-start.justify-md-center > div.detail_l.col-sm-12.col-md-8.col-lg-9.col-xl-9.col-12 > div.v-window.detail_tab_items.v-item-group.theme--light.v-tabs-items > div > div > div.investment > div.d-flex.flex-row.align-center.justify-space-between > div.d-flex.flex-column.flex-md-row.align-end.align-md-center > div > button:nth-child(2)").click();
            """
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#app > div > main > div > div > div.row.detail.common_detail.justify-start.justify-md-center > div.detail_l.col-sm-12.col-md-8.col-lg-9.col-xl-9.col-12 > div.v-window.detail_tab_items.v-item-group.theme--light.v-tabs-items > div > div > div.investment > div.d-flex.flex-row.align-center.justify-space-between > div.d-flex.flex-column.flex-md-row.align-end.align-md-center > div > button:nth-child(2)")))
        driver.execute_script(initial_button_js)
        # print("Initial button clicked successfully.")
        time.sleep(1)
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
            time.sleep(1.2)  
            # print(f"Successfully navigated to page {page_number + 1}")
            page_number += 1
        except Exception as e:
            print(f"An error occurred while parsing page {page_number}: {e}")
            break

    driver.quit()

    # Save items to CSV
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'Data')
    os.makedirs(data_dir, exist_ok=True)
    progress_csv_path = os.path.join(data_dir, '[ignore]Progress.csv')

    df = pd.DataFrame(all_items)

    df['project_name'] = df.apply(lambda row: row['token_name'] if row['project_name'] == '' else row['project_name'], axis=1)
    
    df['Sector'] = ''
    df['Price'] = ''
    df['MC'] = ''
    df['FDV'] = ''
    df['Exchange'] = ''
    df = df[['token_name', 'project_name', 'Sector', 'last_funding_time', 'funding_round', 'total_funding', 'valuation', 'Price', 'MC', 'FDV', 'Exchange']]
    df.columns = ['Token', 'Name', 'Sector', 'Date', 'Round', 'Total Funding', 'Valuation', 'Price', 'MC', 'FDV', 'Exchange']
    df.to_csv(progress_csv_path, index=False)
    # print(f"CSV file '{progress_csv_path}' created successfully.")

    # for item in all_items:
    #     print(f"Project Name: {item['project_name']}")
    #     print(f"Token Name: {item['token_name']}")
    #     print(f"Funding Round: {item['funding_round']}")
    #     print(f"Total Funding: {item['total_funding']}")
    #     print(f"Valuation: {item['valuation']}")
    #     print(f"Last Funding Time: {item['last_funding_time']}")
    #     print("-" * 20)

if __name__ == "__main__":
    main()