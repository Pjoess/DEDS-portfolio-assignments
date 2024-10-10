import requests
import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


# driver = webdriver.Chrome()
# ?pagina=2

# ?page=2
page = 1
max = 500
name = 1

headers = {
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

with open('bol.csv', 'w', newline='') as csvfile:
    fieldnames = ['product_name','price','title','reviewer','date','description']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    while page <= max:
        homepage = 'https://www.bol.com/nl/nl/l/jassen/47445/?page=' + str(page)
        response = requests.get(homepage, headers=headers)


        soup = BeautifulSoup(response.content, 'html.parser')
        product_tags = soup.find_all('li', {'class': 'product-item--column'})




        for tag in product_tags:

            url = "https://bol.com" + tag.find('a')['href']
            print(url)

            rp = requests.get(url, headers=headers)
            item = BeautifulSoup(rp.content, 'html.parser')

            product_reviews = item.find_all('li', {'class': 'review'})

            img = item.find('img', {'data-test': 'product-main-image'})
            img_link = img["src"]
            if "noimage" not in img_link.lower():
                response = requests.get(img_link)

                # Check if the request was successful and the image exists
                if response.status_code == 200:
                    # Schrijf de inhoud van de response weg naar een lokale bestand
                    bestandsnaam = f'images/product{str(name)}.jpg'
                    with open(bestandsnaam, 'wb') as f:
                        f.write(response.content)
                    print(f'Afbeelding opgeslagen als {bestandsnaam}.')
                else:
                    print(f'Afbeelding voor product {str(name)} niet gevonden.')
            else:
                print(f'Product {str(name)} heeft geen afbeelding beschikbaar.')

            for review in product_reviews:

                product_name = None
                price = None
                title = None
                reviewer = None
                date = None
                description = None

                if item.find('span', {'data-test': 'title'}) is not None and isinstance(item.find('span', {'data-test': 'title'}).text, str):
                    product_name = item.find('span', {'data-test': 'title'}).text.strip()
                else:
                    continue  # skip this review if title is not text type
                if item.find('span', {'data-test': 'price'}) is not None and isinstance(item.find('span', {'data-test': 'price'}).text, str):
                    price = item.find('span', {'data-test': 'price'}).text.strip()
                else:
                    continue  # skip this review if title is not text type

                if review.find('strong', {'class': 'review__title'}) is not None and isinstance(review.find('strong', {'class': 'review__title'}).text, str):
                    title = review.find('strong', {'class': 'review__title'}).text.strip()
                else:
                    continue  # skip this review if title is not text type
                if review.find('li', {'data-test': 'review-author-name'}) is not None and isinstance(review.find('li', {'data-test': 'review-author-name'}).text, str):
                    reviewer = review.find('li', {'data-test': 'review-author-name'}).text.strip()
                else:
                    continue  # skip this review if title is not text type
                if review.find('li', {'data-test': 'review-author-date'}) is not None and isinstance(review.find('li', {'data-test': 'review-author-date'}).text, str):
                    date = review.find('li', {'data-test': 'review-author-date'}).text.strip()
                else:
                    continue  # skip this review if title is not text type
                if review.find('p', {'data-test': 'review-body'}) is not None and isinstance(review.find('p', {'data-test': 'review-body'}).text, str):
                    description = review.find('p', {'data-test': 'review-body'}).text.strip()
                else:
                    continue  # skip this review if title is not text type



                writer.writerow({'product_name': product_name, 'price': price, 'title': title, 'reviewer': reviewer, 'date': date, 'description': description})
            name+=1
        page+=1
