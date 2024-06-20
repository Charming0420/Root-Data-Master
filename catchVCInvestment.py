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
    # 設置 Chrome 瀏覽器選項
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # 在背景執行瀏覽器
    chrome_options.add_argument("--disable-gpu")  # 關閉 GPU 加速

    # 使用 ChromeDriverManager 來自動管理 ChromeDriver
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

    driver.get(url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "row")))

    html_content = driver.page_source
    driver.quit()

    return html_content

def parse_list_page(html_content):
    soup = BeautifulSoup(html_content, 'lxml')
    items = []

    # 找到列表的父容器
    list_container = soup.select_one('.row.list')
    if not list_container:
        raise Exception("Failed to find the list container.")

    # 找到所有列表項目
    list_items = list_container.find_all('div', recursive=False)
    
    for item in list_items:
        logo = item.find('img')['src'] if item.find('img') else None
        name = item.select_one('.ml-2').text.strip() if item.select_one('.ml-2') else None
        description = item.select_one('.mb-0.mt-2.intro').text.strip() if item.select_one('.mb-0.mt-2.intro') else None
        
        if name:  # 剔除那些 Name 為 None 的元素
            items.append({
                'logo': logo,
                'name': name,
                'description': description
            })

    return items

def main():
    url = "https://www.rootdata.com/zh/Projects/detail/DWF%20Labs?k=NDA3NQ%3D%3D"
    html_content = fetch_page_content(url)
    items = parse_list_page(html_content)
    
    for item in items:
        print(f"Name: {item['name']}")
        print(f"Logo: {item['logo']}")
        print(f"Description: {item['description']}")
        print("-" * 20)

if __name__ == "__main__":
    main()