import requests
import csv
from bs4 import BeautifulSoup
import time

def get_value(element, class_name):
    found_element = element.find(class_=class_name)
    return found_element.text.strip() if found_element else 'None'

def scrape_and_update_url(base_url, page_number, skip_value):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

    while True:
        # Construct the URL for the current page
        url = f"{base_url}?page={page_number}&skip={skip_value}"

        # Send a GET request to the URL
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find all product cards on the page
            product_cards = soup.find_all('article', class_='ProductCardWrapper--6uxd5a')

            if not product_cards:
                # If no product cards are found, terminate the loop
                print("No more products found!")
                break

            # Print headers
            if page_number == 1:
                print("Product Title,Price Per Weight,Savings,Image URL")

            for card in product_cards:
                # Extracting product title (containing price)
                product_title = card.find('p', class_='AriaProductTitleParagraph--1yc7f4f').text.strip()

                # Extracting price per weight
                price_per_weight = get_value(card, 'ProductCardPriceInfo--1vvb8df')

                # Extracting product savings
                product_savings = get_value(card, 'Badge--ayjc1w')

                # Extracting product image URL
                product_image_url = card.find('img')['src']

                # Print product information in CSV format
                print(f'"{product_title}","{price_per_weight}","{product_savings}","{product_image_url}"')

            # Update page_number and skip_value for the next iteration
            page_number += 1
            skip_value += 30

            # Introduce a delay of 1.5 seconds before the next request
            time.sleep(1.5)

        else:
            print(f"Failed to retrieve the page {page_number}. Status code:", response.status_code)
            break

# Example usage:
base_url = "https://shop.supervalu.ie/sm/delivery/rsid/5550/categories/chilled-food/soup-id-O200215"
scrape_and_update_url(base_url, page_number=1, skip_value=0)
