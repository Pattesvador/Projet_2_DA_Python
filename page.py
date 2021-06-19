import requests
from bs4 import BeautifulSoup
import csv


def scrap_page(url, file_title):
    response = requests.get(url)
    if not response:
        print("Veuillez saisir une adresse valide.")
    else:
        info_page = {}
        soup = BeautifulSoup(response.text, "html.parser")
        info_page["product_page_url"] = response.url
        info_page["universal_product_code"] = soup.find("th", text="UPC").next_sibling.text
        info_page["title"] = soup.find("div", class_="col-sm-6 product_main").h1.text
        info_page["price_including_tax"] = soup.find("th", text="Price (incl. tax)").next_sibling.text[1:]
        info_page["price_excluding_tax"] = soup.find("th", text="Price (excl. tax)").next_sibling.text[1:]
        info_page["number_available"] = soup.find("th", text="Availability").next_sibling.next_sibling.text
        product_description = soup.find(id="product_description")

        if product_description:
            info_page["product_description"] = soup.find(id="product_description").next_sibling.next_sibling.text
        else:
            info_page["product_description"] = "No product description available"

        info_page["category"] = soup.find_all("a")[3].text
        info_page["review_rating"] = soup.find("p", class_="star-rating").attrs["class"][1]
        info_page["image_url"] = "https://books.toscrape.com/" + soup.find("img").attrs["src"]

        with open(file_title, "a", encoding="utf-8", newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(info_page.values())

        img_url = requests.get(info_page["image_url"])
        img_file = info_page["title"] + ".jpg"
        with open(img_file, "wb") as file:
            file.write(img_url.content)

    return info_page


print(scrap_page("https://books.toscrape.com/catalogue/in-a-dark-dark-wood_963/index.html", "Mystery.csv"))
# print(scrap_page("https://books.toscrape.com/catalogue/alice-in-wonderland-alices-adventures-in-wonderland-1_5/index.html", "Mystery.csv"))
# print(scrap_page("https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"))
# for i in scrap_page("https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html").values():
#    print(i, "\n")

'''
url = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"

response = requests.get(url)
if response:
    soup = BeautifulSoup(response.text, "html.parser")
    # clean = soup.prettify()
    # print(clean)
    product_page_url = response.url
    print(product_page_url)
    print(type(product_page_url))
    universal_product_code = soup.find("th", text="UPC").next_sibling
    print(universal_product_code.text)
    print(type(universal_product_code))
    # universal_product_code = universal_product_code.next_sibling.text
    title = soup.find("div", class_="col-sm-6 product_main").h1
    print(title.text)
    print(type(title))
    price_including_tax = soup.find("th", text="Price (incl. tax)").next_sibling
    print(price_including_tax.text)
    print(type(price_including_tax))
    price_excluding_tax = soup.find("th", text="Price (excl. tax)").next_sibling
    print(price_excluding_tax.text)
    print(type(price_excluding_tax))
    number_available = soup.find("th", text="Availability").next_sibling.next_sibling
    print(number_available.text)
    print(type(number_available))
    product_description = soup.find(id="product_description").next_sibling.next_sibling
    print(product_description.text)
    print(type(product_description))
    # category = soup.find("ul", class_="breadcrumb").next_element.next_element
    category = soup.find_all("a")[3]
    # category = category[3]
    print(category.text)
    print(type(category))
    # review_rating = soup.find("div", class_="col-sm-6 product_main").p
    review_rating = soup.find("p", class_="star-rating").attrs["class"][1]
    print(review_rating)
    print(type(review_rating))
    image_url = soup.find("img").attrs
    print(image_url["src"])
    print(type(image_url))
    # print(universal_product_code, title, price_including_tax, price_excluding_tax, number_available.next_sibling)
else:
    print("PAS OK")
'''