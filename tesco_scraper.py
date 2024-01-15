from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import csv
from urllib.parse import urljoin
import os

def extract_data_from_url(url, output_file):
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
        fieldnames = ['Title', 'Price', 'Promotional Price', 'Price Per', 'Product URL', 'Image URL']
        csv_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write the header
        csv_writer.writeheader()

        while True:
            promotion_substring = '?viewAll=promotion&promotion=offers'
            url_prefix = '&' if promotion_substring in url else '?'
            current_url = f"{url}{url_prefix}page={page_number}&count=48"
            driver.get(current_url)

            time.sleep(1)

            # Check if the page has products
            products = driver.find_elements(By.CLASS_NAME, 'styles__StyledVerticalTileWrapper-dvv1wj-0.dtCNPH')
            if not products:
                print("No more products found!")
                break  # No more pages, exit the loop

            for product in products:
                title_element = product.find_element(By.CLASS_NAME, "styled__Text-sc-1i711qa-1.xZAYu.ddsweb-link__text")
                title = title_element.text
                product_url = title_element.find_element(By.XPATH, "..").get_attribute("href")

                try:
                    price_element = product.find_element(By.CLASS_NAME, "styled__StyledHeading-sc-119w3hf-2.jWPEtj.styled__Text-sc-8qlq5b-1.lnaeiZ.beans-price__text")
                    price = price_element.text
                except:
                    price_element = None
                    price = "Currently out of stock"

                try:
                    priceper = product.find_element(By.CLASS_NAME, "styled__StyledFootnote-sc-119w3hf-7.icrlVF.styled__Subtext-sc-8qlq5b-2.bNJmdc.beans-price__subtext").text
                except:
                    priceper = ""

                try:
                    promotional_price_element = product.find_element(By.CLASS_NAME, "offer-text")
                    promotional_price = promotional_price_element.text
                except:
                    promotional_price_element = None
                    promotional_price = ""

                image_element = product.find_element(By.CLASS_NAME, "styled__Image-sc-j2gwt2-0.iCtiex.product-image.ddsweb-responsive-image__image")
                driver.execute_script("arguments[0].scrollIntoView();", image_element)
                image_url = image_element.get_attribute("src")

                # Write the data to CSV
                csv_writer.writerow({
                    'Title': title,
                    'Price': price,
                    'Promotional Price': promotional_price,
                    'Price Per': priceper,
                    'Product URL': product_url,
                    'Image URL': image_url
                })

            time.sleep(1)
            page_number += 1

    driver.quit()

def scrape_category(category_name, category_data):
    category_folder = os.path.join(output_folder, category_name)
    os.makedirs(category_folder, exist_ok=True)

    for subcategory_name, subcategory_url in category_data.items():
        subcategory_folder = os.path.join(category_folder, subcategory_name)
        os.makedirs(subcategory_folder, exist_ok=True)
        for subsubcatrgory, subsubcatrgory_url in subcategory_url.items():
            full_url = urljoin(base_url, subsubcatrgory_url.replace("?include-children=true", ""))
            output_file_path = os.path.join(subcategory_folder, f'{subsubcatrgory}.csv')
            extract_data_from_url(full_url, output_file_path)

# Specify the output folder path
output_folder = 'C:\\Users\\dammy.OLUWADAMILOLA\\VS Developer\\WebScraper\\Tesco'

# Base URL
base_url = 'https://www.tesco.ie'

