import requests
from bs4 import BeautifulSoup
import csv
import os

# url = "https://books.toscrape.com/index.html"
# response = requests.get(url)


def gather_categories(url):
    """Récupère les url de toutes les catégories"""
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    categories = soup.find("div", class_="side_categories").find_all("a")
    categories_url = []
    for i in categories:
        categories_url.append("https://books.toscrape.com/" + i.get("href"))
    categories_url.pop(0)

    return categories_url


def gather_books(url, books_list):
    print("Récupération de la catégorie ", url)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    header_title = soup.find("li", class_="active").text
    datas_file_path = os.path.join('data', header_title + ".csv")
    iterable = soup.find_all("h3")

    for i in iterable:
        part_url = i.find("a").get("href")
        books_list.append(construct_url("https://books.toscrape.com/catalogue/", part_url))
    if soup.find("li", class_="next"):
        # print(soup.find("li", class_="next").find("a").get('href'))
        next_page_part_url = soup.find("li", class_="next").find("a").get("href")
        gather_books(construct_url_2(response.url, next_page_part_url), books_list)

    try:
        os.mkdir(os.getcwd() + "\\data")
    except FileExistsError:
        None

    with open(datas_file_path, "w", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([header_title])
        writer.writerow([
            "Product page URL",
            "Universal product code",
            "Title", "Price including tax",
            "Price excluding tax", "Number available",
            "Product description",
            "Category",
            "Review rating",
            "Image URL"
        ])

    return books_list, datas_file_path


def construct_url(url, part_url):
    part_url = part_url.split("/")
    part_url = list(dict.fromkeys(part_url))
    part_url.pop(0)
    part_url = "/".join(part_url)
    url = url + part_url

    return url


def construct_url_2(url, part_url):
    url = url.split("/")
    url.pop(-1)
    url.append(part_url)
    url = "/".join(url)

    return url


def scrap_page(url, data_file_path):
    response = requests.get(url)
    response.encoding = "utf-8"

    info_page = {}
    soup = BeautifulSoup(response.text, "html.parser")
    info_page["product_page_url"] = response.url
    info_page["universal_product_code"] = soup.find("th", text="UPC").next_sibling.text
    info_page["title"] = soup.find("div", class_="col-sm-6 product_main").h1.text
    print("Téléchargement du livre ", info_page["title"])
    info_page["price_including_tax"] = soup.find("th", text="Price (incl. tax)").next_sibling.text  # [1:]
    info_page["price_excluding_tax"] = soup.find("th", text="Price (excl. tax)").next_sibling.text  # [1:]
    info_page["number_available"] = soup.find("th", text="Availability").next_sibling.next_sibling.text
    product_description = soup.find(id="product_description")
    if product_description:
        info_page["product_description"] = soup.find(id="product_description").next_sibling.next_sibling.text
    else:
        info_page["product_description"] = "No product description available"
    info_page["category"] = soup.find_all("a")[3].text
    info_page["review_rating"] = soup.find("p", class_="star-rating").attrs["class"][1]
    info_page["image_url"] = "https://books.toscrape.com/" + "/".join(
        soup.find("img").attrs["src"].split("/")[2:])  # soup.find("img").attrs["src"]

    with open(data_file_path, "a", encoding="utf-8", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(info_page.values())

    img_url = requests.get(info_page["image_url"])
    img_file = response.url.split("/")[-2][:166] + ".jpg"
    print(os.path.join('images', img_file))

    try:
        os.mkdir(os.getcwd() + '\\images')
    except FileExistsError:
        None

    with open(os.path.join('images', img_file), "wb") as file:
        file.write(img_url.content)

    return info_page


categories_list = gather_categories(("https://books.toscrape.com/index.html"))
for category in categories_list:
    category_books_list, data_file_path = gather_books(category, books_list=[])
    for book in category_books_list:
        scrap_page(book, data_file_path)



'''
categories_list = gather_categories("https://books.toscrape.com/index.html")
# all_books_list = []
for i in categories_list:
    all_books_list.extend(gather_books(i, books_list = []))

all_books_infos = []
for i in all_books_list:
    all_books_infos.append(scrap_page(i))

print(all_books_infos[0], all_books_infos[499], all_books_infos[999])
print(len(all_books_infos))
# var = "\n".join(all_books_list)
# print(var)
'''


