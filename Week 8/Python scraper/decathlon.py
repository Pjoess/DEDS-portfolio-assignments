import requests
import csv
from bs4 import BeautifulSoup
page = 0
max = 40 #1600
name = 1

headers = {
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

with open('decathlon.csv', 'w', newline='') as csvfile:
    fieldnames = []
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    while page <= max:
        homepage = 'https://www.decathlon.nl/search?Ntt=jas&facets=genderLabels:HEREN_&from={0}&size=40'
        homepage = homepage.format(page)
        page+=40

        response = requests.get(homepage, headers=headers)


        soup = BeautifulSoup(response.content, 'html.parser')
        products = soup.find_all('div', {'class': 'vtmn-flex vtmn-flex-col vtmn-items-center vtmn-relative vtmn-overflow-hidden vtmn-text-center vtmn-z-0 dpb-holder svelte-2ckipo'})




        for product in products:

            url = 'https://www.decathlon.nl' + product.find('a')['href']
            print(url)

            rp = requests.get(url, headers=headers)
            item = BeautifulSoup(rp.content, 'html.parser')

            review_list = item.find('section', {'class': 'review-list'})

            product_reviews = review_list.find('a')['href']
            pg = requests.get(product_reviews, headers=headers)
            product_reviews_ = BeautifulSoup(pg.content, 'html.parser')

            product_reviews_list = product_reviews_.find_all('article', {'class': 'review-article-container'})

        #
        #     img = item.find('img', {'data-test': 'product-main-image'})
        #     img_link = img["src"]
        #     if "noimage" not in img_link.lower():
        #         response = requests.get(img_link)
        #
        #         # Check if the request was successful and the image exists
        #         if response.status_code == 200:
        #             # Schrijf de inhoud van de response weg naar een lokale bestand
        #             bestandsnaam = f'images/product{str(name)}.jpg'
        #             with open(bestandsnaam, 'wb') as f:
        #                 f.write(response.content)
        #             print(f'Afbeelding opgeslagen als {bestandsnaam}.')
        #         else:
        #             print(f'Afbeelding voor product {str(name)} niet gevonden.')
        #     else:
        #         print(f'Product {str(name)} heeft geen afbeelding beschikbaar.')
        #
            for review in product_reviews_list:

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
