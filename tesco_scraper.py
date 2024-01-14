from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import csv

def extract_data_from_url(url, output_file='output.csv'):
    options = Options()
    options.add_argument("--headless")
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument("--disable-extensions")
    options.add_experimental_option('useAutomationExtension', False)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
    driver = webdriver.Chrome(options=options)
    page_number = 1

    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Title', 'Price', 'Price Per', 'Image URL']
        csv_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Write the header
        csv_writer.writeheader()

        while True:
            current_url = f"{url}?page={page_number}&count=48"
            driver.get(current_url)

            time.sleep(1)
            
            # Check if the page has products
            products = driver.find_elements(By.CLASS_NAME, 'styles__StyledVerticalTileWrapper-dvv1wj-0.dtCNPH')
            if not products:
                print("No more products found!")
                break  # No more pages, exit the loop

            for product in products:
                title = product.find_element(By.CLASS_NAME, "styled__Text-sc-1i711qa-1.xZAYu.ddsweb-link__text").text
                try:
                    price = product.find_element(By.CLASS_NAME, "styled__StyledHeading-sc-119w3hf-2.jWPEtj.styled__Text-sc-8qlq5b-1.lnaeiZ.beans-price__text").text
                except:
                    price = "Currently out of stock"

                try:
                    priceper = product.find_element(By.CLASS_NAME, "styled__StyledFootnote-sc-119w3hf-7.icrlVF.styled__Subtext-sc-8qlq5b-2.bNJmdc.beans-price__subtext").text
                except:
                    priceper = ""

                image_element = product.find_element(By.CLASS_NAME, "styled__Image-sc-j2gwt2-0.iCtiex.product-image.ddsweb-responsive-image__image")
                driver.execute_script("arguments[0].scrollIntoView();", image_element)
                image_url = image_element.get_attribute("src")

                # Write the data to CSV
                csv_writer.writerow({'Title': title, 'Price': price, 'Price Per': priceper, 'Image URL': image_url})

            time.sleep(2)
            page_number += 1

    driver.quit()


# Specify the output file path if you want to use a different name/location
output_file_path = 'finestfoodcupboard.csv'
url = 'https://www.tesco.ie/groceries/en-IE/shop/tesco-finest/finest-food-cupboard/all'
extract_data_from_url(url, output_file_path)
