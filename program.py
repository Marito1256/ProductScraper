from dotenv import load_dotenv
import os
import openai
from bs4 import BeautifulSoup
import requests
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
    products = []
    product_elements = soup.select_one('div.sc-plp-cards.sc-plp-cards-grid')
    if product_elements:
        for element in product_elements.select('div.sc-pc-title-medium h3'):
            print(element.get_text(strip=True))
    else:
        print("no product element found")
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
        driver.get(f"https://www.samsclub.com/s/{searchParam}")
        HTML2 = driver.page_source
        # print(driver.page_source[:1000])
    finally:
        try:
            driver.quit()
        except:
            pass
    soup = BeautifulSoup(HTML2, "html.parser")
    soup2 = BeautifulSoup(HTML2, "html.parser")
    # title = soup.find("h1", id="main-title").get_text(strip=True)
    # itemStack = soup.find("div", attrs={"data-testid":"item-stack"})
    # titles = itemStack.find_all("span", class_="w_iUH7")
    products = extract_products_SamsClub(soup)
    # products += extract_prodcuts_target(soup2)
    # print(HTML2) checking we can access the html in the first place
    print("thats all")
    print("\n\n\n\n")
    return products
if __name__ == "__main__":
    input = input("Search here\n")
    products = mainone(input)
    for product in products:
        print(f"Product:\n{product['title']}\nprice:\n{product['price']}\nReviews:\n{product['reviews']}\n")
