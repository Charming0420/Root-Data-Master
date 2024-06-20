import time
import random
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

def parse_table_page(driver, page_number):
    items = []
    try:
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "table")))
        rows = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")
        print(f"Found {len(rows)} rows on page {page_number}")

        for row in rows:
            try:
                project_name = row.find_element(By.CSS_SELECTOR, ".el-tooltip.list_name.animation_underline").text.strip()
                token_name_element = row.find_elements(By.CSS_SELECTOR, ".symbol.ml-1.d-none.d-md-inline")
                token_name = token_name_element[0].text.strip() if token_name_element else ""
                funding_round = row.find_elements(By.CSS_SELECTOR, ".align_right")[0].text.strip()
                total_funding = row.find_element(By.CSS_SELECTOR, ".d-flex.flex-row.align-center.justify-end").text.strip()
                valuation = row.find_elements(By.CSS_SELECTOR, ".align_right")[1].text.strip() if len(row.find_elements(By.CSS_SELECTOR, ".align_right")) > 1 else ""
                last_funding_time = row.find_element(By.CSS_SELECTOR, ".text_wrap.d-flex.flex-row.align-center.justify-end").text.strip()

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
        print(f"Successfully parsed {len(items)} items on page {page_number}")
    except Exception as e:
        print(f"Error parsing table on page {page_number}: {e}")

    return items

def click_next_page(driver):
    try:
        next_button_js = """
        document.querySelector("#app > div > main > div > div > div.row.detail.common_detail.justify-start.justify-md-center > div.detail_l.col-sm-12.col-md-8.col-lg-9.col-xl-9.col-12 > div.v-window.detail_tab_items.v-item-group.theme--light.v-tabs-items > div > div > div.investment > div:nth-child(4) > div.pagination-container.d-flex.justify-center > div > button.btn-next").click();
        """
        driver.execute_script(next_button_js)
        print("Next button clicked successfully.")
    except Exception as e:
        print(f"Failed to click next button: {e}")

def main():
    url = "https://www.rootdata.com/Projects/detail/DWF%20Labs?k=NDA3NQ%3D%3D"
    driver = setup_driver()
    driver.get(url)

    time.sleep(5)

    current_url = driver.current_url
    if "zh" in current_url:
        driver.get(url)
        print("Redirected to the correct URL.")
        time.sleep(5)

    try:
        initial_button_js = """
        document.querySelector("#app > div > main > div > div > div.row.detail.common_detail.justify-start.justify-md-center > div.detail_l.col-sm-12.col-md-8.col-lg-9.col-xl-9.col-12 > div.v-window.detail_tab_items.v-item-group.theme--light.v-tabs-items > div > div > div.investment > div.d-flex.flex-row.align-center.justify-space-between > div.d-flex.flex-column.flex-md-row.align-end.align-md-center > div > button:nth-child(2)").click();
        """
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#app > div > main > div > div > div.row.detail.common_detail.justify-start.justify-md-center > div.detail_l.col-sm-12.col-md-8.col-lg-9.col-xl-9.col-12 > div.v-window.detail_tab_items.v-item-group.theme--light.v-tabs-items > div > div > div.investment > div.d-flex.flex-row.align-center.justify-space-between > div.d-flex.flex-column.flex-md-row.align-end.align-md-center > div > button:nth-child(2)")))
        driver.execute_script(initial_button_js)
        print("Initial button clicked successfully.")
        time.sleep(5)
    except Exception as e:
        print(f"Failed to click initial button: {e}")
        driver.quit()
        return

    all_items = []
    page_number = 1

    while True:
        try:
            print(f"Parsing page {page_number}")
            items = parse_table_page(driver, page_number)
            if not items:
                print("No items found on this page, stopping.")
                break
            all_items.extend(items)

            prev_rows = len(driver.find_elements(By.CSS_SELECTOR, "table tbody tr"))
            click_next_page(driver)
            time.sleep(5)  # 增加等待時間，確保頁面完全加載
            WebDriverWait(driver, 20).until(lambda d: len(d.find_elements(By.CSS_SELECTOR, "table tbody tr")) == prev_rows)
            print(f"Successfully navigated to page {page_number + 1}")
            page_number += 1
        except Exception as e:
            print(f"An error occurred while parsing page {page_number}: {e}")
            break

    driver.quit()

    for item in all_items:
        print(f"Project Name: {item['project_name']}")
        print(f"Token Name: {item['token_name']}")
        print(f"Funding Round: {item['funding_round']}")
        print(f"Total Funding: {item['total_funding']}")
        print(f"Valuation: {item['valuation']}")
        print(f"Last Funding Time: {item['last_funding_time']}")
        print("-" * 20)

if __name__ == "__main__":
    main()