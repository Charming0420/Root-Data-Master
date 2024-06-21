import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def fetch_page_content(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

    driver.get(url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "row")))

    html_content = driver.page_source
    driver.quit()

    return html_content

def parse_list_page(html_content):
    soup = BeautifulSoup(html_content, 'lxml')
    items = []

    list_container = soup.select_one('.row.list')
    if not list_container:
        raise Exception("Failed to find the list container.")

    list_items = list_container.find_all('div', recursive=False)

    for item in list_items:
        logo = item.find('img')['src'] if item.find('img') else None
        name = item.select_one('.ml-2').text.strip() if item.select_one('.ml-2') else None
        description = item.select_one('.mb-0.mt-2.intro').text.strip() if item.select_one('.mb-0.mt-2.intro') else None

        if name:
            items.append({
                'logo': logo,
                'name': name,
                'description': description
            })

    # print(f"Total items fetched by investment data script: {len(items)}")
    return items

def main(url):
    html_content = fetch_page_content(url)
    items = parse_list_page(html_content)
    return items

if __name__ == "__main__":
    # url = "https://www.rootdata.com/Projects/detail/DWF%20Labs?k=NDA3NQ%3D%3D"
    main(url)