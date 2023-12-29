from selenium import webdriver
from selenium.webdriver.common.by import By
import time

url = 'https://www.tesco.ie/groceries/en-IE/shop/bakery/in-store-bakery/all'

driver = webdriver.Chrome()

driver.get(url)


products = driver.find_elements(By.CLASS_NAME, 'styles__StyledVerticalTileWrapper-dvv1wj-0.dtCNPH')
for product in products:
    title = product.find_element(By.CLASS_NAME, "styled__Text-sc-1i711qa-1.xZAYu.ddsweb-link__text").text
    price = product.find_element(By.CLASS_NAME, "styled__StyledHeading-sc-119w3hf-2.jWPEtj.styled__Text-sc-8qlq5b-1.lnaeiZ.beans-price__text").text
    priceper = product.find_element(By.CLASS_NAME, "styled__StyledFootnote-sc-119w3hf-7.icrlVF.styled__Subtext-sc-8qlq5b-2.bNJmdc.beans-price__subtext").text
    image_element = product.find_element(By.CLASS_NAME, "styled__Image-sc-j2gwt2-0.iCtiex.product-image.ddsweb-responsive-image__image")
    # Scroll the image element into view
    driver.execute_script("arguments[0].scrollIntoView();", image_element)
    image_url = image_element.get_attribute("src")


    print(f'"{title}","{price}","{priceper}","{image_url}"')
