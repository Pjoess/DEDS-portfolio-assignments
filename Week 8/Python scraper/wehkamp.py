import requests
import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


driver = webdriver.Chrome()
# ?pagina=2

url_wehkamp_homepage ='https://www.wehkamp.nl/heren-kleding-jassen/'
headers = {
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}
response = requests.get(url_wehkamp_homepage, headers=headers)


soup = BeautifulSoup(response.content, 'html.parser')
product_tags = soup.find_all('li', {'class': 'UI_ProductGrid_item'})





with open('Wehkamp_jassen.csv', 'w', newline='') as csvfile:
    fieldnames = ['review', 'price', 'description']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()


    for tag in product_tags:
        url = tag.find('a')['href']
        driver.get(url)



        try:
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "Reviews__list___KfPgV"))
            )
        finally:
            driver.quit()

        reviews = soup.find_all('li', {'class': 'UI_ProductGrid_item'})
        if not reviews:
            continue

        containers = driver.find_elements(By.CLASS_NAME, 'padding-vertical-xsmall')
        for container in containers:
            title = container.find_element(By.CLASS_NAME, 'type-body').text
            # review = container.find_element(By.CLASS_NAME, 'color-black-opacity-88').text
            print(title)
            # print(review)


        # name = tag.find('div', {'class': 'as-m-product-tile__title-wrapper'}).text.strip()
        # price = tag.find('div', {'class': 'as-a-price__value as-a-price__value--sell'}).text.strip()
        # description = tag.find('div', {'class': 'as-m-product-tile__info-wrapper'}).text.strip()
        # writer.writerow({'name': name, 'price': price, 'description': description})
