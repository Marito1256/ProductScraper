from dotenv import load_dotenv
import os
import openai
from bs4 import BeautifulSoup
import requests
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#Load the api key
load_dotenv()
openai.api_key = os.getenv("OPENAI_APIKEY")

# list of data we need to start a report
# response =  openai.chat.completions.create(
#     model="gpt-4o",
#     messages=[
#         {"role": "system", "content": "you are allow to research on the internet, and retrieve relevant hyperlinks and related information about them"},
#         {"role": "user", "content": "give me all product listings and hyperlinks from popular retailers for the Vaio product with model number VWTC7M164B-FE"}
#     ]
# )
# import requests
# from bs4 import BeautifulSoup
import undetected_chromedriver as uc
HTML1 = str()

def extract_products_walmart(soup):
    products = []

    # Each product card is a direct child of the item stack container
    item_stack = soup.find("div", attrs={"data-testid": "item-stack"})
    product_cards = item_stack.find_all("div", recursive=False) if item_stack else []

    for card in product_cards:
        # Title
        title_elem = card.find("span", attrs={"data-automation-id": "product-title"})
        title = title_elem.get_text(strip=True) if title_elem else "N/A"

        # Price
        dollars = card.find("span", class_="f2")
        cents_elem = card.find_all("span", class_="f6 f5-l")
        cents = next((c.get_text(strip=True) for c in cents_elem if c.get_text(strip=True).isdigit()), "00")
        price = f"${dollars.get_text(strip=True)}.{cents}" if dollars else "N/A"

        # Reviews
        # review_elem = card.find("span",  class_="w_iUH7")
        # reviews = review_elem.get_text(strip = True) if review_elem else "No reviews"
        rating_container = card.find("div", class_="flex items-center mt2")
        reviews = "No rating"

        if rating_container:
            rating_span = rating_container.find("span", class_="w_iUH7")
            if rating_span:
                reviews = rating_span.get_text(strip=True)
        products.append({
            "title": title,
            "price": price,
            "reviews": reviews
        })

    return products
def extract_products_SamsClub(soup):
    productsArray = []
    # Find all product containers
    products = soup.select("div.sc-plp-cards-card")
    for product in products:
        title_tag = product.select_one("div.sc-pc-title-medium h3")
        price_tag = product.select_one("span.visuallyhidden")
        review_label = product.select_one("label.bst-rating")

        title = title_tag.get_text(strip=True) if title_tag else "No title"
        price = price_tag.get_text(strip=True).replace("Current price: ", "") if price_tag else "No price"
        reviews = review_label.get_text(strip=True).split(")")[-1].strip("()") if review_label else "No reviews"
        if title:
            print(f"Title: {title}")
        else:
            title="title missing"
            print(f"{title}")
        if price:
            print(f"Price: {price}")
        else:
            price = "price missing" 
            print(f"{price}")
        if reviews:
            print(f"Reviews: {reviews}")
        else:
            reviews = "reviews missing"
            print(f"{reviews}")
        print("-" * 40)
    productsArray.append({
            "title": title,
            "price": price,
            "reviews": reviews
    })
    return productsArray
 
def extract_products_Target(soup):
    products = []
    
    # Save full HTML for debugging
    with open("output.html", "w", encoding="utf-8") as f:
        f.write(str(soup.prettify()))

    # Find product cards using data-test attribute
    cards = soup.find_all("div", attrs={"data-test": "@web/site-top-of-funnel/ProductCardWrapper"})

    for card in cards:
        title = card.find("a", attrs={"data-test": "product-title"}).get_text(strip=True) if card.find("a", attrs={"data-test": "product-title"}) else "N/A"
        priceSpan = card.find("span", attrs={"data-test": "current-price"})
        price = priceSpan.find("span").get_text(strip=True) if priceSpan else "N/A"
        reviews = card.find("span", attrs={"class": "styles_ndsScreenReaderOnly__mcNC_ styles_notFocusable__XkHOR"}).get_text(strip=True) if card.find("span", attrs={"data-test": "rating-count"}) else "N/A"
        
        products.append({
            "title": title,
            "price": price,
            "reviews": reviews
        })
    return products

def mainone(searchParam):
    options= uc.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36")

    driver=uc.Chrome(options=options)
    # target_driver = uc.Chrome(options=options)
    try:
        # driver.get(f"https://www.walmart.com/search?q={searchParam}")
        # HTML1 = driver.page_source
        # driver.get(f"https://www.samsclub.com/s/{searchParam}")
        # HTML2 = driver.page_source
        driver.get(f"https://www.target.com/s?searchTerm={searchParam}")
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-test="@web/site-top-of-funnel/ProductCardWrapper"]'))
        )
        time.sleep(10)
        HTML1 = driver.page_source
        # print(driver.page_source[:1000])
        soup = BeautifulSoup(HTML1, "html.parser")
    
        # products = extract_products_SamsClub(soup)
        products = extract_products_Target(soup)
    finally:
        try:
            driver.quit()
        except:
            pass
    print("-" *20)
    print("\n\n\n\n")
    return products
if __name__ == "__main__":
    input = input("Search here\n")
    products = mainone(input)
    count = 0
    for product in products:
        count += 1
        print(f"Product {count}:\n{product['title']}\nprice:\n{product['price']}\nReviews:\n{product['reviews']}\n")