# Categories dictionary
categories = {
    'Fresh Food': {
        'Fresh Fruit': {
            'All Fresh Fruit': '/groceries/en-IE/shop/fresh-food/fresh-fruit/all',
            'Apples, Pears & Rhubarb': '/groceries/en-IE/shop/fresh-food/fresh-fruit/apples-pears-and-rhubarb',
            'Avocados': '/groceries/en-IE/shop/fresh-food/fresh-fruit/avocados',
            'Bananas': '/groceries/en-IE/shop/fresh-food/fresh-fruit/bananas',
            'Berries & Cherries': '/groceries/en-IE/shop/fresh-food/fresh-fruit/berries-and-cherries',
            'Citrus Fruit': '/groceries/en-IE/shop/fresh-food/fresh-fruit/citrus-fruit',
            'Dried Fruit & Nuts': '/groceries/en-IE/shop/fresh-food/fresh-fruit/dried-fruit-and-nuts',
            'Grapes': '/groceries/en-IE/shop/fresh-food/fresh-fruit/grapes',
            'Nectarines & Peaches': '/groceries/en-IE/shop/fresh-food/fresh-fruit/nectarines-and-peaches',
            'Organic Fruit': '/groceries/en-IE/shop/fresh-food/fresh-fruit/organic-fruit',
            'Plums & Apricots': '/groceries/en-IE/shop/fresh-food/fresh-fruit/plums-and-apricots',
            'Prepared Fruit': '/groceries/en-IE/shop/fresh-food/fresh-fruit/prepared-fruit',
            'Tropical & Exotic Fruit': '/groceries/en-IE/shop/fresh-food/fresh-fruit/tropical-and-exotic-fruit',
            'Offers on Fresh Fruit': '/groceries/en-IE/shop/fresh-food/fresh-fruit/all?viewAll=promotion&promotion=offers',
        },
        'Fresh Vegetables': {
            'All Fresh Vegetables': '/groceries/en-IE/shop/fresh-food/fresh-vegetables/all',
            'Baby Vegetables': '/groceries/en-IE/shop/fresh-food/fresh-vegetables/baby-vegetables',
            'Broccoli, Cauliflower & Cabbage': '/groceries/en-IE/shop/fresh-food/fresh-vegetables/broccoli-cauliflower-and-cabbage',
            'Carrots & Root Vegetables': '/groceries/en-IE/shop/fresh-food/fresh-vegetables/carrots-and-root-vegetables',
            'Chillies, Garlic & Ginger': '/groceries/en-IE/shop/fresh-food/fresh-vegetables/chillies-garlic-and-ginger',
            'Courgettes, Aubergines & Asparagus': '/groceries/en-IE/shop/fresh-food/fresh-vegetables/courgettes-aubergines-and-asparagus',
            'Mushrooms': '/groceries/en-IE/shop/fresh-food/fresh-vegetables/mushrooms',
            'Onions & Shallots': '/groceries/en-IE/shop/fresh-food/fresh-vegetables/onions-and-shallots',
            'Organic Vegetables': '/groceries/en-IE/shop/fresh-food/fresh-vegetables/organic-vegetables',
            'Peas, Beans & Sweetcorn': '/groceries/en-IE/shop/fresh-food/fresh-vegetables/peas-beans-and-sweetcorn',
            'Potatoes': '/groceries/en-IE/shop/fresh-food/fresh-vegetables/potatoes',
            'Prepared Vegetables': '/groceries/en-IE/shop/fresh-food/fresh-vegetables/prepared-vegetables',
            'Seasonal Vegetables': '/groceries/en-IE/shop/fresh-food/fresh-vegetables/seasonal-vegetables',
            'Spinach, Greens & Kale': '/groceries/en-IE/shop/fresh-food/fresh-vegetables/spinach-greens-and-kale',
            'Stir Fry': '/groceries/en-IE/shop/fresh-food/fresh-vegetables/stir-fry',
            'Offers on Fresh Vegetables': '/groceries/en-IE/shop/fresh-food/fresh-vegetables/all?viewAll=promotion&promotion=offers',
        },
        'Salads & Dips': {
            'All Salads & Dips': '/groceries/en-IE/shop/fresh-food/salads-and-dips/all',
            'Chilled Dips': '/groceries/en-IE/shop/fresh-food/salads-and-dips/chilled-dips',
            'Coleslaw & Dressed Salads': '/groceries/en-IE/shop/fresh-food/salads-and-dips/coleslaw-and-dressed-salads',
            'Fresh Herbs, Chillies & Spices': '/groceries/en-IE/shop/fresh-food/salads-and-dips/fresh-herbs-chillies-and-spices',
            'Prepared Salad & Salad Bags': '/groceries/en-IE/shop/fresh-food/salads-and-dips/prepared-salad-and-salad-bags',
            'Salad Vegetables': '/groceries/en-IE/shop/fresh-food/salads-and-dips/salad-vegetables',
            'Tomatoes': '/groceries/en-IE/shop/fresh-food/salads-and-dips/tomatoes',
            'Offers on Salads & Dips': '/groceries/en-IE/shop/fresh-food/salads-and-dips/all?viewAll=promotion&promotion=offers',
        },
        'Milk, Butter & Eggs': {
            'All Milk, Butter & Eggs': '/groceries/en-IE/shop/fresh-food/milk-butter-and-eggs/all',
            'Butter, Spreads & Margarine': '/groceries/en-IE/shop/fresh-food/milk-butter-and-eggs/butter-spreads-and-margarine',
            'Eggs': '/groceries/en-IE/shop/fresh-food/milk-butter-and-eggs/eggs',
            'Fresh Cream & Custard': '/groceries/en-IE/shop/fresh-food/milk-butter-and-eggs/fresh-cream-and-custard',
            'Fresh Milk': '/groceries/en-IE/shop/fresh-food/milk-butter-and-eggs/fresh-milk',
            'Baking & Cooking': '/groceries/en-IE/shop/fresh-food/milk-butter-and-eggs/baking-and-cooking',
            'Offers on Milk, Butter & Eggs': '/groceries/en-IE/shop/fresh-food/milk-butter-and-eggs/all?viewAll=promotion&promotion=offers',
        },
        'Cheese': {
            'All Cheese': '/groceries/en-IE/shop/fresh-food/cheese/all',
            'Cheese Boards & Gifts': '/groceries/en-IE/shop/fresh-food/cheese/cheese-boards-and-gifts',
            'Cheddar Cheese': '/groceries/en-IE/shop/fresh-food/cheese/cheddar-cheese',
            'Cheese Spreads & Snacks': '/groceries/en-IE/shop/fresh-food/cheese/cheese-spreads-and-snacks',
            'Cottage & Soft Cheese': '/groceries/en-IE/shop/fresh-food/cheese/cottage-and-soft-cheese',
            'Sliced & Grated Cheese': '/groceries/en-IE/shop/fresh-food/cheese/sliced-and-grated-cheese',
            'Speciality & Continental Cheese': '/groceries/en-IE/shop/fresh-food/cheese/speciality-and-continental-cheese',
            'Offers on Cheese': '/groceries/en-IE/shop/fresh-food/cheese/all?viewAll=promotion&promotion=offers',
        },
        'Yoghurt': {
            'All Yoghurt': '/groceries/en-IE/shop/fresh-food/yoghurt/all',
            'Yoghurts': '/groceries/en-IE/shop/fresh-food/yoghurt/yoghurts',
            'Yoghurt Drinks': '/groceries/en-IE/shop/fresh-food/yoghurt/yoghurt-drinks',
            'Offers on Yoghurt': '/groceries/en-IE/shop/fresh-food/yoghurt/all?viewAll=promotion&promotion=offers',
        },

        'Dairy Alternatives': {
            'All Dairy Alternatives': '/groceries/en-IE/shop/fresh-food/dairy-alternatives/all',
            'Dairy Alternatives': '/groceries/en-IE/shop/fresh-food/dairy-alternatives/dairy-alternatives',
            'Offers on Dairy Alternatives': '/groceries/en-IE/shop/fresh-food/dairy-alternatives/all?viewAll=promotion&promotion=offers',
        },

        'Fresh Meat & Poultry': {
            'All Fresh Meat & Poultry': '/groceries/en-IE/shop/fresh-food/fresh-meat-and-poultry/all',
            'Fresh Bacon': '/groceries/en-IE/shop/fresh-food/fresh-meat-and-poultry/fresh-bacon',
            'Fresh Beef': '/groceries/en-IE/shop/fresh-food/fresh-meat-and-poultry/fresh-beef',
            'Fresh Chicken': '/groceries/en-IE/shop/fresh-food/fresh-meat-and-poultry/fresh-chicken',
            'Fresh Duck': '/groceries/en-IE/shop/fresh-food/fresh-meat-and-poultry/fresh-duck',
            'Fresh Lamb': '/groceries/en-IE/shop/fresh-food/fresh-meat-and-poultry/fresh-lamb',
            'Fresh Pork': '/groceries/en-IE/shop/fresh-food/fresh-meat-and-poultry/fresh-pork',
            'Fresh Turkey': '/groceries/en-IE/shop/fresh-food/fresh-meat-and-poultry/fresh-turkey',
            'Ready to Cook': '/groceries/en-IE/shop/fresh-food/fresh-meat-and-poultry/ready-to-cook',
            'Breaded Poultry': '/groceries/en-IE/shop/fresh-food/fresh-meat-and-poultry/breaded-poultry',
            'Sausages': '/groceries/en-IE/shop/fresh-food/fresh-meat-and-poultry/sausages',
            'BBQ': '/groceries/en-IE/shop/fresh-food/fresh-meat-and-poultry/bbq',
            'Pudding': '/groceries/en-IE/shop/fresh-food/fresh-meat-and-poultry/pudding',
            'Rashers': '/groceries/en-IE/shop/fresh-food/fresh-meat-and-poultry/rashers',
            'Offers on Fresh Meat & Poultry': '/groceries/en-IE/shop/fresh-food/fresh-meat-and-poultry/all?viewAll=promotion&promotion=offers',
        },
        'Stuffing & Accompaniments': {
            'All Stuffing & Accompaniments': '/groceries/en-IE/shop/fresh-food/stuffing-and-accompaniments/all',
            'Breadcrumbs & Stuffing': '/groceries/en-IE/shop/fresh-food/stuffing-and-accompaniments/breadcrumbs-and-stuffing',
            'Sauces': '/groceries/en-IE/shop/fresh-food/stuffing-and-accompaniments/sauces',
            'Breadcrumbs': '/groceries/en-IE/shop/fresh-food/stuffing-and-accompaniments/breadcrumbs',
            'Stuffing': '/groceries/en-IE/shop/fresh-food/stuffing-and-accompaniments/stuffing',
            'Other': '/groceries/en-IE/shop/fresh-food/stuffing-and-accompaniments/other',
            'Offers on Stuffing & Accompaniments': '/groceries/en-IE/shop/fresh-food/stuffing-and-accompaniments/all?viewAll=promotion&promotion=offers',
        },

        'Chilled Fish & Sea Food': {
            'All Chilled Fish & Sea Food': '/groceries/en-IE/shop/fresh-food/chilled-fish-and-sea-food/all',
            'Breaded & Prepared': '/groceries/en-IE/shop/fresh-food/chilled-fish-and-sea-food/breaded-and-prepared',
            'Cod, Haddock & White Fish': '/groceries/en-IE/shop/fresh-food/chilled-fish-and-sea-food/cod-haddock-and-white-fish',
            'Mackerel': '/groceries/en-IE/shop/fresh-food/chilled-fish-and-sea-food/mackerel',
            'Prawns & Seafood': '/groceries/en-IE/shop/fresh-food/chilled-fish-and-sea-food/prawns-and-seafood',
            'Ready to Cook': '/groceries/en-IE/shop/fresh-food/chilled-fish-and-sea-food/ready-to-cook',
            'Salmon & Trout': '/groceries/en-IE/shop/fresh-food/chilled-fish-and-sea-food/salmon-and-trout',
            'Smoked Fish': '/groceries/en-IE/shop/fresh-food/chilled-fish-and-sea-food/smoked-fish',
            'Offers on Chilled Fish & Sea Food': '/groceries/en-IE/shop/fresh-food/chilled-fish-and-sea-food/all?viewAll=promotion&promotion=offers',
        },

        'Cooked Meat': {
            'All Cooked Meat': '/groceries/en-IE/shop/fresh-food/cooked-meat/all',
            'Cooked Chicken & Turkey': '/groceries/en-IE/shop/fresh-food/cooked-meat/cooked-chicken-and-turkey',
            'Deli Counter Cooked Meats': '/groceries/en-IE/shop/fresh-food/cooked-meat/deli-counter-cooked-meats',
            'Frankfurters & Snacking': '/groceries/en-IE/shop/fresh-food/cooked-meat/frankfurters-and-snacking',
            'Sliced Beef': '/groceries/en-IE/shop/fresh-food/cooked-meat/sliced-beef',
            'Sliced Ham': '/groceries/en-IE/shop/fresh-food/cooked-meat/sliced-ham',
            'Value Ham & Luncheon Meats': '/groceries/en-IE/shop/fresh-food/cooked-meat/value-ham-and-luncheon-meats',
            'Polish Cooked Meat': '/groceries/en-IE/shop/fresh-food/cooked-meat/polish-cooked-meat',
            'Offers on Cooked Meat': '/groceries/en-IE/shop/fresh-food/cooked-meat/all?viewAll=promotion&promotion=offers',
        },

        'Continental Meats & Antipasti': {
            'All Continental Meats & Antipasti': '/groceries/en-IE/shop/fresh-food/continental-meats-and-antipasti/all',
            'Chorizo & Pancetta': '/groceries/en-IE/shop/fresh-food/continental-meats-and-antipasti/chorizo-and-pancetta',
            'Continental Cooked Ham': '/groceries/en-IE/shop/fresh-food/continental-meats-and-antipasti/continental-cooked-ham',
            'Continental Meat Platters': '/groceries/en-IE/shop/fresh-food/continental-meats-and-antipasti/continental-meat-platters',
            'Olives & Antipasti': '/groceries/en-IE/shop/fresh-food/continental-meats-and-antipasti/olives-and-antipasti',
            'Parma Ham, Prosciutto & Serrano Ham': '/groceries/en-IE/shop/fresh-food/continental-meats-and-antipasti/parma-ham-prosciutto-and-serrano-ham',
            'Pate': '/groceries/en-IE/shop/fresh-food/continental-meats-and-antipasti/pate',
            'Salami & Pepperoni': '/groceries/en-IE/shop/fresh-food/continental-meats-and-antipasti/salami-and-pepperoni',
            'Offers on Continental Meats & Antipasti': '/groceries/en-IE/shop/fresh-food/continental-meats-and-antipasti/all?viewAll=promotion&promotion=offers',
        },

        'Chilled Food': {
            'All Chilled Food': '/groceries/en-IE/shop/fresh-food/chilled-food/all',
            'Polish Food': '/groceries/en-IE/shop/fresh-food/chilled-food/polish-food',
            'Offers on Chilled Food': '/groceries/en-IE/shop/fresh-food/chilled-food/all?viewAll=promotion&promotion=offers',
        },

        'Chilled Desserts': {
            'All Chilled Desserts': '/groceries/en-IE/shop/fresh-food/chilled-desserts/all',
            'Chilled Dessert': '/groceries/en-IE/shop/fresh-food/chilled-desserts/chilled-dessert',
            'Sponges, Pies & Puddings': '/groceries/en-IE/shop/fresh-food/chilled-desserts/sponges-pies-and-puddings',
            'Trifles & Cheesecakes': '/groceries/en-IE/shop/fresh-food/chilled-desserts/trifles-and-cheesecakes',
            'Fresh Cream Desserts': '/groceries/en-IE/shop/fresh-food/chilled-desserts/fresh-cream-desserts',
            'Individual Desserts': '/groceries/en-IE/shop/fresh-food/chilled-desserts/individual-desserts',
            'Indulgent Desserts': '/groceries/en-IE/shop/fresh-food/chilled-desserts/indulgent-desserts',
            'Rice Puddings': '/groceries/en-IE/shop/fresh-food/chilled-desserts/rice-puddings',
            'Low Fat Desserts': '/groceries/en-IE/shop/fresh-food/chilled-desserts/low-fat-desserts',
            'Offers on Chilled Desserts': '/groceries/en-IE/shop/fresh-food/chilled-desserts/all?viewAll=promotion&promotion=offers',
        },
        'Fresh Meals, Pizza, Pasta & Garlic Bread': {
            'All Fresh Meals, Pizza, Pasta & Garlic Bread': '/groceries/en-IE/shop/fresh-food/fresh-meals-pizza-pasta-and-garlic-bread/all',
            'Fresh Garlic & Cheese Breads': '/groceries/en-IE/shop/fresh-food/fresh-meals-pizza-pasta-and-garlic-bread/fresh-garlic-and-cheese-breads',
            'Fresh Pasta': '/groceries/en-IE/shop/fresh-food/fresh-meals-pizza-pasta-and-garlic-bread/fresh-pasta',
            'Fresh Pasta Sauce & Pesto': '/groceries/en-IE/shop/fresh-food/fresh-meals-pizza-pasta-and-garlic-bread/fresh-pasta-sauce-and-pesto',
            'Fresh Pizza': '/groceries/en-IE/shop/fresh-food/fresh-meals-pizza-pasta-and-garlic-bread/fresh-pizza',
            'Party Food': '/groceries/en-IE/shop/fresh-food/fresh-meals-pizza-pasta-and-garlic-bread/party-food',
            'Prepared Meals': '/groceries/en-IE/shop/fresh-food/fresh-meals-pizza-pasta-and-garlic-bread/prepared-meals',
            'Sandwiches, Snacks & Sushi': '/groceries/en-IE/shop/fresh-food/fresh-meals-pizza-pasta-and-garlic-bread/sandwiches-snacks-and-sushi',
            'Stock, Soup & Sauces': '/groceries/en-IE/shop/fresh-food/fresh-meals-pizza-pasta-and-garlic-bread/stock-soup-and-sauces',
            'Chilled Ready Meals': '/groceries/en-IE/shop/fresh-food/fresh-meals-pizza-pasta-and-garlic-bread/chilled-ready-meals',
            'Offers on Fresh Meals, Pizza, Pasta & Garlic Bread': '/groceries/en-IE/shop/fresh-food/fresh-meals-pizza-pasta-and-garlic-bread/all?viewAll=promotion&promotion=offers',
        },
        'Savoury Pastry': {
            'All Savoury Pastry': '/groceries/en-IE/shop/fresh-food/savoury-pastry/all',
            'Pies, Quiche & Pasties': '/groceries/en-IE/shop/fresh-food/savoury-pastry/pies-quiche-and-pasties',
            'Sausage Rolls, Cocktail Sausages & Scotch Eggs': '/groceries/en-IE/shop/fresh-food/savoury-pastry/sausage-rolls-cocktail-sausages-and-scotch-eggs',
            'Offers on Savoury Pastry': '/groceries/en-IE/shop/fresh-food/savoury-pastry/all?viewAll=promotion&promotion=offers',
        },
        'Flowers': {
            'All Flowers': '/groceries/en-IE/shop/fresh-food/flowers/all',
            'Bouquet': '/groceries/en-IE/shop/fresh-food/flowers/bouquet',
            'Offers on Flowers': '/groceries/en-IE/shop/fresh-food/flowers/all?viewAll=promotion&promotion=offers',
        },
        'Juices & Smoothies': {
            'All Juices & Smoothies': '/groceries/en-IE/shop/fresh-food/juices-and-smoothies/all',
            'Chilled Juice': '/groceries/en-IE/shop/fresh-food/juices-and-smoothies/chilled-juice',
            'Coconut Water': '/groceries/en-IE/shop/fresh-food/juices-and-smoothies/coconut-water',
            'Smoothies': '/groceries/en-IE/shop/fresh-food/juices-and-smoothies/smoothies',
            'Offers on Juices & Smoothies': '/groceries/en-IE/shop/fresh-food/juices-and-smoothies/all?viewAll=promotion&promotion=offers',
        },
        'Meat Free': {
            'All Meat Free': '/groceries/en-IE/shop/fresh-food/meat-free/all',
            'Meat Free Bacon & Pudding': '/groceries/en-IE/shop/fresh-food/meat-free/meat-free-bacon-and-pudding',
            'Meat Free Burgers': '/groceries/en-IE/shop/fresh-food/meat-free/meat-free-burgers',
            'Meat Free Chicken': '/groceries/en-IE/shop/fresh-food/meat-free/meat-free-chicken',
            'Meat Free Deli Slices': '/groceries/en-IE/shop/fresh-food/meat-free/meat-free-deli-slices',
            'Meat Free Mince & Meatballs': '/groceries/en-IE/shop/fresh-food/meat-free/meat-free-mince-and-meatballs',
            'Meat Free Other': '/groceries/en-IE/shop/fresh-food/meat-free/meat-free-other',
            'Meat Free Sausages': '/groceries/en-IE/shop/fresh-food/meat-free/meat-free-sausages',
            'Ready Meals': '/groceries/en-IE/shop/fresh-food/meat-free/ready-meals',
            'Tofu & Tempeh': '/groceries/en-IE/shop/fresh-food/meat-free/tofu-and-tempeh',
            'Offers on Meat Free': '/groceries/en-IE/shop/fresh-food/meat-free/all?viewAll=promotion&promotion=offers',
        },
    },
    'Bakery':{
        'In Store Bakery': {
            'All In Store Bakery': '/groceries/en-IE/shop/bakery/in-store-bakery/all',
            'Brown & Seeded Bread': '/groceries/en-IE/shop/bakery/in-store-bakery/brown-and-seeded-bread',
            'In Store French Bread & Rolls': '/groceries/en-IE/shop/bakery/in-store-bakery/in-store-french-bread-and-rolls',
            'In Store Speciality Bread': '/groceries/en-IE/shop/bakery/in-store-bakery/in-store-speciality-bread',
            'In Store Tea Cakes & Scones': '/groceries/en-IE/shop/bakery/in-store-bakery/in-store-tea-cakes-and-scones',
            'Rolls': '/groceries/en-IE/shop/bakery/in-store-bakery/rolls',
            'White Bread': '/groceries/en-IE/shop/bakery/in-store-bakery/white-bread',
            'Offers on In Store Bakery': '/groceries/en-IE/shop/bakery/in-store-bakery/all?viewAll=promotion&promotion=offers',
        },
        'Bread': {
            'All Bread': '/groceries/en-IE/shop/bakery/bread/all',
            'Brown & Seeded Bread': '/groceries/en-IE/shop/bakery/bread/brown-and-seeded-bread',
            'Naan & Pitta Bread': '/groceries/en-IE/shop/bakery/bread/naan-and-pitta-bread',
            'Rolls, Bagels & Wraps': '/groceries/en-IE/shop/bakery/bread/rolls-bagels-and-wraps',
            'White Bread': '/groceries/en-IE/shop/bakery/bread/white-bread',
            'World & Speciality Bread': '/groceries/en-IE/shop/bakery/bread/world-and-speciality-bread',
            'Seeded Bread': '/groceries/en-IE/shop/bakery/bread/seeded-bread',
            'Half & half Bread': '/groceries/en-IE/shop/bakery/bread/half-and-half-bread',
            'Small Loaves': '/groceries/en-IE/shop/bakery/bread/small-loaves',
            'Brown and Wholemeal Bread': '/groceries/en-IE/shop/bakery/bread/brown-and-wholemeal-bread',
            'Healthy Bread': '/groceries/en-IE/shop/bakery/bread/healthy-bread',
            'Offers on Bread': '/groceries/en-IE/shop/bakery/bread/all?viewAll=promotion&promotion=offers',
        },
        'Croissants & Pastries': {
            'All Croissants & Pastries': '/groceries/en-IE/shop/bakery/croissants-and-pastries/all',
            'Croissants': '/groceries/en-IE/shop/bakery/croissants-and-pastries/croissants',
            'Pastries': '/groceries/en-IE/shop/bakery/croissants-and-pastries/pastries',
            'Offers on Croissants & Pastries': '/groceries/en-IE/shop/bakery/croissants-and-pastries/all?viewAll=promotion&promotion=offers',
        },
        'Crumpets & Pancakes': {
            'All Crumpets & Pancakes': '/groceries/en-IE/shop/bakery/crumpets-and-pancakes/all',
            'Crumpets & Pancakes': '/groceries/en-IE/shop/bakery/crumpets-and-pancakes/crumpets-and-pancakes',
            'Offers on Crumpets & Pancakes': '/groceries/en-IE/shop/bakery/crumpets-and-pancakes/all?viewAll=promotion&promotion=offers',
        },
        'Cakes & Pies': {
            'All Cakes & Pies': '/groceries/en-IE/shop/bakery/cakes-and-pies/all',
            'Birthday & Celebration Cakes': '/groceries/en-IE/shop/bakery/cakes-and-pies/birthday-and-celebration-cakes',
            'Fruit Pies & Tarts': '/groceries/en-IE/shop/bakery/cakes-and-pies/fruit-pies-and-tarts',
            'Large Cakes & Swiss Rolls': '/groceries/en-IE/shop/bakery/cakes-and-pies/large-cakes-and-swiss-rolls',
            'Multipack Bars & Mini Bites': '/groceries/en-IE/shop/bakery/cakes-and-pies/multipack-bars-and-mini-bites',
            'Scones, Buns & Fruitcakes': '/groceries/en-IE/shop/bakery/cakes-and-pies/scones-buns-and-fruitcakes',
            'Seasonal Cakes': '/groceries/en-IE/shop/bakery/cakes-and-pies/seasonal-cakes',
            'Cake Slices': '/groceries/en-IE/shop/bakery/cakes-and-pies/cake-slices',
            'Small Cakes': '/groceries/en-IE/shop/bakery/cakes-and-pies/small-cakes',
            'Offers on Cakes & Pies': '/groceries/en-IE/shop/bakery/cakes-and-pies/all?viewAll=promotion&promotion=offers',
        },
        'Doughnuts, Muffins & Cookies': {
            'All Doughnuts, Muffins & Cookies': '/groceries/en-IE/shop/bakery/doughnuts-muffins-and-cookies/all',
            'Cookies & Flapjacks': '/groceries/en-IE/shop/bakery/doughnuts-muffins-and-cookies/cookies-and-flapjacks',
            'Doughnuts': '/groceries/en-IE/shop/bakery/doughnuts-muffins-and-cookies/doughnuts',
            'Muffins & Brownies': '/groceries/en-IE/shop/bakery/doughnuts-muffins-and-cookies/muffins-and-brownies',
            'Offers on Doughnuts, Muffins & Cookies': '/groceries/en-IE/shop/bakery/doughnuts-muffins-and-cookies/all?viewAll=promotion&promotion=offers',
        },
        'Flans & Pastry': {
            'All Flans & Pastry': '/groceries/en-IE/shop/bakery/flans-and-pastry/all',
            'Sweet & Savoury Bases': '/groceries/en-IE/shop/bakery/flans-and-pastry/sweet-and-savoury-bases',
            'Fresh Pastry & Baking': '/groceries/en-IE/shop/bakery/flans-and-pastry/fresh-pastry-and-baking',
            'Offers on Flans & Pastry': '/groceries/en-IE/shop/bakery/flans-and-pastry/all?viewAll=promotion&promotion=offers',
        },
        'Specialist Bakery': {
            'All Specialist Bakery': '/groceries/en-IE/shop/bakery/specialist-bakery/all',
            'Gluten Free': '/groceries/en-IE/shop/bakery/specialist-bakery/gluten-free',
            'Free From': '/groceries/en-IE/shop/bakery/specialist-bakery/free-from',
            'Offers on Specialist Bakery': '/groceries/en-IE/shop/bakery/specialist-bakery/all?viewAll=promotion&promotion=offers',
        },
        'Christmas Bakery': {
            'All Christmas Bakery': '/groceries/en-IE/shop/bakery/christmas-bakery/all',
            'Christmas Cakes & Pies': '/groceries/en-IE/shop/bakery/christmas-bakery/christmas-cakes-and-pies',
            'Offers on Christmas Bakery': '/groceries/en-IE/shop/bakery/christmas-bakery/all?viewAll=promotion&promotion=offers',
        },
        'Cakes, Cake Bars, Slices & Pies': {
            'All Cakes, Cake Bars, Slices & Pies': '/groceries/en-IE/shop/bakery/cakes-cake-bars-slices-and-pies/all',
            'Birthday & Celebration Cakes': '/groceries/en-IE/shop/bakery/cakes-cake-bars-slices-and-pies/birthday-and-celebration-cakes',
            'Large Sharing Cakes': '/groceries/en-IE/shop/bakery/cakes-cake-bars-slices-and-pies/large-sharing-cakes',
            'Small Cakes, Bites & Slices': '/groceries/en-IE/shop/bakery/cakes-cake-bars-slices-and-pies/small-cakes-bites-and-slices',
            'Offers on Cakes, Cake Bars, Slices & Pies': '/groceries/en-IE/shop/bakery/cakes-cake-bars-slices-and-pies/all?viewAll=promotion&promotion=offers',
        },
        'Finest Bakery': {
            'All Finest Bakery': '/groceries/en-IE/shop/bakery/finest-bakery/all',
            'Finest Bread': '/groceries/en-IE/shop/bakery/finest-bakery/finest-bread',
            'Finest Sweet Bakery': '/groceries/en-IE/shop/bakery/finest-bakery/finest-sweet-bakery',
            'Offers on Finest Bakery': '/groceries/en-IE/shop/bakery/finest-bakery/all?viewAll=promotion&promotion=offers',
        },
        'From Our Bakery': {
            'All From Our Bakery': '/groceries/en-IE/shop/bakery/from-our-bakery/all',
            'Bread From Our Bakery': '/groceries/en-IE/shop/bakery/from-our-bakery/bread-from-our-bakery',
            'Doughnuts From Our Bakery': '/groceries/en-IE/shop/bakery/from-our-bakery/doughnuts-from-our-bakery',
            'Scones From Our Bakery': '/groceries/en-IE/shop/bakery/from-our-bakery/scones-from-our-bakery',
            'Sweet Treats From Our Bakery': '/groceries/en-IE/shop/bakery/from-our-bakery/sweet-treats-from-our-bakery',
            'Offers on From Our Bakery': '/groceries/en-IE/shop/bakery/from-our-bakery/all?viewAll=promotion&promotion=offers',
        'Fruit Loaves, Hot Cross Buns & Scones': {
            'All Fruit Loaves, Hot Cross Buns & Scones': '/groceries/en-IE/shop/bakery/fruit-loaves-hot-cross-buns-and-scones/all',
            'Scones': '/groceries/en-IE/shop/bakery/fruit-loaves-hot-cross-buns-and-scones/scones',
            'Offers on Fruit Loaves, Hot Cross Buns & Scones': '/groceries/en-IE/shop/bakery/fruit-loaves-hot-cross-buns-and-scones/all?viewAll=promotion&promotion=offers',
        },
        'Pancakes, Waffles, Farls & Crumpets': {
            'All Pancakes, Waffles, Farls & Crumpets': '/groceries/en-IE/shop/bakery/pancakes-waffles-farls-and-crumpets/all',
            'Pancakes': '/groceries/en-IE/shop/bakery/pancakes-waffles-farls-and-crumpets/pancakes',
            'Offers on Pancakes, Waffles, Farls & Crumpets': '/groceries/en-IE/shop/bakery/pancakes-waffles-farls-and-crumpets/all?viewAll=promotion&promotion=offers',
            },
        }
    }
}

# Scrape each category
for main_category, subcategories in categories.items():
    scrape_category(main_category, subcategories)
