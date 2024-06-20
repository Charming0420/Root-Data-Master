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
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
    return driver

def display_target_div(driver, target_selector):
    try:
        target_div = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, target_selector)))
        driver.execute_script("arguments[0].style.display = 'block';", target_div)
        print(f"Div with CSS Selector '{target_selector}' displayed successfully.")
    except Exception as e:
        print(f"Div not found or not displayable: {e}")
        driver.quit()
        exit()

def parse_table_page(driver):
    items = []
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "table")))
        rows = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")

        for row in rows:
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
        print(f"Error parsing table: {e}")

    return items

def main():
    url = "https://www.rootdata.com/zh/Projects/detail/DWF%20Labs?k=NDA3NQ%3D%3D"
    driver = setup_driver()
    driver.get(url)

    show_div_selector = "#app > div > main > div > div > div.row.detail.common_detail.justify-start.justify-md-center > div.detail_l.col-sm-12.col-md-8.col-lg-9.col-xl-9.col-12 > div.v-window.detail_tab_items.v-item-group.theme--light.v-tabs-items > div > div > div.investment > div:nth-child(4)"
    hide_div_selector = "#app > div > main > div > div > div.row.detail.common_detail.justify-start.justify-md-center > div.detail_l.col-sm-12.col-md-8.col-lg-9.col-xl-9.col-12 > div.v-window.detail_tab_items.v-item-group.theme--light.v-tabs-items > div > div > div.investment > div:nth-child(3)"
    display_target_div(driver, show_div_selector)
    display_target_div(driver, hide_div_selector)

    all_items = []
    page_number = 1

    while True:
        print(f"Parsing page {page_number}")
        items = parse_table_page(driver)
        all_items.extend(items)

        # 嘗試使用提供的 CSS Selector 來點擊按鈕
        try:
            next_button_selector = '#app > div > main > div > div > div.row.detail.common_detail.justify-start.justify-md-center > div.detail_l.col-sm-12.col-md-8.col-lg-9.col-xl-9.col-12 > div.v-window.v-item-group.theme--light.v-tabs-items > div > div > div.investment > div:nth-child(4) > div.pagination-container.d-flex.justify-center > div > button.btn-next'
            next_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, next_button_selector)))
            
            if next_button:
                driver.execute_script("arguments[0].scrollIntoView();", next_button)
                time.sleep(2)  # 確保按鈕在視野內
                driver.execute_script("arguments[0].click();", next_button)
                WebDriverWait(driver, 20).until(EC.staleness_of(next_button))
                WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "table")))
                page_number += 1
                time.sleep(random.randint(5, 15))
            else:
                print("Next button not found or not clickable.")
                break
        except Exception as e:
            print(f"An error occurred: {e}")
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