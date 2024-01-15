import os
from urllib.parse import urljoin
categories = {
    'Bakery': {
        'In Store Bakery': {
            'All In Store Bakery': '/groceries/en-IE/shop/bakery/in-store-bakery/all?include-children=true',
            'Brown & Seeded Bread': '/groceries/en-IE/shop/bakery/in-store-bakery/brown-and-seeded-bread?include-children=true',
            'In Store French Bread & Rolls': '/groceries/en-IE/shop/bakery/in-store-bakery/in-store-french-bread-and-rolls?include-children=true',
            'In Store Speciality Bread': '/groceries/en-IE/shop/bakery/in-store-bakery/in-store-speciality-bread?include-children=true',
            'In Store Tea Cakes & Scones': '/groceries/en-IE/shop/bakery/in-store-bakery/in-store-tea-cakes-and-scones?include-children=true',
            'Rolls': '/groceries/en-IE/shop/bakery/in-store-bakery/rolls?include-children=true',
            'White Bread': '/groceries/en-IE/shop/bakery/in-store-bakery/white-bread?include-children=true',
            'Offers on In Store Bakery': '/groceries/en-IE/shop/bakery/in-store-bakery/all?viewAll=promotion&amp;promotion=offers?include-children=true',
        },
        'Bread': {
            'All Bread': '/groceries/en-IE/shop/bakery/bread/all?include-children=true',
            'Brown & Seeded Bread': '/groceries/en-IE/shop/bakery/bread/brown-and-seeded-bread?include-children=true',
            'Naan & Pitta Bread': '/groceries/en-IE/shop/bakery/bread/naan-and-pitta-bread?include-children=true',
            'Rolls, Bagels & Wraps': '/groceries/en-IE/shop/bakery/bread/rolls-bagels-and-wraps?include-children=true',
            'White Bread': '/groceries/en-IE/shop/bakery/bread/white-bread?include-children=true',
            'World & Speciality Bread': '/groceries/en-IE/shop/bakery/bread/world-and-speciality-bread?include-children=true',
            'Seeded Bread': '/groceries/en-IE/shop/bakery/bread/seeded-bread?include-children=true',
            'Half & half Bread': '/groceries/en-IE/shop/bakery/bread/half-and-half-bread?include-children=true',
            'Small Loaves': '/groceries/en-IE/shop/bakery/bread/small-loaves?include-children=true',
            'Brown and Wholemeal Bread': '/groceries/en-IE/shop/bakery/bread/brown-and-wholemeal-bread?include-children=true',
            'Healthy Bread': '/groceries/en-IE/shop/bakery/bread/healthy-bread?include-children=true',
            'Offers on Bread': '/groceries/en-IE/shop/bakery/bread/all?viewAll=promotion&amp;promotion=offers?include-children=true',
        },
    },
    'Fresh Food': {
        'Fresh Fruit': {
            'All Fresh Fruit': '/groceries/en-IE/shop/fresh-food/fresh-fruit/all?include-children=true',
            'Apples, Pears & Rhubarb': '/groceries/en-IE/shop/fresh-food/fresh-fruit/apples-pears-and-rhubarb?include-children=true',
            'Avocados': '/groceries/en-IE/shop/fresh-food/fresh-fruit/avocados?include-children=true',
            'Bananas': '/groceries/en-IE/shop/fresh-food/fresh-fruit/bananas?include-children=true',
            'Berries & Cherries': '/groceries/en-IE/shop/fresh-food/fresh-fruit/berries-and-cherries?include-children=true',
            'Citrus Fruit': '/groceries/en-IE/shop/fresh-food/fresh-fruit/citrus-fruit?include-children=true',
            'Dried Fruit & Nuts': '/groceries/en-IE/shop/fresh-food/fresh-fruit/dried-fruit-and-nuts?include-children=true',
            'Grapes': '/groceries/en-IE/shop/fresh-food/fresh-fruit/grapes?include-children=true',
            'Nectarines & Peaches': '/groceries/en-IE/shop/fresh-food/fresh-fruit/nectarines-and-peaches?include-children=true',
            'Organic Fruit': '/groceries/en-IE/shop/fresh-food/fresh-fruit/organic-fruit?include-children=true',
            'Plums & Apricots': '/groceries/en-IE/shop/fresh-food/fresh-fruit/plums-and-apricots?include-children=true',
            'Prepared Fruit': '/groceries/en-IE/shop/fresh-food/fresh-fruit/prepared-fruit?include-children=true',
            'Tropical & Exotic Fruit': '/groceries/en-IE/shop/fresh-food/fresh-fruit/tropical-and-exotic-fruit?include-children=true',
            'Offers on Fresh Fruit': '/groceries/en-IE/shop/fresh-food/fresh-fruit/all?viewAll=promotion&amp;promotion=offers?include-children=true',
        },
        'Fresh Vegetables': {
            'All Fresh Vegetables': '/groceries/en-IE/shop/fresh-food/fresh-vegetables/all?include-children=true',
            'Baby Vegetables': '/groceries/en-IE/shop/fresh-food/fresh-vegetables/baby-vegetables?include-children=true',
            'Broccoli, Cauliflower & Cabbage': '/groceries/en-IE/shop/fresh-food/fresh-vegetables/broccoli-cauliflower-and-cabbage?include-children=true',
            'Carrots & Root Vegetables': '/groceries/en-IE/shop/fresh-food/fresh-vegetables/carrots-and-root-vegetables?include-children=true',
            'Chillies, Garlic & Ginger': '/groceries/en-IE/shop/fresh-food/fresh-vegetables/chillies-garlic-and-ginger?include-children=true',
            'Courgettes, Aubergines & Asparagus': '/groceries/en-IE/shop/fresh-food/fresh-vegetables/courgettes-aubergines-and-asparagus?include-children=true',
            'Mushrooms': '/groceries/en-IE/shop/fresh-food/fresh-vegetables/mushrooms?include-children=true',
            'Onions & Shallots': '/groceries/en-IE/shop/fresh-food/fresh-vegetables/onions-and-shallots?include-children=true',
            'Organic Vegetables': '/groceries/en-IE/shop/fresh-food/fresh-vegetables/organic-vegetables?include-children=true',
            'Peas, Beans & Sweetcorn': '/groceries/en-IE/shop/fresh-food/fresh-vegetables/peas-beans-and-sweetcorn?include-children=true',
            'Potatoes': '/groceries/en-IE/shop/fresh-food/fresh-vegetables/potatoes?include-children=true',
            'Prepared Vegetables': '/groceries/en-IE/shop/fresh-food/fresh-vegetables/prepared-vegetables?include-children=true',
            'Seasonal Vegetables': '/groceries/en-IE/shop/fresh-food/fresh-vegetables/seasonal-vegetables?include-children=true',
            'Spinach, Greens & Kale': '/groceries/en-IE/shop/fresh-food/fresh-vegetables/spinach-greens-and-kale?include-children=true',
            'Stir Fry': '/groceries/en-IE/shop/fresh-food/fresh-vegetables/stir-fry?include-children=true',
            'Offers on Fresh Vegetables': '/groceries/en-IE/shop/fresh-food/fresh-vegetables/all?viewAll=promotion&amp;promotion=offers?include-children=true',
        },
        'Salads & Dips': {
            'All Salads & Dips': '/groceries/en-IE/shop/fresh-food/salads-and-dips/all?include-children=true',
            'Chilled Dips': '/groceries/en-IE/shop/fresh-food/salads-and-dips/chilled-dips?include-children=true',
            'Coleslaw & Dressed Salads': '/groceries/en-IE/shop/fresh-food/salads-and-dips/coleslaw-and-dressed-salads?include-children=true',
            'Fresh Herbs, Chillies & Spices': '/groceries/en-IE/shop/fresh-food/salads-and-dips/fresh-herbs-chillies-and-spices?include-children=true',
            'Prepared Salad & Salad Bags': '/groceries/en-IE/shop/fresh-food/salads-and-dips/prepared-salad-and-salad-bags?include-children=true',
            'Salad Vegetables': '/groceries/en-IE/shop/fresh-food/salads-and-dips/salad-vegetables?include-children=true',
            'Tomatoes': '/groceries/en-IE/shop/fresh-food/salads-and-dips/tomatoes?include-children=true',
            'Offers on Salads & Dips': '/groceries/en-IE/shop/fresh-food/salads-and-dips/all?viewAll=promotion&amp;promotion=offers?include-children=true',
        },
    }
    # Add more categories as needed
}

# Scrape each category
for main_category, subcategories in categories.items():
    category_folder = os.path.join('C:\\Users\\dammy.OLUWADAMILOLA\\VS Developer\\WebScraper\\Tesco', main_category)
    #print(category_folder)
    for subcategory_name, subcategory_url in subcategories.items():
        subcategory_folder = os.path.join(category_folder, subcategory_name)
        #print(subcategory_folder)
        for subsubcatrgory, subsubcatrgory_url in subcategory_url.items():
            full_url = urljoin('https://www.tesco.ie', subsubcatrgory_url)
            output_file_path = os.path.join(subcategory_folder, f'{subsubcatrgory}.csv')
            #print(full_url)
            print(output_file_path)